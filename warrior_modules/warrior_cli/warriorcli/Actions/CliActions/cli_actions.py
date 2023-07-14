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

import json
import os
import time
from warrior.Framework import Utils
from warriorcli.Utils import cli_Utils
from warrior.Framework.Utils.print_Utils import print_error, print_info, print_warning, print_debug
from warrior.Framework.Utils.testcase_Utils import pNote
from warrior.Framework.Utils.data_Utils import getSystemData, get_session_id, get_credentials
from warrior.Framework.Utils.encryption_utils import decrypt
from warrior.WarriorCore.Classes.warmock_class import mockready
from warrior.WarriorCore.Classes.war_cli_class import WarriorCliClass
from warriorcli.ClassUtils.WNetwork.warrior_cli_class import WarriorCli
from warrior.Framework.ClassUtils.confluent_kafka_utils_class import WarriorConfluentKafkaConsumer,\
        WarriorConfluentKafkaProducer, WarriorConfluentKafkaClient
"""This is the cli_actions module that has all cli related keywords """


class CliActions(object):
    """CliActions class which has methods(keywords)
    related to actions performed on any command line interface """

    def __init__(self):
        """constructor"""
        self.resultfile = Utils.config_Utils.resultfile
        self.datafile = Utils.config_Utils.datafile
        self.logsdir = Utils.config_Utils.logsdir
        self.filename = Utils.config_Utils.filename
        self.logfile = Utils.config_Utils.logfile
        self.kafka_producer_inst = None
        self.kafka_consumer_inst = None

    @mockready
    def connect(self, system_name, session_name=None, prompt=".*(%|#|\$)",
                ip_type="ip", via_host=None, tuple_pty_dimensions=None):
        """
        This is a generic connect that can connect to ssh/telnet based
        on the conn_type provided by the user in the input datafile.

        :Datafile usage:

            Tags or attributes to be used in input datafile for the system or subsystem
            If both tag and attribute is provided the attribute will be used.

            1. ip = IP address of the system.

                Default value for ip type is ip, it can take any type of ip's
                to connect to (like ipv4, ipv6, dns etc)

                Users can provide tag/attribute for any ip_type under the system
                in the input datafile and specify the tag/attribute name
                as the value for ip_type argument, then the connection will be
                established using that value.

            2. username = username for the  session.
            3. password = password for the  session.
            4. timeout = use if you want to set timeout while connecting,
                used for both ssh and telnet
            5. prompt = for ssh connections, this is the prompt expected when
                the connection is successful, not required for telnet.
            6. conn_type = the type of connection to be created (ssh/telnet).
            7. ssh_port = use this tag to provide ssh port to connect to, if
                not provided default ssh port of 22 will be used.
            8. telnet_port = use this tag to provide a telnet port to connect to
                if not provided default telnet port 23 will be used.
            9. conn_options = extra arguments that will be used when sending
                the ssh/telnet command, default is empty
            10.custom_keystroke = a keystroke that will be sent after the initial
                timeout, in case of server require a keystroke to show any prompt.
                Default is the enter key
            11.pty_dimensions = size of the pseudo-terminal specified as a
                two-entry tuple (rows, columns), eg. (24, 80).


        :Arguments:
            1. system_name (string) = This can be name of the\
                system or a subsystem.

                    To connect to a system provided system_name=system_name.

                    To connect to a single subsystem provide
                    system_name=system_name[subsystem_name].

                    To connect to multiple subsystems provide
                    system_name=system_name[subsystem1_name,subsystem2_name..etc..].

                    To connect to all subsystems under a system provide
                    system_name="system_name[all]".

            2. session_name(string) = name of the session to the system.
            3. prompt(string) = prompt expected in the terminal.
            4. ip_type(string) = type of the ip address(ip, ipv4, ipv6, dns, etc).
            5. via_host = Name of the system in the data file to be used as an
                intermediate system for establishing nested connections,
                currently it is applicable only for SSH connections.
            6. tuple_pty_pty_dimensions(tuple) = size of the pseudo-terminal specified as a
                two-entry tuple(rows, columns), eg. (24, 80).

        :Returns:
            1. status(bool)= True / False.
            2. session_id (dict element)= an id is generated for each connection
                and each connection is stored in the framework's data_repository.
                session_id=system_name+subsystem_name+session_name.
            3. response dictionary(dict): an empty dictionary to store the responses of all
                commands sent to the particular system or subsystem.
                This dictionary is available in warrior frameworks global data_repository
                and can be retrieved using the key= "session_id + _td_response".

        """

        wdesc = "Connect to the ssh/telnet port of the system"
        pNote("KEYWORD: connect | Description: {0}".format(wdesc))
        # Resolve system_name and subsystem_list
        # Removing duplicate subsystem entry and blank spaces in entry name
        system_name, subsystem_list = Utils.data_Utils.resolve_system_subsystem_list(self.datafile,
                                                                                     system_name)
        output_dict = {}
        status = True

        attempt = 1 if subsystem_list is None else len(subsystem_list)
        for i in range(attempt):
            result = False
            subsystem_name = subsystem_list[i] if subsystem_list is not None else None
            # Put system_name in system_name[subsystem] format before calling
            # connect_ssh/connect_telnet.
            call_system_name = system_name
            if subsystem_name:
                call_system_name += "[{}]".format(subsystem_name)
            conn_type = getSystemData(self.datafile, call_system_name, "conn_type")

            if conn_type is not False:
                if conn_type == "ssh":
                    result, output_dict = \
                     self.connect_ssh(call_system_name, session_name, prompt,
                                      ip_type, via_host=via_host,
                                      tuple_pty_dimensions=tuple_pty_dimensions)
                elif conn_type == "telnet":
                    result, output_dict = \
                     self.connect_telnet(call_system_name, session_name, ip_type,
                                         tuple_pty_dimensions=tuple_pty_dimensions)
                else:
                    pNote("<conn_type>={0} provided for '{1}' is  not "
                          "supported".format(conn_type, call_system_name), "error")
            else:
                pNote("conn_type not provided for system={0}".format(call_system_name), "warn")
            status = status and result
        return status, output_dict

    def connect_to_session_manager(self, system_name, kafka_system_name, tid, operation, session_name=None,
                                   wait_timeout=120):
        """
        This keyword checks whether the command can be published to the kafka topic
        to which the session manager will be listening to and can recieve the response
        by subscribing to the uniquely created kafka topic(tid_operation).

        Arguments:
            1. system_name = This can be name of the system or a subsystem.
            2. tid = This is a task id, each task will have it's own unique id.
            3. operation = operation type
            4. session_name = name of the session to the system.
            5. wait_timeout = timeout value in seconds

        Returns:
            1. status(bool) = True/False
            2. response dictionary(dict): an empty dictionary to store the responses of all
                commands sent to the particular system or subsystem.

        """

        wdesc = "Check Session manager connectivity"
        pNote(
            "KEYWORD: connect_to_session_manager | Description: {0}".format(wdesc))
        system_name, subsystem_list = Utils.data_Utils.resolve_system_subsystem_list(self.datafile,system_name)
        kafka_consumers = Utils.data_Utils.get_object_from_datarepository("kafka_consumers") or []
        output_dict = {}
        time_list = []
        status = True
        status_message = ""
        wc_obj = WarriorCli()
        session_id = get_session_id(system_name, session_name)
        output_dict[session_id] = wc_obj
        output_dict[session_id + "_td_response"] = {}
        wait_timeout_ms = int(wait_timeout)

        # We should get these parameters from payload or input data file
        # tid = Utils.data_Utils.get_object_from_datarepository("ne_data").get("tid")
        # operation = Utils.data_Utils.get_object_from_datarepository("operation")
        # kafka_send_topic = Utils.data_Utils.get_object_from_datarepository("session_mgr_kafka_topic")
        #kafka_send_topic = "SESSION-MGR"
        kafka_send_topic = os.getenv("SC_PRODUCER_TOPIC")
        kafka_receive_topic = os.getenv("SC_CONSUMER_TOPIC")
        kafka_ip = getSystemData(self.datafile, kafka_system_name, "ip")
        kafka_port = getSystemData(self.datafile, kafka_system_name, "kafka_port")
        #bootstrap_servers = ["{}:{}".format(kafka_ip, kafka_port)]
        bootstrap_servers = kafka_ip + ':' + kafka_port

        # kafka producer instance to send commands to the session manager
        conf = {'bootstrap.servers' : bootstrap_servers,
                'request.timeout.ms' : 800000,
                'api.version.request.timeout.ms' : 200000
                }
        producer = WarriorConfluentKafkaProducer(conf)

        # kafka consumer instance to receive response from session manager
        #grp = 'group' + '_' + str(int(time.time()))
        #grp = 'group' + kafka_receive_topic
        if not kafka_consumers:
            grp = 'group' + '_' + kafka_receive_topic
            client_id = 'my-client-' + str(int(time.time()))
            conf={'bootstrap.servers' : bootstrap_servers,
                  'group.id' : grp,
                  'client.id': client_id,
                  'auto.offset.reset' : 'latest',
                  'max.poll.interval.ms' : 2400000,
                  'session.timeout.ms' : 900000,
                  'debug' : 'consumer',
                  'enable.auto.commit': False}

            consumer = WarriorConfluentKafkaConsumer(conf)
        else:
            # Use the existing consumer instance
            consumer = kafka_consumers[0]

        #kafka_receive_topic = tid + "_" + operation + "_" + str(int(time.time()))
        #kafka_consumers.append(consumer)
        #Utils.data_Utils.update_datarepository({"kafka_consumers": kafka_consumers})
        output_dict[session_id + "_kafka_producer_instance"] = producer
        output_dict[session_id + "_kafka_consumer_instance"] = consumer
        output_dict[session_id + "_kafka_receive_topic"] = kafka_receive_topic
        output_dict[session_id + "_kafka_send_topic"] = kafka_send_topic
        output_dict["tid"] = tid
        output_dict["kafka_ip_port"] = "{}:{}".format(kafka_ip, kafka_port)
        Utils.data_Utils.update_datarepository(output_dict)
        command_payload = {
            "tid": tid,
            "session_validation": "true",
            "cmd": "",
            "kafka_produc_topic": kafka_receive_topic,
            "createProducer": "true"
        }

        # create kafka topic
        conf = {'bootstrap.servers' : bootstrap_servers,
                'request.timeout.ms' : 600000}
        war_kafka_client = WarriorConfluentKafkaClient(conf)
        start = int(time.time())
        topic_metadata = war_kafka_client.kafka_client.list_topics(timeout=180)
        if kafka_receive_topic not in topic_metadata.topics:
            topic_result = war_kafka_client.create_topics([[kafka_receive_topic, 1]], timeout=900)
            print_info("Topic creation call took {0} secs".format(time.time()-start))
            if topic_result:
                print_info("Topic {} created successfully".format(kafka_receive_topic))
            else:
                print_info("Failed to create Topic: {}".format(kafka_receive_topic))

        # Subscribe to the topic to listen to Session-manager responses
        if not kafka_consumers:
            result = consumer.subscribe_to_topics(topics=[kafka_receive_topic])
            kafka_consumers.append(consumer)
            Utils.data_Utils.update_datarepository({"kafka_consumers": kafka_consumers})
        else:
            # No need to subscribe again, use the existing consumer instance
            result = True

        if result:
            # Waiting for the partition assignment to happen before consuming data
            start_time = time.time()
            while True:
                partitions = consumer.kafka_consumer.assignment()
                if partitions:
                    print_info("Partitions assignment completed")
                    committed = consumer.kafka_consumer.committed(partitions, timeout=10)
                    print("Committed offsets: ",committed)
                    break
                if time.time() - start_time >= 180:
                    print_info("Partitions assignment for Topic:{0} was not completed".format(kafka_receive_topic))
                    break
                consumer.kafka_consumer.poll(0)
            print_info("Waited {0} secs for partition assignment to happen".format(time.time() - start_time))

            # Adding sleep to let all the consumer internal calls get finished
            time.sleep(5)

            # Produce message to SM
            result = producer.send_messages(kafka_send_topic, command_payload)
            if not result:
                print_error("Failed to publish command to the kafka topic: {}".format(
                kafka_send_topic))
                status_message = "Failed to publish command to the kafka topic"
                status, output_dict = False, output_dict
            else:
                print_info(
                    "Command payload successfully published to the kafka topic: {}".format(kafka_send_topic))
                print_info("Warrior will wait for {} seconds to get response from session manager".format(
                    wait_timeout_ms))
                messages = []
                messages = consumer.get_messages(timeout=wait_timeout_ms,max_records=1,
                                                 get_all_messages=None)
                if messages:
                    print_info("Response received from session manager [{}]: {}".format(int(time.time()), messages))
                    if messages[0].get("cmdRes", None) == "NE Session Inactive":
                        status_message = "NE Session Inactive"
                    if messages[0].get("status") in ["true", "True"]:
                            #and isinstance(messages[0].get("kafkaPublishTopic"), str)):
                        #kafka_send_topic = messages[0].get("kafkaPublishTopic")
                        status, output_dict = True, output_dict
                    else:
                        status, output_dict = False, output_dict
                    #consumer.kafka_consumer.commit()
                else:
                    print_info('Inside else part of get messages.')
                    #time.sleep(120)
                    res = wc_obj.verify_through_all_messages(topic=kafka_receive_topic, consumer_inst=consumer)
                    if res:
                        print_info('Response received from session manager [{}] : {}'.format(int(time.time()), res))
                        if res.get("cmdRes", None) == "NE Session Inactive":
                            status_message = "NE Session Inactive"
                        if res.get("status") in ["true", "True"]:
                                #and isinstance(res.get("kafkaPublishTopic"), str)):
                            #kafka_send_topic = res.get("kafkaPublishTopic")
                            status, output_dict = True, output_dict
                        else:
                            status, output_dict = False, output_dict
                    else:
                        print_error("No response from session manager")
                        status_message = "No response from session manager while connecting to session mgr"
                        status, output_dict = False, output_dict
                #consumer.kafka_consumer.commit()
        else:
            print_error("Can not subscribe to the topic: {}".format(kafka_receive_topic))
            status_message = "Can not subscribe to the topic"
            status, output_dict = False, output_dict

        Utils.data_Utils.update_datarepository({"FAILURE_REASON": status_message})
        Utils.data_Utils.update_datarepository(output_dict)
        return status, output_dict

    def disconnect_from_session_manager(self, system_name, session_name=None):
        """
        This keyword closes all the Kafka related instances and sends the topic name
        to Session Controller so that it can reuse the topic

        Arguments:
            1. system_name = This can be name of the system or a subsystem.
            2. session_name = name of the session to the system.

        Returns:
            1. status(bool) = True/False

        """

        wdesc = "Disconnect_from_session_manager kafka topic"
        pNote("KEYWORD: disconnect_from_session_manager | Description: {0}".format(wdesc))
        system_name, subsystem_list = Utils.data_Utils.resolve_system_subsystem_list(self.datafile,
                                                                                     system_name)
        kafka_consumers = Utils.data_Utils.get_object_from_datarepository("kafka_consumers") or []

        status = True
        producer_result = None
        session_id = get_session_id(system_name, session_name)

        producer = Utils.data_Utils.get_object_from_datarepository(session_id + "_kafka_producer_instance")

        tid = Utils.data_Utils.get_object_from_datarepository("tid")
        kafka_receive_topic = Utils.data_Utils.get_object_from_datarepository(session_id + "_kafka_receive_topic")
        kafka_send_topic = Utils.data_Utils.get_object_from_datarepository(session_id + "_kafka_send_topic")

        if kafka_consumers:
            # In case of Restore and Upgrades, where we login twice
            # We will have multiple consumers which needs to be closed
            for kafka_consumer in kafka_consumers:
                print_info("Closing Consumer instance: ")
                kafka_consumer.kafka_consumer.unsubscribe()
                kafka_consumer.kafka_consumer.poll(0)
                kafka_consumer.kafka_consumer.close()

        if producer:
            #sending message to session manager to close producer instance
            command_payload = {
                "tid": tid,
                "session_validation": "true",
                "cmd": "",
                "kafka_produc_topic": kafka_receive_topic,
                "closeProducer": "true"
            }

            producer_result = producer.send_messages(kafka_send_topic, command_payload)

            if producer_result:
                print_info(
                      "Command payload:{0} successfully published to the kafka topic: {1}".format(
                          command_payload, kafka_send_topic))
            else:
                print_info("Failed to publish command payload:{0} to the given kafka topic: {1}".format(
                    command_payload, kafka_send_topic))

            # Need to send this payload so that SC can resue this topic
            sc_topic = "SESSION_CTRL"

            command_payload = {
                    "operation": "WARRIOR",
                    "topic": kafka_receive_topic
                }

            producer_result = producer.send_messages(sc_topic, command_payload)

            if producer_result:
                print_info(
                      "Command payload:{0} successfully published to the kafka topic: {1}".format(
                          command_payload, sc_topic))
            else:
                print_info("Failed to publish command payload:{0} to the given kafka topic: {1}".format(
                    command_payload, sc_topic))

            print_info("closing producer instance")
            producer.kafka_producer.poll(0)
            producer.kafka_producer = None

        return status

    @mockready
    def disconnect(self, system_name, session_name=None):
        """ Disconnects/Closes  session established with the system

        :Arguments:
            1. system_name (string) = This can be name of the\
                system or a subsystem.

                    To connect to a system provided system_name=system_name.

                    To connect to a single subsystem provide
                    system_name=system_name[subsystem_name].

                    To connect to multiple subsystems provide
                    system_name=system_name[subsystem1_name,subsystem2_name..etc..].

                    To connect to all subsystems under a system provide
                    system_name="system_name[all]".
            2. session_name(string) = name of the session to the system

        :Returns:
            1. status(bool)= True / False
        """
        wdesc = "Disconnects/Closes  session established with the system/subsystem"
        # Resolve system_name and subsystem_list
        # Removing duplicate subsystem entry and blank spaces in entry name
        system_name, subsystem_list = Utils.data_Utils.resolve_system_subsystem_list(self.datafile,
                                                                                     system_name)
        status = True

        attempt = 1 if subsystem_list is None else len(subsystem_list)
        for i in range(attempt):
            Utils.testcase_Utils.pNote("KEYWORD: disconnect | Description: {0}".format(wdesc))
            subsystem_name = subsystem_list[i] if subsystem_list is not None else None
            call_system_name = system_name
            if subsystem_name:
                call_system_name += "[{}]".format(subsystem_name)
            Utils.testcase_Utils.pSubStep(wdesc)
            # Utils.testcase_Utils.pNote(system_name)
            # Utils.testcase_Utils.pNote(self.datafile)
            session_id = get_session_id(call_system_name, session_name)
            wc_obj = Utils.data_Utils.get_object_from_datarepository(session_id)
            msg1 = "Disconnect successful for system_name={0}, "\
                   "session_name={1}".format(system_name, session_name)
            msg2 = "Disconnection of system_name={0}, "\
                   "session_name={1} Failed".format(system_name, session_name)
            if WarriorCliClass.mock or WarriorCliClass.sim:
                result = True
            elif (isinstance(wc_obj, WarriorCli) and
                  wc_obj.conn_obj is not None and
                  wc_obj.conn_obj.target_host is not None):
                # execute smart action to produce user report
                connect_testdata = Utils.data_Utils.get_object_from_datarepository(\
                session_id+"_system",verbose=False)
                if connect_testdata is not None and connect_testdata is not False:
                    cli_Utils.smart_action(self.datafile, call_system_name, "",
                                                 wc_obj.conn_obj.target_host,
                                                 "disconnect", connect_testdata)

                wc_obj.disconnect()
                result = False if wc_obj.isalive() else True
            else:
                pNote("session does not exist", "warning")
                result = False

            msg = msg1 if result else msg2
            if not WarriorCliClass.mock and not WarriorCliClass.sim:
                Utils.testcase_Utils.pNote(msg)
            Utils.testcase_Utils.report_substep_status(result)
            status = status and result
        return status

    @mockready
    def connect_ssh(self, system_name, session_name=None, prompt=".*(%|#|\$)",
                    ip_type="ip", int_timeout=60, via_host=None,
                    tuple_pty_dimensions=None):
        """Connects to the ssh port of the the given system or subsystems

        :Datafile usage:

            Tags or attributes to be used in input datafile for the system or subsystem
            If both tag and attribute is provided the attribute will be used.

            1. ip = IP address of the system.

                Default value for ip type is ip, it can take any type of ip's
                to connect to (like ipv4, ipv6, dns etc)

                Users can provide tag/attribute for any ip_type under the system
                in the input datafile and specify the tag/attribute name
                as the value for ip_type argument, then the connection will be
                established using that value.

            2. username = username for the ssh session
            3. password = password for the ssh session
            4. timeout = use if you want to set timeout while connecting
            5. prompt = the prompt expected when the connection is successful
            6. ssh_port = use this tag to provide a ssh port to connect to,
                if not provided default ssh port 22 will be used.
            7. conn_options = extra arguments that will be used when sending
                the ssh/telnet command, default is empty
            8. custom_keystroke = a keystroke that will be sent after the initial
                timeout, in case of server require a keystroke to show any prompt.
                Default is the enter key
            9. pty_dimensions = size of the pseudo-terminal specified as a
                two-entry tuple(rows, columns), eg. (24, 80).

        :Arguments:
            1. system_name (string) = This can be name of the\
                system or a subsystem.

                    To connect to a system provided system_name=system_name.

                    To connect to a single subsystem provide
                    system_name=system_name[subsystem_name].

                    To connect to multiple subsystems provide
                    system_name=system_name[subsystem1_name,subsystem2_name..etc..].

                    To connect to all subsystems under a system provide
                    system_name="system_name[all]".
            2. session_name(string) = name of the session to the system/subsystem.
            3. prompt(string) = prompt expected in the terminal
            4. ip_type(string) = type of the ip address(ip, ipv4, ipv6, dns, etc).
            5. int_timeout(int) = use this to set timeout value for commands
                issued in this session.
            6. via_host(string) = name of the system in the data file to be
                used as an intermediate system for establishing nested ssh
                connections.
            7. tuple_pty_dimensions(tuple) = size of the pseudo-terminal specified as a
                two-entry tuple(rows, columns), eg. (24, 80).

        :Returns:
            1. status(bool)= True / False.
            2. session_id (dict element)= an id is generated for each connection
                and each connection is stored in the framework's data_repository.
                session_id=system_name+subsystem_name+session_name.
            3. response dictionary(dict): an empty dictionary to store the responses of all
                commands sent to the particular system or subsystem.
                This dictionary is available in warrior frameworks global data_repository
                and can be retrieved using the key= "session_id + _td_response".
        """
        wdesc = "Connect to the ssh port of the system/subsystem and creates a session"
        pNote("KEYWORD: connect_ssh | Description: {0}".format(wdesc))
        # Resolve system_name and subsystem_list
        # Removing duplicate subsystem entry and blank spaces in entry name
        system_name, subsystem_list = Utils.data_Utils.resolve_system_subsystem_list(self.datafile,
                                                                                     system_name)
        output_dict = {}
        status = True

        attempt = 1 if subsystem_list is None else len(subsystem_list)
        for i in range(attempt):
            Utils.testcase_Utils.pSubStep(wdesc)
            # Get name from the list when it's not 'None', otherwise, set it to 'None'
            subsystem_name = subsystem_list[i] if subsystem_list is not None else None
            call_system_name = system_name
            if subsystem_name:
                call_system_name += "[{}]".format(subsystem_name)
            credentials = get_credentials(self.datafile, call_system_name,
                                          [ip_type, 'ssh_port', 'username',
                                           'password', 'prompt', 'timeout',
                                           'conn_options', 'custom_keystroke',
                                           'escape', 'pty_dimensions'])
            # parse more things here
            pNote("system={0}, session={1}".format(call_system_name, session_name))
            session_id = get_session_id(call_system_name, session_name)
            if credentials is not None and credentials is not False:
                if not credentials["custom_keystroke"]:
                    credentials["custom_keystroke"] = "wctrl:M"
                credentials = cli_Utils.get_connection_port("ssh", credentials)
                credentials["logfile"] = Utils.file_Utils.getCustomLogFile(self.filename,
                                                                           self.logsdir,
                                                                           'ssh_%s_' % session_id)
                if not credentials["prompt"]:
                    credentials["prompt"] = prompt
                if not credentials["timeout"]:
                    credentials["timeout"] = int_timeout
                if not credentials["pty_dimensions"]:
                    credentials["pty_dimensions"] = tuple_pty_dimensions
                credentials["password"] = decrypt(credentials["password"])

                if ip_type != "ip":
                    credentials['ip'] = credentials[ip_type]
                # To get the details of the intermediate system
                if via_host is not None:
                    via_crendentials = get_credentials(self.datafile, via_host,
                                                       [ip_type, 'ssh_port',
                                                        'username', 'password',
                                                        'timeout'])
                    credentials['conn_type'] = "SSH_NESTED"
                    credentials['via_ip'] = via_crendentials[ip_type]
                    credentials['via_port'] = via_crendentials['ssh_port']
                    credentials['via_username'] = via_crendentials['username']
                    credentials['via_password'] = via_crendentials['password']
                    if via_crendentials["timeout"]:
                        credentials["via_timeout"] = int(via_crendentials["timeout"])
                    else:
                        credentials["via_timeout"] = int_timeout
                else:
                    credentials['conn_type'] = "SSH"

                # Create an object for WarriorCli class and use it to
                # establish ssh sessions
                wc_obj = WarriorCli()
                if WarriorCliClass.mock or WarriorCliClass.sim:
                    output_dict[session_id] = wc_obj
                    output_dict[session_id + "_connstring"] = ""
                    output_dict[session_id + "_td_response"] = {}
                    result = True
                else:
                    if credentials['conn_type'] == "SSH_NESTED":
                        from warriorcli.ClassUtils.WNetwork.warrior_cli_class\
                        import ParamikoConnect
                        wc_obj.conn_obj = ParamikoConnect(credentials)
                    else:
                        from warriorcli.ClassUtils.WNetwork.warrior_cli_class\
                        import PexpectConnect
                        wc_obj.conn_obj = PexpectConnect(credentials)
                    wc_obj.conn_obj.connect_ssh()

                    if wc_obj.conn_obj is not None and wc_obj.conn_obj.target_host is not None:
                        conn_string = wc_obj.conn_obj.conn_string
                        output_dict[session_id] = wc_obj
                        output_dict[session_id + "_connstring"] = conn_string.replace(b"\r\n", b"")
                        output_dict[session_id + "_td_response"] = {}
                        output_dict['connected_system'] = {"username": credentials['username'],
                                                           "password": credentials['password'],
                                                           "sysname": system_name}
                        result = True
                        pNote("Connection to system-subsystem-session={0}-{1}-{2}"
                              " is successful".format(system_name, subsystem_name, session_name))

                        # execute smart action to produce user report
                        smart_result = cli_Utils.smart_action(self.datafile,
                                                                    call_system_name, conn_string,
                                                                    wc_obj.conn_obj.target_host,
                                                                    "connect")
                        if smart_result is not None:
                            output_dict[session_id + "_system"] = smart_result

                    else:
                        result = False
                        pNote("Connection to system-subsystem-session={0}-{1}-{2}"
                              " Failed".format(system_name, subsystem_name, session_name),
                              "warning")
            else:
                result = False
            Utils.data_Utils.update_datarepository(output_dict)
            Utils.testcase_Utils.report_substep_status(result)
            status = status and result
        return status, output_dict

    @mockready
    def connect_telnet(self, system_name, session_name=None, ip_type="ip",
                       int_timeout=60, tuple_pty_dimensions=None):
        """Connects to the telnet port of the the given system and/or subsystem and creates a
        pexpect session object for the system

        A session_id is created using the combination system_name+session_name,
        system_name+subsystem+session_name and returned by this keyword to be stored
        in Warrior framework's data repository

        :Datafile usage:

            Tags or attributes to be used in input datafile for the system or subsystem
            If both tag and attribute is provided the attribute will be used.

            1. ip = IP address of the system.\

                Default value for ip type is ip, it can take any type of ip's
                to connect to (like ipv4, ipv6, dns etc)

                Users can provide tag/attribute for any ip_type under the system
                in the input datafile and specify the tag/attribute name
                as the value for ip_type argument, then the connection will be
                established using that value.

            2. username = username for the ssh session
            3. password = password for the ssh session
            4. prompt = prompt expected in the terminal
            5. timeout = use if you want to set timeout while connecting.
            6. telnet_port = use this tag to provide a telnet port to connect to,\
                if not provided default telnet port 23 will be used.
            7. conn_options = extra arguments that will be used when sending\
                the ssh/telnet command, default is empty
            8. custom_keystroke = a keystroke that will be sent after the initial\
                timeout, in case of server require a keystroke to show any prompt.
                Default is the enter key
            9. pty_dimensions = size of the pseudo-terminal specified as a
                two-entry tuple(rows, columns), eg. (24, 80).

        :Arguments:
            1. system_name (string) = This can be name of the\
                system or a subsystem.

                    To connect to a system provided system_name=system_name.

                    To connect to a single subsystem provide
                    system_name=system_name[subsystem_name].

                    To connect to multiple subsystems provide
                    system_name=system_name[subsystem1_name,subsystem2_name..etc..].

                    To connect to all subsystems under a system provide
                    system_name="system_name[all]".
            2. session_name(string) = name of the session to the system
            3. ip_type(string) = type of the ip address(ip, ipv4, ipv6, dns, etc).
            4. int_timeout(int) = use this to set timeout value for commands
                issued in this session.
            5. tuple_pty_dimensions(tuple) = size of the pseudo-terminal specified as a
                two-entry tuple(rows, columns), eg. (24, 80).

        :Returns:
            1. status(bool)= True / False.
            2. session_id (dict element)= an id is generated for each connection\
                and each connection is stored in the framework's data_repository.\
                session_id=system_name+subsystem_name+session_name
            3. response dictionary(dict): an empty dictionary to store the responses of all\
                commands sent to the particular system or subsystem.\
                This dictionary is available in warrior frameworks global data_repository\
                and can be retrieved using the key= "session_id + _td_response".

        """

        wdesc = "Connect to the telnet port of the system and creates a session"
        pNote("KEYWORD: connect_telnet | Description: {0}".format(wdesc))
        # Resolve system_name and subsystem_list
        # Removing duplicate subsystem entry and blank spaces in entry name
        system_name, subsystem_list = Utils.data_Utils.resolve_system_subsystem_list(self.datafile,
                                                                                     system_name)
        output_dict = {}
        status = True

        attempt = 1 if subsystem_list is None else len(subsystem_list)
        for i in range(attempt):
            Utils.testcase_Utils.pSubStep(wdesc)
            # Get name from the list when it's not 'None', otherwise, set it to 'None'
            subsystem_name = subsystem_list[i] if subsystem_list is not None else None
            call_system_name = system_name
            if subsystem_name:
                call_system_name += "[{}]".format(subsystem_name)
            credentials = get_credentials(self.datafile, call_system_name,
                                          [ip_type, 'telnet_port', 'username',
                                           'prompt', 'password', 'timeout',
                                           'conn_options', 'custom_keystroke',
                                           'escape', 'pty_dimensions'])
            pNote("system={0}, session={1}".format(call_system_name, session_name))
            Utils.testcase_Utils.pNote(Utils.file_Utils.getDateTime())
            session_id = get_session_id(call_system_name, session_name)
            if credentials is not None and credentials is not False:
                if not credentials["custom_keystroke"]:
                    credentials["custom_keystroke"] = "wctrl:M"
                credentials = cli_Utils.get_connection_port("telnet", credentials)
                credentials['logfile'] = Utils.file_Utils.getCustomLogFile(self.filename,\
                    self.logsdir, 'telnet_{0}_'.format(session_id))
                if not credentials["timeout"]:
                    credentials["timeout"] = int_timeout
                if not credentials["pty_dimensions"]:
                    credentials["pty_dimensions"] = tuple_pty_dimensions
                if credentials["password"]:
                    credentials["password"] = decrypt(credentials["password"])

                if ip_type != "ip":
                    credentials['ip'] = credentials[ip_type]
                credentials['conn_type'] = "TELNET"

                # Create an object for WarriorCli class and use it to
                # establish telnet sessions
                wc_obj = WarriorCli()
                if WarriorCliClass.mock or WarriorCliClass.sim:
                    output_dict[session_id] = wc_obj
                    output_dict[session_id + "_connstring"] = ""
                    output_dict[session_id + "_td_response"] = {}
                    result = True
                else:
                    from warriorcli.ClassUtils.WNetwork.warrior_cli_class\
                    import PexpectConnect
                    wc_obj.conn_obj = PexpectConnect(credentials)
                    wc_obj.conn_obj.connect_telnet()

                    if wc_obj.conn_obj is not None and wc_obj.conn_obj.target_host is not None:
                        conn_string = wc_obj.conn_obj.conn_string
                        output_dict[session_id] = wc_obj
                        output_dict[session_id + "_connstring"] = conn_string.replace(b"\r\n", b"")
                        output_dict[session_id + "_td_response"] = {}
                        result = True
                        pNote("Connection to system-subsystem-session"
                              "={0}-{1}-{2} is successful".format(system_name,
                                                                  subsystem_name, session_name))

                        # execute smart action to produce user report
                        smart_result = cli_Utils.smart_action(self.datafile,
                                                                    call_system_name,
                                                                    conn_string,
                                                                    wc_obj.conn_obj.target_host,
                                                                    "connect")
                        if smart_result is not None:
                            output_dict[session_id + "_system"] = smart_result

                    else:
                        result = False
                        pNote("Connection to system-subsystem-session"
                              "={0}-{1}-{2} Failed".format(system_name, subsystem_name,
                                                           session_name), "warning")
            else:
                result = False
            Utils.data_Utils.update_datarepository(output_dict)
            Utils.testcase_Utils.report_substep_status(result)
            status = status and result
        return status, output_dict

    @mockready
    def send_command(self, command, system_name, session_name=None,
                     start_prompt='.*', end_prompt='.*', int_timeout=60):
        """Sends a command to a system or a subsystem

        :Arguments:
            1. command(string)      = the command to be sent to the system
            2. system_name (string) = This can be name of the\
                system or a subsystem. In case of subsystem only\
                single subsystem is supported. Format for subsystem\
                is "system_name[subsystem_name]"
            3. session_name(string) = name of the session to the system
            4. start_prompt(string) = starting prompt for the command
            5. end_prompt(string) = ending prompt for the command
            6. int_timeout (integer) = timeout for the command

        :Returns:
            1. command_status(bool)
        """

        wdesc = "Send cli command to the provided system"
        pNote("KEYWORD: send_command | Description: {0}".format(wdesc))
        Utils.testcase_Utils.pSubStep(wdesc)
        # Utils.testcase_Utils.pNote(system_name)
        # Utils.testcase_Utils.pNote(self.datafile)

        session_id = Utils.data_Utils.get_session_id(system_name, session_name)
        session_object = Utils.data_Utils.get_object_from_datarepository(session_id)
        if session_object:
            if isinstance(session_object, WarriorCli):
                command_status, _ = session_object.send_command(start_prompt, end_prompt,
                                                                command, int_timeout)
            else:
                command_status, _ = cli_Utils.send_command(session_object, start_prompt,
                                                                 end_prompt, command, int_timeout)

        else:
            print_warning("%s-%s is not available for use" % (system_name, session_name))
            command_status = False

        Utils.testcase_Utils.report_substep_status(command_status)
        return command_status

    @mockready
    def send_all_testdata_commands(self, system_name, session_name=None, var_sub=None,
                                   description=None, td_tag=None, vc_tag=None):
        """
        Sends all commands from all rows that are marked execute=yes from the testdata

        This keyword expects the usage of warrior framework's
        recommended testdata xml files, sample testdata file is
        available in Warriorspace/Config_files/sample/testdata_sample.xml

        :Datafile usage:

            Tags or attributes to be used in input datafile for the system or subsystem
            If both tag and attribute is provided the attribute will be used.

            1. testdata = absolute/relative path of the testdata file.
            2. variable_config = absolute/relative path of the variable\
                                config file.

            By default the "testdata" and "variable_config" tag/attribute
            will be used to get the details of testdata and variable config file.
            If a different tag/attribute name is used, provide the tagnames
            as the value to the arguments td_tag and vc_tag.


        :Arguments:
            1. system_name (string) = This can be name of the\
                system or a subsystem. In case of subsystem only\
                single subsystem is supported. Format for subsystem\
                is "system_name[subsystem_name]"
            2. session_name(string) = name of the session to the string
            3. var_sub(string) = the pattern [var_sub] in the testdata commands,\
                                 start_prompt, end_prompt, verification search\
                                 will substituted with this value.
            4. description(string) = optional description string that overwrites the\
                                default description(wdesc) of the keyword.
                                This string will be printed as the keyword description\
                                in console logs and result files.
            5. td_tag = custom tag/attribute name of testdata file.
            6. vc_tag = custom tag/attribute name of variable conig file.

        :Returns:
            1. status(bool)
            2. response dictionary(dict): a dictionary having the responses of all\
                commands sent to the particular system or subsystem. This dictionary\
                is available in warrior frameworks global data_repository and can be\
                retrieved using the key= "session_id + _td_response" where\
                session_id="system_name+subsystem_name+session_name"
        """

        wdesc = "Send commands from rows marked execute=yes in the test data of the system"
        pNote("KEYWORD: send_all_testdata_commands | Description: {0}".format(wdesc))
        desc = wdesc if description is None else description
        return self.send_testdata_command_kw(system_name, session_name, desc,
                                             var_sub, td_tag, vc_tag)

    @mockready
    def send_commands_by_testdata_rownum(self, row_num, system_name,
                                         session_name=None, var_sub=None,
                                         description=None, td_tag=None, vc_tag=None):
        """Sends all the commands from testdata that has row equal to the
        provided row_num

        This keyword expects the usage of warrior framework's
        recommended testdata xml files, sample testdata file is
        available in Warriorspace/Config_files/sample/testdata_sample.xml

        :Datafile usage:

            Tags or attributes to be used in input datafile for the system or subsystem
            If both tag and attribute is provided the attribute will be used.

            1. testdata = absolute/relative path of the testdata file.
            2. variable_config = absolute/relative path of the variable
                                config file.

            By default the "testdata" and "variable_config" tag/attribute
            will be used to get the details of testdata and variable config file.
            If a different tag/attribute name is used, provide the tagnames
            as the value to the arguments td_tag and vc_tag.

        :Arguments:
            1. row_num (string) = row number in string representation
            2. system_name (string) = This can be name of the
                system or a subsystem. In case of subsystem only
                single subsystem is supported. Format for subsystem
                is "system_name[subsystem_name]"
            3. session_name(string) = name of the session to the string
            4. var_sub(string) = the pattern [var_sub] in the testdata commands,
                                 start_prompt, end_prompt, verification search
                                 will substituted with this value.
            5. description(string) = optional description string that overwrites the
                                default description(wdesc) of the keyword.
                                This string will be printed as the keyword description
                                in console logs and result files.
            6. td_tag = custom tag/attribute name of testdata file
            7. vc_tag = custom tag/attribute name of variable config file.

        :Returns:
            1. status(bool)
            2. response dictionary(dict): a dictionary having the responses of all
                commands sent to the particular system or subsystem. This dictionary
                is available in warrior frameworks global data_repository and can be
                retrieved using the key= "session_id + _td_response" where
                session_id="system_name+subsystem_name+session_name"
        """

        wdesc = "Send commands by row num of testdata file"
        pNote("KEYWORD: send_commands_by_testdata_rownum | Description: {0}".format(wdesc))
        desc = wdesc if description is None else description
        return self.send_testdata_command_kw(system_name, session_name,
                                             desc, var_sub, row_num=row_num,
                                             td_tag=td_tag, vc_tag=vc_tag)

    @mockready
    def send_commands_by_testdata_title(self, title, system_name, session_name=None,
                                        var_sub=None, description=None,
                                        td_tag=None, vc_tag=None):
        """Sends all the commands from testdata that has title equal to the
        provided title

        This keyword expects the usage of warrior framework's
        recommended testdata xml files, sample testdata file is
        available in Warriorspace/Config_files/sample/testdata_sample.xml

        :Datafile usage:

            Tags or attributes to be used in input datafile for the system or subsystem
            If both tag and attribute is provided the attribute will be used.

            1. testdata = absolute/relative path of the testdata file.
            2. variable_config = absolute/relative path of the variable
                                config file.

            By default the "testdata" and "variable_config" tag/attribute
            will be used to get the details of testdata and variable config file.
            If a different tag/attribute name is used, provide the tagname
            as the value to the arguments td_tag and vc_tag.

        :Arguments:
            1. title (string) = title in string representation
            2. system_name (string) = This can be name of the
                system or a subsystem. In case of subsystem only
                single subsystem is supported. Format for subsystem
                is "system_name[subsystem_name]"
            3. session_name(string) = name of the session to the string
            4. var_sub(string) = the pattern [var_sub] in the testdata commands,
                                 start_prompt, end_prompt, verification search
                                 will substituted with this value.
            5. description(string) = optional description string that overwrites the
                                default description(wdesc) of the keyword.
                                This string will be printed as the keyword description
                                in console logs and result files.
            6. td_tag = custom tag/attribute name of testdata file.
            7. vc_tag = custom tag/attribute name of variable config file.

        :Returns:
            1. status(bool)
            2. response dictionary(dict): a dictionary having the responses of all
                commands sent to the particular system or subsystem. This dictionary
                is available in warrior frameworks global data_repository and can be
                retrieved using the key= "session_id + _td_response" where
                session_id="system_name+subsystem_name+session_name"
        """

        wdesc = "Send commands by title of testdata file"
        pNote("KEYWORD: send_commands_by_testdata_title | Description: {0}".format(wdesc))
        desc = wdesc if description is None else description
        return self.send_testdata_command_kw(system_name, session_name, desc, var_sub,
                                             title=title, td_tag=td_tag, vc_tag=vc_tag)

    @mockready
    def send_commands_by_testdata_title_rownum(self, title, row_num, system_name,
                                               session_name=None, var_sub=None,
                                               description=None, td_tag=None, vc_tag=None):
        """Sends all the commands from testdata that has title/row equal to the
        provided title/row_num

        This keyword expects the usage of warrior framework's
        recommended testdata xml files, sample testdata file is
        available in Warriorspace/Config_files/sample/testdata_sample.xml

        :Datafile usage:

            Tags or attributes to be used in input datafile for the system or subsystem
            If both tag and attribute is provided the attribute will be used.

            1. testdata = absolute/relative path of the testdata file.
            2. variable_config = absolute/relative path of the variable
                                config file.

            By default the "testdata" and "variable_config" tag/attribute
            will be used to get the details of testdata and variable config file.
            If a different tag/attribute name is used, provide the tagnames
            as the value to the arguments td_tag and vc_tag.

        :Arguments:
            1. title = Title of the testdata block
            2. row = Row number of the testdata block
            3. system_name (string) = This can be name of the
                system or a subsystem. In case of subsystem only
                single subsystem is supported. Format for subsystem
                is "system_name[subsystem_name]"
            4. session_name(string) = name of the session to the string
            5. var_sub(string) = the pattern [var_sub] in the testdata commands,
                                 start_prompt, end_prompt, verification search
                                 will substituted with this value.
            6. description(string) = optional description string that overwrites the
                                default description(wdesc) of the keyword.
                                This string will be printed as the keyword description
                                in console logs and result files.
            7. td_tag = custom tag/attribute name of testdata file.
            8. vc_tag = custom tag/attribute name of variable config file.

        :Returns:
            1. status(bool)
            2. response dictionary(dict): a dictionary having the responses of all
                commands sent to the particular system or subsystem. This dictionary
                is available in warrior frameworks global data_repository and can be
                retrieved using the key= "session_id + _td_response" where
                session_id="system_name+subsystem_name+session_name"
        """
        wdesc = "Send commands by title, row & execute=yes in the test data of the system"
        pNote("KEYWORD: send_commands_by_testdata_title_rownum | Description: {0}".format(wdesc))
        desc = wdesc if description is None else description
        return self.send_testdata_command_kw(system_name, session_name,
                                             desc, var_sub, title=title, row_num=row_num,
                                             td_tag=td_tag, vc_tag=vc_tag)

    def publish_testdata_command_to_kafka(self, system_name, session_name=None, wdesc='', var_sub=None,
                                          title=None, row_num=None, td_tag=None, vc_tag=None):
        """
        Publish all the commands from testdata to kafka topic that has title equal to the
        provided title
        :Arguments:
            1. system_name (string) = name of the system in the input datafile
            2. session_name(string) = name of the session to the string
            3. wdesc(string) = Keyword description
            4. var_sub(string) = the pattern [var_sub] in the testdata commands,
                                 start_prompt, end_prompt, verification search
                                 will substituted with this value.
            5. title = title from the testdata file.
            6. row_num = row from the testdata file.
            7. td_tag = tag/attribute name of testdata file.
            8. vc_tag = tag/attribute name of variable config file.
        :Returns:
            1. status(bool)
            2. response dictionary(dict): a dictionary having the responses of all
                commands sent to the particular system or subsystem. This dictionary
                is available in warrior frameworks global data_repository and can be
                retrieved using the key= "session_id + _td_response" where
                session_id="system_name+subsystem_name+session_name"
        """
        wdesc = "publish testdata command to kafka"
        Utils.testcase_Utils.pSubStep(wdesc)
        print_debug("System Name: {0}".format(system_name))
        print_debug("Datafile: {0}".format(self.datafile))
        session_id = Utils.data_Utils.get_session_id(system_name, session_name)
        warcli_object = Utils.data_Utils.get_object_from_datarepository(
            session_id)
        testdata, varconfigfile = Utils.data_Utils.get_td_vc(self.datafile,
                                                             system_name, td_tag, vc_tag)
        status, td_resp_dict = cli_Utils.publish_commands_to_kafka_from_testdata(testdata,
                                                                                 warcli_object,
                                                                                 varconfigfile=varconfigfile,
                                                                                 var_sub=var_sub, title=title,
                                                                                 row=row_num,
                                                                                 system_name=system_name,
                                                                                 session_name=session_name,
                                                                                 datafile=self.datafile)
        Utils.testcase_Utils.report_substep_status(status)
        return status, td_resp_dict

    @mockready
    def send_testdata_command_kw(self, system_name, session_name=None, wdesc='', var_sub=None,
                                 title=None, row_num=None, td_tag=None, vc_tag=None):
        """
        UseAsKeyword=No
        - This will not be listed as a keyword in Katana

        :Arguments:
            1. system_name (string) = name of the system in the input datafile
            2. session_name(string) = name of the session to the string
            3. wdesc(string) = Keyword description
            4. var_sub(string) = the pattern [var_sub] in the testdata commands,
                                 start_prompt, end_prompt, verification search
                                 will substituted with this value.
            5. title = title from the testdata file.
            6. row_num = row from the testdata file.
            7. td_tag = tag/attribute name of testdata file.
            8. vc_tag = tag/attribute name of variable config file.
        :Returns:
            1. status(bool)
            2. response dictionary(dict): a dictionary having the responses of all
                commands sent to the particular system or subsystem. This dictionary
                is available in warrior frameworks global data_repository and can be
                retrieved using the key= "session_id + _td_response" where
                session_id="system_name+subsystem_name+session_name"
        """
        wdesc = "send testdata command kw"
        Utils.testcase_Utils.pSubStep(wdesc)
        print_debug("System Name: {0}".format(system_name))
        print_debug("Datafile: {0}".format(self.datafile))
        session_id = Utils.data_Utils.get_session_id(system_name, session_name)
        session_object = Utils.data_Utils.get_object_from_datarepository(session_id)
        testdata, varconfigfile = Utils.data_Utils.get_td_vc(self.datafile,
                                                             system_name, td_tag, vc_tag)
        status, td_resp_dict = cli_Utils.send_commands_from_testdata(testdata,
                                                                     session_object,
                                                                     varconfigfile=varconfigfile,
                                                                     var_sub=var_sub, title=title,
                                                                     row=row_num,
                                                                     system_name=system_name,
                                                                     session_name=session_name,
                                                                     datafile=self.datafile)

        Utils.testcase_Utils.report_substep_status(status)
        return status, td_resp_dict

    def set_session_timeout(self, system_name, session_name=None, int_timeout=30):
        """Sets the timeout period for the ssh/telnet session

        :Arguments:
            1. system_name(string-mandatory)      = name of the system from the input datafile
            2. session_name(string)               = name of the session to the system
            3. int_timeout(integer)               = timeout value in minutes

        :Returns:
            1. status(bool)
        """

        wdesc = "Sets the timeout period for the ssh/telnet session"
        pNote("KEYWORD: set_session_timeout | Description: {0}".format(wdesc))
        status = True
        Utils.testcase_Utils.pSubStep(wdesc)
        # Utils.testcase_Utils.pNote(system_name)
        # Utils.testcase_Utils.pNote(self.datafile)
        session_id = Utils.data_Utils.get_session_id(system_name, session_name)
        session_object = Utils.data_Utils.get_object_from_datarepository(session_id)

        if session_object.isalive():
            session_object.timeout = int_timeout
            Utils.testcase_Utils.pNote("Timeout value is set to {0}mins for the session "
                                       "with system name : {1}, session name : "
                                       "{2}".format(int_timeout, system_name, session_name))
        else:
            status = False
            Utils.testcase_Utils.pNote("Session with system name : {0}, session name : {1}"
                                       " is timedout/closed".format(system_name, session_name))
        return status

    def verify_session_status(self, system_name, session_name=None):
        """Checks whether the ssh/telnet session is alive or not

        :Arguments:
            1. system_name(string-mandatory)      = name of the system from the input datafile
            2. session_name(string)               = name of the session to the system

        :Returns:
            1. status(bool) : True if alive, False if not alive
        """

        wdesc = "Checks whether the ssh/telnet session is alive or not"
        pNote("KEYWORD: verify_session_status | Description: {0}".format(wdesc))
        status = True
        Utils.testcase_Utils.pSubStep(wdesc)
        # Utils.testcase_Utils.pNote(system_name)
        # Utils.testcase_Utils.pNote(self.datafile)
        session_id = Utils.data_Utils.get_session_id(system_name, session_name)
        session_object = Utils.data_Utils.get_object_from_datarepository(session_id)

        if session_object.isalive():
            Utils.testcase_Utils.pNote("Session with system name : {0}, session name : {1}"
                                       " is alive".format(system_name, session_name))
        else:
            status = False
            Utils.testcase_Utils.pNote("Session with system name : {0}, session name : {1}"
                                       " is not alive".format(system_name, session_name))
        return status

    @mockready
    def connect_all(self):
        """This is a connect all operation that can connect to  all ssh/telnet based
        on the conn_type provided by the user in the input datafile.

        :Datafile usage:

            Tags or attributes to be used in input datafile for the system or subsystem
            If both tag and attribute is provided the attribute will be used.

            1. ip = IP address of the system.\

                Default value for ip type is ip, it can take any type of ip's
                to connect to (like ipv4, ipv6, dns etc)

                Users can provide tag/attribute for any ip_type under the system
                in the input datafile and specify the tag/attribute name
                as the value for ip_type argument, then the connection will be
                established using that value.

            2. username = username for the  session.
            3. password = password for the  session.
            4. timeout = use if you want to set timeout while connecting,\
                used for both ssh and telnet
            5. prompt = for ssh connections, this is the prompt expected when\
                the connection is successful, not required for telnet.
            6. conn_type = the type of connection to be created (ssh/telnet).
            7. ssh_port = use this tag to provide ssh port to connect to, if\
                not provided default ssh port of 22 will be used.
            8. telnet_port = use this tag to provide a telnet port to connect to\
                if not provided default telnet port 23 will be used.


        :Arguments:
            None. Keyword will read the input datafile and get the data from
            tag <system> and <subsystem>.

        :Returns:
            1. status(bool)= True / False.
            2. session_id (dict element)= an id is generated for each connection
                and each connection is stored in the framework's data_repository.
                session_id=system_name+subsystem_name+session_name.
            3. response dictionary(dict): an empty dictionary to store the responses of all
                commands sent to the particular system or subsystem.
                This dictionary is available in warrior frameworks global data_repository
                and can be retrieved using the key= "session_id + _td_response".
        """
        wdesc = "Connect to all systems and subsystems in the datafile."
        pNote("KEYWORD: connect_all | Description: {0}".format(wdesc))

        output_dict = {}
        status = True

        root = Utils.xml_Utils.getRoot(self.datafile)
        systems = root.findall('system')
        system_list = []
        for system in systems:
            # check if the system has subsystem or not.
            subsystems = system.findall('subsystem')
            if subsystems != []:
                for subsystem in subsystems:
                    subsystem_name = subsystem.get('name')
                    system_name = system.get('name') + '[' + subsystem_name + ']'
                    system_list.append(system_name)
            # if there is no subsystem use the system.
            else:
                system_name = system.get('name')
                system_list.append(system_name)

        for system_name in system_list:
            sys_status, sys_dict = self.connect(system_name)
            status = status and sys_status
            output_dict.update(sys_dict)
        return status, output_dict

    @mockready
    def disconnect_all(self):
        """This is a disconnect all operation that can disconnect all ssh/telnet sessions
        based on the details provided by the user in the input datafile.

        :Arguments:
            None. Keyword will read the input datafile and get the data from
            tag <system> and <subsystem>.

        :Returns:
            1. status(bool)= True / False.
        """
        wdesc = "Disconnect all systems and subsystems in the datafile."
        pNote("KEYWORD: disconnect_all | Description: {0}".format(wdesc))
        status = True
        root = Utils.xml_Utils.getRoot(self.datafile)
        systems = root.findall('system')
        system_list = []
        for system in systems:
            # check if the system has subsystem or not.
            subsystems = system.findall('subsystem')
            if subsystems != []:
                for subsystem in subsystems:
                    subsystem_name = subsystem.get('name')
                    system_name = system.get('name') + '[' + subsystem_name + ']'
                    system_list.append(system_name)
            # if there is no subsystem use the system.
            else:
                system_name = system.get('name')
                system_list.append(system_name)

        for system_name in system_list:
            sys_status = self.disconnect(system_name)
            status = status and sys_status
        return status

