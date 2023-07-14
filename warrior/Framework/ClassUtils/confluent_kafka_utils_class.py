'''
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
from warrior.Framework.Utils.print_Utils import print_info, print_error, print_exception
from warrior.Framework.Utils import config_Utils
import json
import time
try:
    from confluent_kafka import Producer, DeserializingConsumer, Consumer
    from confluent_kafka.admin import AdminClient, NewTopic
    from confluent_kafka import KafkaException, TopicPartition, KafkaError
except ImportError as err:
    print_error("Module kafka is not installed, Refer exception below")
    print_exception(err)

class WarriorConfluentKafkaConsumer():
    """
    This class contains all Confluent kafka consumer methods
    """
    def __init__(self, configs):
        """
        Create Kafka Consumer object
        """
        print_info("creating kafka consumer")
        try:
            self.kafka_consumer = Consumer(configs)
        except KafkaException as exc:
            print_error("Kafka consumer - Exception during connecting to broker - {}".format(exc))

    def subscribe_to_topics(self, topics, **kwargs):
        """
        Subscribe to list of specified topics.
        Arguments:
          topics(list): list of topic names to subscribe
          pattern(list): list of topic name patterns to subscribe
          listener(func): callback function
        Returns:
          result(bool) : False if exception occures, True otherwise
        """
        pattern = kwargs.get("pattern", None)
        listener = kwargs.get("listener", None)

        def on_assign(consumer, partitions):
            for partition in partitions:
                partition.offset = -1
            consumer.assign(partitions)

        print_info("subscribe to topics {}".format(topics))
        try:
            self.kafka_consumer.subscribe(topics, on_assign=on_assign)
            result = True
        except KafkaException as exc:
            print_error("Exception during subscribing to topics - {}".format(exc))
            result = False
        return result

    def unsubscribe_to_topics(self):
        """
        Unsubscribe to all topics.
        Arguments: None.
        Returns:
          result(bool) : False if exception occures, True otherwise
        """
        print_info("unsubscribe to all topics")
        try:
            self.kafka_consumer.unsubscribe()
            result = True
        except KafkaException as exc:
            print_error("Exception during unsubscibing to topics - {}".format(exc))
            result = False
        return result

    def assign_partitions(self, partitions):
        """
        Assign partitions to consumer.
        Arguments:
          partitions(list) : list of [topic, partition] lists
            example : [[topic1,1], [topic2,1]]
        Returns:
            None.
        """
        print_info("assigning partitions to consumer {}".format(partitions))
        topic_partitions = [TopicPartition(topic=tup[0], partition=tup[1]) for tup in partitions]
        try:
            self.kafka_consumer.assign(topic_partitions)
            result = True
        except KafkaException as exc:
            print_error("Exception during assiging partitions - {}".format(exc))
            result = False
        return result

    def seek_to_position(self, topic, partition, offset):
        """
        Seek to the given offset.
        Arguments:
          topic(str): topic name
          partition(int): partition number
          offset(int): offset number
        Returns:
          result(bool) : False if exception occures, True otherwise
        """
        print_info("seeking to position {}:{}:{}".format(topic, partition, offset))
        topic_partition = TopicPartition(topic=topic, partition=partition, offset=offset)
        try:
            self.kafka_consumer.seek(partition=topic_partition)
            result = True
        except KafkaException as exc:
            print_error("Exception during seek - {}".format(exc))
            result = False
        return result

    def assign_to_beginning(self, topic=None):
        topic_partitions = []
        if topic is None:
            print_info("Topic not provided for assign to beginning")
        else:
            ltopics = self.kafka_consumer.list_topics()
            dict_topics = ltopics.topics
            if topic not in dict_topics:
                print_info("Topic not present in kafka environment")
            else:
                dict_partitions = dict_topics[topic].partitions
                partitions = list(dict_partitions.keys())
                for partition in partitions:
                    topic_partitions.append(TopicPartition(topic,partition,offset=-2))
                self.kafka_consumer.assign(topic_partitions)

    def assign_to_previous_offset(self, topic=None):
        """
        This function will start reading from 3 offsets back
        from all partitions of a topic
        """
        start_time = time.time()
        max_attempts = 5
        topic_partitions = None
        for _ in range(max_attempts):
            partitions = self.kafka_consumer.assignment()
            if partitions:
                attempt = 0
                while attempt < max_attempts:
                    try:
                        topic_partitions = self.kafka_consumer.committed(partitions, timeout=20)
                        break
                    except KafkaException as e:
                        print_error("Attempt {0} failed: {1}".format(attempt+1, e))
                        attempt += 1
                if topic_partitions is None:
                    print_info("Failed to get committed offsets after {0} attempts".format(max_attempts))
                else:
                    print_info("Successfully fetched committed offsets")
                    break
            self.kafka_consumer.poll(0)
            time.sleep(180)

        if topic_partitions is not None:
            print_info("Partition and offset for the topic: ",  topic)
            for tp in topic_partitions:
                print("Before: partition-{0}, offset-{1}".format(tp.partition, tp.offset))
                if tp.offset < 2:
                    tp.offset = -2
                else:
                    tp.offset = tp.offset - 2
                print("After: partition-{0}, offset-{1}".format(tp.partition, tp.offset))
            print("\n")
            self.kafka_consumer.assign(topic_partitions)
        else:
            print_info("After multiple tries also failed to get committed offsets")

    def get_messages(self, get_all_messages=False, topic=None, **kwargs):
        """
        Get messages from consumer.
        Arguments:
          get_all_messages(bool): set this to True to get all the messages, seeks to the beginning.
                                   Defaults to False.
          timeout(int): timeout in seconds
          max_records(int): maximum messages to fetch
        Returns:
          messages(list): messages from the consumer
        """
        timeout_sec = kwargs.get("timeout", 1.0)
        max_records = kwargs.get("max_records", 200)
        messages = []
        msg_pack = []
        max_attempts=5
        print_info("get messages published to subscribed topics")
        for i in range(max_attempts):
            print_info('Try: {0}'.format(i+1))
            try:
                msg_pack = self.kafka_consumer.consume(int(max_records), int(timeout_sec))
                if msg_pack is None:
                    messages = []
                else:
                    for message in msg_pack:
                        if message.error():
                            raise KafkaException(message.error())
                        else:
                            print("Reading from topic:%s partition:%d offset:%d" % (message.topic(),message.partition(),message.offset()))
                            dict_str = message.value()
                            data = json.loads(dict_str.decode("UTF-8"))
                            messages.append(data)
                            self.kafka_consumer.commit(message)
                break
            except KafkaException as exc:
                if exc.args[0].code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    print_error("Topic or partition not available. Creating topic.")
                    if "kafka_client" in config_Utils.data_repository:
                        war_kafka_client = config_Utils.data_repository["kafka_client"]
                        topic_result = war_kafka_client.create_topics([[topic, 1]], timeout=900)
                        if topic_result:
                            print_info("Topic {} created successfully".format(topic))
                else:
                    print_error("Exception occured in get_messages - {}".format(exc))
                    print_error("Attempt failed, Retrying")
                    time.sleep(180)
            except json.JSONDecodeError as exc:
                print_error("Received incorrect Kafka payload format {}".format(exc))
                break
        return messages

    def get_topics(self):
        """
        Get subscribed topics of the consumer.
        Arguments:
          None.
        Returns:
          topic_list(list of lists): list of [topic, partition] lists
            example : [[topic1,1], [topic2,2]]
        """
        print_info("get all the topics consumer is subscribed to")
        try:
            topic_partitions = self.kafka_consumer.assignment()
            topic_list = [[topic_partition.topic, topic_partition.partition] \
                       for topic_partition in topic_partitions]
        except KafkaException as exc:
            print_error("Exception during getting assigned partitions - {}".format(exc))
            topic_list = None
        return topic_list

class WarriorConfluentKafkaProducer():
    """
    This class contains all kafka producer methods
    """
    def __init__(self, configs, data_format='Json'):
        """
        Create kafka producer object
        """
        print_info("Creating kafka producer")
        self.data_format = data_format
        try:
            self.kafka_producer = Producer(configs)
        except KafkaException as exc:
            print_error("kafka producer - Exception during connecting to broker - {}".format(exc))

    def send_messages(self, topic, value=None, **kwargs):
        """
        Publish messages to the desired topic
        Arguments:
          topic(str): topic name to publish messages
          partition(int): partition nubmer
          value(str): message to publish
        Returns:
          result(bool) : False if exception occures, True otherwise
        """
        partition = kwargs.get("partition", None)
        print_info('publishing messages to the topic: {0}'.format(topic))
        if self.data_format != 'Json':
            value = bytes(value)
        else:
            value = json.dumps(value, indent=4, sort_keys=True, default=str).encode('utf-8')

        def delivery_report(err, msg):
            if err:
                print_error('Message delivery failed: {}'.format(err))
            else:
                print_info('Message delivered to {}'.format(msg.topic()))

        for i in range(5):
            print_info('Try: {0}'.format(i+1))
            try:
                if partition:
                    self.kafka_producer.produce(topic=topic,
                                            value=value,
                                            partition=partition,
                                            callback=delivery_report)
                else:
                    self.kafka_producer.produce(topic=topic, value=value)
                self.kafka_producer.flush()
                result = True
                break
            except BufferError:
                print_error('Local producer queue is full ({0} messages awaiting delivery): '
                        'try again\n'.format(len(self.kafka_producer)))
                result = False
            except KafkaException as exc:
                print_error("Exception during publishing messages - {}".format(exc))
                print("============sleeping for 3 minutes before attempt to reconnect==============")
                time.sleep(180)
                result = False
        return result

class WarriorConfluentKafkaClient():
    """
    This class contains all kafka admin client related
    methods
    """
    def __init__(self, configs):
        """
        create a kafka client
        """
        print_info("Creating kafka client")
        try:
            self.kafka_client = AdminClient(configs)
        except KafkaException as exc:
            print_error("kafka client - Exception during connecting to broker- {}".format(exc))

    def create_topics(self, topic_sets, **kwargs):
        """
        create topics for the producer or consumer to use
        Arguments:
         topic_sets(list) : list of
         ['topic_name', 'num_partitions', 'replication_factor'] lists
         example : ['topic1',1,1]
         timeout(int): time in seconds
        Returns:
          result(bool) : False if exception occures, True otherwise
         None.
        """
        timeout = kwargs.get("timeout", 0)
        validate = kwargs.get("validate", False)
        new_topics = [NewTopic(topic=tup[0], num_partitions=tup[1]) for tup in topic_sets]
        print_info("creating topics")
        try:
            fs = self.kafka_client.create_topics(new_topics=new_topics,
                                            operation_timeout=float(timeout),
                                            request_timeout=float(timeout),
                                            validate_only=validate)
            for topic, f in fs.items():
                f.result()
                print_info("Topic {} created".format(topic))
            result = True
        except KafkaException as exc:
            print_error("Exception during creating topics - {}".format(exc))
            result = False
        return result

    def delete_topics(self, topics, timeout=None):
        """
        Delete topics
        Arguments:
          topics(list): list of topic names
          timeout(int): timeout in seconds
        Returns:
          result(bool) : False if exception occures, True otherwise
        """
        print_info("deleting topics {}".format(topics))
        try:
            fs = self.kafka_client.delete_topics(topics=topics,
                                                 operation_timeout=float(timeout),
                                                 request_timeout=float(timeout))
            for topic, f in fs.items():
                f.result()
                print_info("Topic {} deleted".format(topic))
            result = True
        except KafkaException as exc:
            print_error("Exception during deleting topics - {}".format(exc))
            result = False
        return result
