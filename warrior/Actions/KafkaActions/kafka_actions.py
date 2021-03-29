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
import time
from json import loads, dumps
from warrior.Framework import Utils
from warrior.Framework.Utils.print_Utils import print_error, print_info
from warrior.Framework.Utils.testcase_Utils import pNote
from warrior.Framework.Utils.data_Utils import getSystemData
from warrior.Framework.ClassUtils.kafka_utils_class import WarriorKafkaProducer,\
    WarriorKafkaConsumer
from warrior.Framework.Utils.config_Utils import data_repository
from configobj import ConfigObj

"""This is the kafka_actions module that has kafka keywords """


class KafkaActions():
    """KafkaActions class which has methods(keywords)
       related to actions performed for kafka"""

    def __init__(self):
        """constructor"""
        self.resultfile = Utils.config_Utils.resultfile
        self.datafile = Utils.config_Utils.datafile
        self.logsdir = Utils.config_Utils.logsdir
        self.filename = Utils.config_Utils.filename
        self.logfile = Utils.config_Utils.logfile

    def send_messages(self, system_name, topic, value,
                      partition=None, headers=None, timestamp=None, key=None):
        """
        This keyword publishes messages to the topic in given kafka broker

        Input data file Usage:
        <credentials>
            <system name="kafka_server1" type="kafka_producer">
                <ip>localhost</ip>
                <kafka_port>9092</kafka_port>
            </system>
        </credentials>

        For complete list of supported parameters, check
        https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html

        :Arguments:
           1.system_name(string) : kafka broker system name in input data file
           2.topic(string) : topic name to publish message
           3.value(string) : message to publish
           4.partition(int) : partition number, Optional
           5.headers(list) : list of headers
           6.timestamp(string) : timestamp
           5.key(string) : key for the message, Optional
        :Returns:
           1.status(bool) : True if message is published, else False

        """
        wdesc = "publish value {} to topic {} in kafka broker {}".format(system_name, topic, value)
        pNote("KEYWORD: send_messages | Description: {0}".format(wdesc))
        status = True
        if not data_repository.get("kafka_producer", None):
            print_info("creating kafka producer")
            # mapper file will be available for netconf backup
            map_file = data_repository.get('wt_mapfile', None)
            if map_file:
                ca_file = key_file = crl_file= ciphers = None
                config = ConfigObj(map_file)
                mapper = config.get('CREDENTIALS', None).get('kafka_server', None) if config.get('CREDENTIALS', None) else None
                if not mapper:
                    return False
                status, mapper_data = Utils.data_Utils.replace_var(mapper, {}, {})
                if not status:
                    return status
                kafka_ip = config["CREDENTIALS"]["kafka_server"].get("kafka_host", None)
                kafka_port = config["CREDENTIALS"]["kafka_server"].get("kafka_port", None)
                ca_file = config["CREDENTIALS"]["kafka_server"].get("ca_file", None)
                key_file = config["CREDENTIALS"]["kafka_server"].get("key_file", None)
                crl_file = config["CREDENTIALS"]["kafka_server"].get("crl_file", None)
                ciphers = config["CREDENTIALS"]["kafka_server"].get("ciphers", None)
            else:
                kafka_ip = getSystemData(self.datafile, system_name, "ip")
                kafka_port = getSystemData(self.datafile, system_name, "kafka_port")
                ca_file = getSystemData(self.datafile, system_name, "ssl_cafile")
                key_file = getSystemData(self.datafile, system_name, "ssl_keyfile")
                crl_file = getSystemData(self.datafile, system_name, "ssl_crlfile")
                ciphers = getSystemData(self.datafile, system_name, "ssl_ciphers")
            if not kafka_ip or not kafka_port:
                status = False
                print_error("ip, kafka_port should be provided")
                return status
            self.kafka_obj_producer = WarriorKafkaProducer(bootstrap_servers=\
                                                             [kafka_ip+":"+kafka_port],
                                                           acks='all',
                                                           request_timeout_ms=1000000,
                                                           api_version_auto_timeout_ms=1000000,
                                                           ssl_cafile=ca_file,
                                                           ssl_keyfile=key_file,
                                                           ssl_crlfile=crl_file,
                                                           ssl_ciphers=ciphers,
                                                           value_serializer=\
                                                             lambda x: dumps(x).encode('utf-8'))
        else:
            self.kafka_obj_producer = data_repository["kafka_producer"]

        # handling string and dict as input
        try:
            value = eval(value)
        except:
            value = value

        if not hasattr(self.kafka_obj_producer, "kafka_producer"):
            print_error("couldn't create connection to the kafka broker")
            result = False
            status = status and result
        else:
            data_repository["kafka_producer"] = self.kafka_obj_producer
            result = self.kafka_obj_producer.send_messages(topic=topic,
                                                           value=value,
                                                           partition=partition,
                                                           headers=headers,
                                                           timestamp=timestamp,
                                                           key=key)
            if not result:
                print_error("couldn't publish message to topic")
            status = status and result
        return status

    def get_messages(self, system_name, list_topics, group_id='my-group',
                     timeout=100, list_patterns=None,
                     max_records=None, get_all_messages=False):
        """
        This keyword gets the messages published to the specified topics

        Input data file Usage:
        <credentials>
            <system name="kafka_server1" type="kafka_consumer">
                <ip>localhost</ip>
                <kafka_port>9092</kafka_port>
            </system>
        </credentials>

        For complete list of supported parameters, check
        https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html

        :Arguments:
          1.system_name(string) : kafka broker system name in inputdata file.
          2.list_topics(list) : list of topics to subscribe.
          3.group_id(string) : group id to use for subscription.
          4.timeout(int) : timeout in milliseconds.
          5.list_patterns(list) : list of patterns of topic names.
          6.max_records(int) : maximum records to fetch
          7.get_all_messages(bool) : True to fetch all messages in topic

        :Returns:
          1.status(bool) : True if messages are fetched successfully, else False
          2.output_dict : list of messages

        """
        wdesc = "get messages subscribed to topics : {}".format(list_topics)
        pNote("KEYWORD: get_messages | Description: {0}".format(wdesc))
        status = True
        output_dict = {}
        if not data_repository.get("kafka_consumer", None):
            print_info("creating kafka consumer")
            kafka_ip = getSystemData(self.datafile, system_name, "ip")
            kafka_port = getSystemData(self.datafile, system_name, "kafka_port")
            ca_file = getSystemData(self.datafile, system_name, "ssl_cafile")
            key_file = getSystemData(self.datafile, system_name, "ssl_keyfile")
            crl_file = getSystemData(self.datafile, system_name, "ssl_crlfile")
            ciphers = getSystemData(self.datafile, system_name, "ssl_ciphers")
            if not kafka_ip or not kafka_port:
                status = False
                print_error("ip, kafka_port should be provided")
                return status
            self.kafka_obj_consumer = WarriorKafkaConsumer(bootstrap_servers=\
                                                            [kafka_ip+":"+kafka_port],
                                                           ssl_cafile=ca_file,
                                                           ssl_keyfile=key_file,
                                                           ssl_crlfile=crl_file,
                                                           ssl_ciphers=ciphers,
                                                           group_id=group_id,
                                                           auto_offset_reset='earliest',
                                                           value_deserializer=\
                                                             lambda x: loads(x.decode('utf-8')))
        else:
            self.kafka_obj_consumer = data_repository["kafka_consumer"]

        if not hasattr(self.kafka_obj_consumer, "kafka_consumer"):
            print_error("couldn't create connection to the kafka broker")
            result = False
            status = status and result
        else:
            data_repository["kafka_consumer"] = self.kafka_obj_consumer
            subscribe_required = False
            assigned_topics = self.kafka_obj_consumer.get_topics()
            if not assigned_topics:
                subscribe_required = True
            else:
                for topic in list_topics:
                    if topic not in str(assigned_topics):
                        subscribe_required = True
            if subscribe_required:
                result = self.kafka_obj_consumer.subscribe_to_topics(topics=list_topics,
                                                                     pattern=list_patterns)
                if not result:
                    print_error("cannot subscribe to topics")
                    status = status and result
            if status:
                messages = self.kafka_obj_consumer.get_messages(timeout=timeout,
                                                                max_records=max_records,
                                                                get_all_messages=get_all_messages)
                print_info("messages received from subscribed topics {}".format(messages))
            if messages:
                time_stamp = int(time.time())
                output_dict["kafka_messages_{}".format(time_stamp)] = messages
        return status, output_dict

