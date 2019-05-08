from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka import TopicPartition
from kafka.admin import KafkaAdminClient, NewTopic, NewPartitions

class WarriorKafkaConsumer(object):
    """
    This class contains all kafka consumer methods
    """
    def __init__(self, *topics, **configs):
        """
        Create Kafka Consumer object
        """
        self.kafka_consumer = KafkaConsumer(*topics, **configs)

    def subscribe_to_topics(self, topics, **kwargs):
        """
        Subscribe to list of specified topics.
        Arguments:
          topics(list): list of topic names to subscribe
          pattern(list): list of topic name patterns to subscribe
          listener(func): callback function
        Returns:
          None.
        """
        pattern = kwargs.get("pattern", None)
        listener = kwargs.get("listener", None)
        self.kafka_consumer.subscribe(topics=topics,
                                      pattern=pattern,
                                      listener=listener)

    def unsubscribe_to_topics(self):
        """
        Unsubscribe to all topics.
        Arguments: None.
        Returns: None.
        """
        self.kafka_consumer.unsubscribe()

    def assign_partitions(self, partitions):
        """
        Assign partitions to consumer.
        Arguments:
          partitions(list) : list of [topic, partition] lists
            example : [[topic1,1], [topic2,1]]
        Returns:
            None.
        """
        topic_partitions = [TopicPartition(topic=tup[0],partition=tup[1]) for tup in partitions]
        self.kafka_consumer.assign(topic_partitions)

    def seek_to_position(self, topic, partition, offset):
        """
        Seek to the given offset.
        Arguments:
          topic(str): topic name
          partition(int): partition number
          offset(int): offset number
        Returns:
          None
        """
        topic_partition = TopicPartition(topic=topic,partition=partition)
        self.kafka_consumer.seek(partition=topic_partition, offset=offset)

    def get_messages(self, get_all_messages=False, **kwargs):
        """
        Get messages from consumer.
        Arguments:
          get_all_messages(bool): set this to True to get all the messages, seeks to the beginning.
                                   Defaults to False.
          timeout(int): timeout in milliseconds
          max_records(int): maximum messages to fetch
        Returns:
          messages(list): messages from the consumer
        """
        timeout_ms = kwargs.get("timeout", 0)
        max_records = kwargs.get("max_records", None)
        messages = []
        if get_all_messages:
            self.kafka_consumer.seek_to_beginning()
        msg_pack = self.kafka_consumer.poll(timeout_ms, max_records)
        for tp, message_list in msg_pack.items():
            for message in message_list:
                messages.append(message.value)
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
        topic_partitions = self.kafka_consumer.assignment()
        topic_list = [[topic_partition.topic, topic_partition.partition] for topic_partition in topic_partitions]
        return topic_list

class WarriorKafkaProducer(object):
    """
    This class contains all kafka producer methods
    """
    def __init__(self, **configs):
        """
        Create kafka producer object
        """
        self.kafka_producer = KafkaProducer(**configs)

    def send_messages(self, topic, value=None, **kwargs):
        """
        Publish messages to the desired topic
        Arguments:
          topic(str): topic name to publish messages
          partition(int): partition nubmer
          key(str): key name
          value(str): message to publish
        Returns:
          None
        """
        partition = kwargs.get("partition", None)
        headers = kwargs.get("headers", None)
        timestamp = kwargs.get("timestamp", None)
        key = kwargs.get("key", None)
        self.kafka_producer.send(topic=topic,
                                 value=value,
                                 partition=partition,
                                 key=key,
                                 headers=headers,
                                 timestamp_ms=timestamp)
        self.kafka_producer.flush()

class WarriorKafkaClient(object):
    """
    This class contains all kafka admin client related
    methods
    """
    def __init__(self, **configs):
        """
        create a kafka client
        """
        self.kafka_client = KafkaAdminClient(**configs)

    def create_topics(self, topic_sets, **kwargs):
        """
        create topics for the producer or consumer to use
        Arguments:
         topic_sets(list) : list of
         ['topic_name', 'num_partitions', 'replication_factor'] lists
         example : ['topic1',1,1]
         timeout(int): time in milliseconds
        Returns:
         None.
        """
        timeout = kwargs.get("timeout", None)
        validate = kwargs.get("validate", False)
        new_topics = [NewTopic(name=tup[0], num_partitions=tup[1],
                      replication_factor=tup[2]) for tup in topic_sets]
        self.kafka_client.create_topics(new_topics=new_topics,
                                        timeout_ms=timeout,
                                        validate_only=validate)

    def delete_topics(self, topics, timeout=None):
        """
        Delete topics
        Arguments:
          topics(list): list of topic names
          timeout(int): timeout in milliseconds
        Returns:
          None.
        """
        self.kafka_client.delete_topics(topics=topics,
                                        timeout_ms=timeout)

    def create_partitions_in_topic(self, partitions, **kwargs):
        """
        create partitions in topic
        Arguments:
          partitions(list) : list of ['topic_name','num_partitions'] lists
          timeout(int): timeout in milliseconds
        Returns:
          None.
        """
        timeout = kwargs.get("timeout", None)
        validate = kwargs.get("validate", False)
        topic_partitions = {tup[0]:NewPartitions(total_count=tup[1]) for tup in partitions}
        self.kafka_client.create_partitions(topic_partitions=topic_partitions, 
                                            timeout_ms=timeout, 
                                            validate_only=validate)
