#!/usr/bin/python
"""
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
"""
import traceback
import json
import warrior.WarriorCore.step_driver as step_driver
import warrior.WarriorCore.onerror_driver as onerror_driver
import warrior.WarriorCore.exec_type_driver as exec_type_driver
from warrior.Framework import Utils
from warrior.WarriorCore import common_execution_utils
from warrior.Framework.Utils.testcase_Utils import pNote, convertLogic
from warrior.Framework.Utils.print_Utils import print_info, print_warning, print_error,\
 print_normal, print_debug
from warrior.Framework.Utils.datetime_utils import wait_for_timeout
from warrior.Framework.Utils.data_Utils import getSystemData, get_object_from_datarepository,\
 update_datarepository
from warrior.Framework.ClassUtils.confluent_kafka_utils_class import WarriorConfluentKafkaConsumer,\
        WarriorConfluentKafkaProducer

"""This module is used for sequential execution of testcase steps """


def get_system_console_log(filename, logsdir, console_name):
    """Assign seperate console logfile for each system in parallel execution """

    console_logfile = Utils.file_Utils.getCustomLogFile(filename, logsdir, console_name)
    print_info("************ This is parallel execution... console logs for {0} will be logged "
               "in {1} ************".format(console_name, console_logfile))
    Utils.config_Utils.debug_file(console_logfile)
    return console_logfile


class TestCaseStepsExecutionClass:
    """ Step Execution Class """

    def __init__(self, step_list, data_repository, go_to_step_number, system_name, parallel,
                 queue, skip_invoked=True):
        """
        Constructor for testcase_steps_execution_class.

        :param step_list: List of steps
        :param data_repository: Inital data_repository
        :param go_to_step_number: go to step_number
        :param system_name: System Name
        :param parallel: parallel
        :param queue: queue
        :param skip_invoked: True by default
        """
        self.step_list = step_list
        self.data_repository = data_repository
        self.system_name = system_name
        self.parallel = parallel
        self.queue = queue
        self.skip_invoked = skip_invoked
        self.default_error_action = self.data_repository['wt_def_on_error_action']
        self.default_error_value = self.data_repository['wt_def_on_error_value']
        self.go_to_step_number = go_to_step_number
        self.kw_resultfile_list = []
        self.step_status_list = []
        self.step_impact_list = []
        self.current_step = False
        self.current_step_number = False
        self.run_current_step = False
        self.current_triggered_action = False
        self.step_status = None

    def execute_step(self, current_step_number, go_to_step_number):
        """
        This function executes the determined step - step_num (integer index) from the step_list.
        This function is called either from the while loop (normal execution) in function
        execute_steps() or from a for loop (invoked execution)
        """
        self.current_step = self.step_list[current_step_number]
        #store loop iter number in data repository
        loop_iter_number = self.current_step.get("loop_iter_number", None)
        update_datarepository({"loop_iter_number" : loop_iter_number})

        #store loop id in data repository
        loop_id = self.current_step.get("loopid", None)
        update_datarepository({"loopid" : loop_id})
        # Incrementing current_step_number for printing purposes.
        self.current_step_number = current_step_number + 1

        self.go_to_step_number = go_to_step_number
        # execute steps
        # Decide whether or not to execute keyword
        # First decide if this step should be executed in this iteration
        if not self.go_to_step_number or self.go_to_step_number == str(self.current_step_number):
            # get Exectype information
            self.run_current_step, self.current_triggered_action = \
                exec_type_driver.main(self.current_step, skip_invoked=self.skip_invoked)
            if not self.run_current_step:
                return self._report_step_as_not_run()

        if not self.go_to_step_number or self.go_to_step_number == str(self.current_step_number):
            self.step_status = self._execute_current_step()
        else:
            # Skip because of goto
            return self._skip_because_of_goto()
        runmode, value, runmode_timer = \
            common_execution_utils.get_runmode_from_xmlfile(self.current_step)
        retry_type, retry_cond, retry_cond_value, retry_value, retry_interval = \
            common_execution_utils.get_retry_from_xmlfile(self.current_step)
        if runmode is not None:
            return self._execute_runmode_step(runmode_timer, runmode, self.step_status, value)

        elif retry_type is not None:
            return self._execute_retry_type_step(retry_type, retry_cond, retry_cond_value,
                                                 retry_interval, retry_value)
        else:
            return self._execute_step_otherwise(self.step_status)

    def _report_step_as_not_run(self):
        """
        This function handles reporting of a step as not run.
        """
        keyword = self.current_step.get('Keyword')
        kw_resultfile = step_driver.get_keyword_resultfile(self.data_repository, self.system_name,
                                                           self.current_step_number, keyword)
        Utils.config_Utils.set_resultfile(kw_resultfile)
        Utils.testcase_Utils.pKeyword(keyword, self.current_step.get('Driver'))
        Utils.testcase_Utils.reportStatus('Skip')
        self.kw_resultfile_list.append(kw_resultfile)
        self.data_repository['wt_junit_object'].update_count(
            "skipped", "1", "tc", self.data_repository['wt_tc_timestamp'])
        self.data_repository['wt_junit_object'].update_count(
            "keywords", "1", "tc", self.data_repository['wt_tc_timestamp'])
        kw_start_time = Utils.datetime_utils.get_current_timestamp()
        step_impact = Utils.testcase_Utils.get_impact_from_xmlfile(self.current_step)
        impact_dict = {"IMPACT": "Impact", "NOIMPACT": "No Impact"}
        self.data_repository['wt_junit_object'].add_keyword_result(
            self.data_repository['wt_tc_timestamp'], self.current_step_number, keyword,
            "SKIPPED", kw_start_time, "0", "skipped",
            impact_dict.get(step_impact.upper()), "N/A")
        self.data_repository['step_{}_result'.format(self.current_step_number)] = "SKIPPED"
        self.go_to_step_number = False
        if self.current_triggered_action.upper() in ['ABORT', 'ABORT_AS_ERROR']:
            return self.current_step_number, self.go_to_step_number, "break"
        elif self.current_triggered_action.upper() in ['SKIP', 'NEXT']:
            return self.current_step_number, self.go_to_step_number, "continue"
        elif self.current_triggered_action == "SKIP_INVOKED":
            if self.skip_invoked:
                print_debug("Skipping this step as it is an invoked step.")
                return self.current_step_number, self.go_to_step_number, "continue"
        # when 'onError:goto' value is less than the current step num,
        # change the next iteration point to goto value
        elif self.current_triggered_action and int(self.current_triggered_action) < \
                self.current_step_number:
            self.current_step_number = int(self.current_triggered_action) - 1
        return self.current_step_number, self.go_to_step_number, "continue"

    def _execute_current_step(self):
        """
        This function actually executes a given step and returns necessary details about that step.
        """
        try:
            result = step_driver.main(self.current_step, self.current_step_number,
                                      self.data_repository, self.system_name,
                                      skip_invoked=self.skip_invoked)
            step_status = result[0]
            kw_resultfile = result[1]
            step_impact = result[2]
        except Exception as e:
            print_error('unexpected error %s' % str(e))
            step_status = False
            kw_resultfile = None
            step_impact = Utils.testcase_Utils.get_impact_from_xmlfile(self.current_step)
            print_error('unexpected error {0}'.format(traceback.format_exc()))
        self.go_to_step_number = False
        self.step_status_list, self.step_impact_list = \
            common_execution_utils.compute_status(self.current_step,
                                                  self.step_status_list,
                                                  self.step_impact_list,
                                                  step_status, step_impact)
        self.kw_resultfile_list.append(kw_resultfile)
        return step_status

    def _skip_because_of_goto(self):
        """
        This function would skip step because of goto
        """
        keyword = self.current_step.get('Keyword')
        kw_resultfile = step_driver.get_keyword_resultfile(self.data_repository, self.system_name,
                                                           self.current_step_number, keyword)
        Utils.config_Utils.set_resultfile(kw_resultfile)
        Utils.testcase_Utils.pKeyword(keyword, self.current_step.get('Driver'))
        Utils.testcase_Utils.reportStatus('Skip')

        step_description = Utils.testcase_Utils.get_description_from_xmlfile(self.current_step)
        self.kw_resultfile_list.append(kw_resultfile)
        self.data_repository['wt_junit_object'].update_count(
            "skipped", "1", "tc", self.data_repository['wt_tc_timestamp'])
        self.data_repository['wt_junit_object'].update_count(
            "keywords", "1", "tc", self.data_repository['wt_tc_timestamp'])
        kw_start_time = Utils.datetime_utils.get_current_timestamp()
        step_impact = Utils.testcase_Utils.get_impact_from_xmlfile(self.current_step)

        impact_dict = {"IMPACT": "Impact", "NOIMPACT": "No Impact"}
        self.data_repository['wt_junit_object']. \
            add_keyword_result(self.data_repository['wt_tc_timestamp'],
                               self.current_step_number, keyword, "SKIPPED",
                               kw_start_time, "0", "skipped",
                               impact_dict.get(step_impact.upper()), "N/A", step_description)
        self.data_repository['step_{}_result'.format(self.current_step_number)] = "SKIPPED"
        # print the end of runmode execution as the steps skip when the condition
        # is met for RUF/RUP
        if self.current_step.find("runmode") is not None and \
           self.current_step.find("runmode").get("attempt") is not None:
            if self.current_step.find("runmode").get("attempt") == \
               self.current_step.find("runmode").get("runmode_val"):
                print_info("\n----------------- End of Step Runmode Execution -----------------\n")
        return self.current_step_number, self.go_to_step_number, "continue"

    def _execute_runmode_step(self, runmode_timer, runmode, step_status, value):
        """
        This function will execute a runmode step
        """
        runmode_evaluation = any([runmode == "RMT",
                                  runmode == "RUF" and step_status is True,
                                  runmode == "RUP" and step_status is False])
        if runmode_timer is not None and runmode_evaluation:
            if not int(self.current_step.find("runmode").get("attempt")) == \
               int(self.current_step.find("runmode").get("runmode_val")):
                pNote("Wait for {0}sec before the next runmode attempt ".format(runmode_timer))
                wait_for_timeout(runmode_timer)
        # if runmode is 'ruf' & step_status is False, skip the repeated
        # execution of same TC step and move to next actual step
        elif runmode.upper() == "RUF" and ((step_status is True) or (step_status is False)):
            runmode_value = self.current_step.find("runmode").get("value")
            if not step_status:
                self.go_to_step_number = str(value)
                return self.current_step_number, self.go_to_step_number, "continue"
            if step_status and self.current_step_number == runmode_value - 1:
                self.go_to_step_number = onerror_driver.main(
                    self.current_step, self.default_error_action, self.default_error_value,
                    skip_invoked=self.skip_invoked, current_step_number=self.current_step_number)
                return self.current_step_number, self.go_to_step_number, "break"
        # if runmode is 'rup' & step_status is True, skip the repeated
        # execution of same TC step and move to next actual step
        elif runmode.upper() == "RUP" and step_status is True:
            self.go_to_step_number = str(value)
        else:
            if step_status is False or str(step_status).upper() in ["ERROR", "EXCEPTION"]:
                self.go_to_step_number = onerror_driver.main(
                    self.current_step, self.default_error_action, self.default_error_value,
                    skip_invoked=self.skip_invoked, current_step_number=self.current_step_number)
                if self.go_to_step_number in ['ABORT', 'ABORT_AS_ERROR']:
                    return self.current_step_number, self.go_to_step_number, "break"
                elif type(self.go_to_step_number) is list:
                    self.__run_execute_and_resume_mode()
        return self.current_step_number, self.go_to_step_number, "continue"

    def _execute_retry_type_step(self, retry_type, retry_cond, retry_cond_value, retry_interval,
                                 retry_value):
        """
        This function will execute a retry step

        """
        if retry_type.upper() == 'IF':
            try:
                if self.data_repository[retry_cond] == retry_cond_value:
                    condition_met = True
                    pNote("Wait for {0} sec before retrying".format(retry_interval))
                    pNote("The given condition '{0}' matches the expected "
                          "value '{1}'".format(self.data_repository[retry_cond], retry_cond_value))
                    wait_for_timeout(retry_interval)
                else:
                    condition_met = False
                    print_warning("The condition value '{0}' does not match with the "
                                  "expected value '{1}'".format(self.data_repository[retry_cond],
                                                                retry_cond_value))
            except KeyError:
                print_warning("The given condition '{0}' do not exists in "
                              "the data repository".format(retry_cond_value))
                condition_met = False
            if condition_met is False:
                self.go_to_step_number = str(retry_value)
        else:
            if retry_type.upper() == 'IF NOT':
                try:
                    if self.data_repository[retry_cond] != retry_cond_value:
                        condition_met = True
                        pNote("Wait for {0}sec before retrying".format(retry_interval))
                        pNote("The condition value '{0}' does not match with the expected "
                              "value '{1}'".format(self.data_repository[retry_cond],
                                                   retry_cond_value))
                        wait_for_timeout(retry_interval)
                    else:
                        condition_met = False
                except KeyError:
                    condition_met = False
                    print_warning(
                        "The given condition '{0}' is not there in the data repository".format(
                            retry_cond_value))
                if not condition_met:
                    pNote("The given condition '{0}' matched with the "
                          "value '{1}'".format(self.data_repository[retry_cond],
                                               retry_cond_value))
                    self.go_to_step_number = str(retry_value)
        return self.current_step_number, self.go_to_step_number, "continue"

    def _execute_step_otherwise(self, step_status):
        """
        This function will execute a step's onError functionality
        """
        if step_status is False or str(step_status).upper() in ["ERROR", "EXCEPTION"]:
            self.go_to_step_number = onerror_driver.main(self.current_step,
                                                         self.default_error_action,
                                                         self.default_error_value,
                                                         skip_invoked=self.skip_invoked)
            if self.go_to_step_number in ['ABORT', 'ABORT_AS_ERROR']:
                return self.current_step_number, self.go_to_step_number, "break"
            # when 'onError:goto' value is less than the current step num,
            # change the next iteration point to goto value
            elif type(self.go_to_step_number) is list:
                self.__run_execute_and_resume_mode()
            elif self.go_to_step_number and int(self.go_to_step_number) < self.current_step_number:
                self.current_step_number = int(self.go_to_step_number) - 1
                self.go_to_step_number = False
        return self.current_step_number, self.go_to_step_number, "continue"

    def __run_execute_and_resume_mode(self):
        """
        This function runs the list of step_numbers (stored in self.go_to_step_number) in the
        Invoked (execute_and_resume) mode.
        """
        print_normal("\n----------------- Starting Invoked Steps Execution -----------------\n")
        temp_step_list = list(self.step_list)
        for x in self.go_to_step_number:
            if 0 <= x < len(self.step_list):
                temp_step_list[x] = self.step_list[x]
        result = execute_steps(temp_step_list, self.data_repository, self.system_name,
                               self.parallel, self.queue, skip_invoked=False,
                               step_num=self.go_to_step_number)
        self.step_status_list.extend(result[0])
        self.kw_resultfile_list.extend(result[1])
        self.step_impact_list.extend(result[2])
        self.data_repository.update(result[3])
        self.go_to_step_number = False
        print_normal("\n----------------- Invoked Steps Execution Finished -----------------\n")

    def update_cancel_status(self):
        """
        This function updates the status with failure in case
        of user interruption
        """
        self.step_status_list.append(False)
        self.step_impact_list.append('IMPACT')
        print_error("OPERATION ABORTED BY USER !!")

class KafkaBasedExecution:
    """
    Kafka handling in case of stage execution class
    """

    def __init__(self, step_list, system_name):
        """
        Constructor

        :param step_list: List of steps
        :system_name: System name
        """

        self.datafile = Utils.config_Utils.datafile
        self.system_name = system_name
        self.step_list = step_list
        self.cleanup_stage = None

    def get_kafka_obj(self):
        """
        This function creates Kafka Consumer and Producer objects
        """
        kafka_ip = getSystemData(self.datafile, self.system_name, "ip")
        kafka_port = getSystemData(self.datafile, self.system_name, "kafka_port")
        ip_port = kafka_ip + ':' + kafka_port

        # Producer
        conf = {'bootstrap.servers' : ip_port}
        producer = WarriorConfluentKafkaProducer(conf)

        # Consumer
        conf={'bootstrap.servers' : ip_port,
              'group.id' : 'my-group',
              'auto.offset.reset' : 'latest',
              'enable.auto.commit': False}

        consumer = WarriorConfluentKafkaConsumer(conf)

        update_datarepository({"step_consumer" : consumer})
        update_datarepository({"step_producer": producer})

        return producer, consumer

    def verify_message(self, message_list):
        """
        This function validates and returns the relevant message from
        the list of kafka messages
        """
        kafka_msg_identifier = get_object_from_datarepository("kafka_msg_identifier")
        message = None

        if kafka_msg_identifier:
            for msg in message_list:
                if kafka_msg_identifier.items() <= msg.items():
                    message = msg
                    break
        else:
            message = message_list[-1]
        if message:
            print_info("Kafka message received: {0}".format(message))
            if 'action' not in message:
                print_error("Kafka message missing action key")
            do_continue = message["action"] if message["action"] else 'continue'
        else:
            print_error("Kafka messgae with {0} not found".format(kafka_msg_identifier))
            do_continue = 'continue'
        return do_continue

    def get_remarks(self, status):
        """
        This function returns remarks based on the status
        """
        to_cancel = get_object_from_datarepository("to_cancel")
        abort_msg = "Operation aborted by User"
        status_remarks = {
            'PASS': 'All OK',
            'FAIL': abort_msg if to_cancel else 'Failed',
            'ERROR': 'ERROR',
            'EXCEPTION': 'EXCEPTION'
        }

        return status_remarks.get(status, 'Stage Skipped')

    def publish_message(self, producer_inst, stage_name=None, stage_status=None):
        """
        This function publish messages to desired topic
        """
        topic_name = getSystemData(self.datafile, self.system_name, "kafka_topic")
        stage_status = "SKIPPED" if stage_status == "SKIPPED" else convertLogic(stage_status)
        msg_dict = {
            "stage_name" : stage_name,
            "status" : stage_status,
            "timestamp" : str(Utils.datetime_utils.get_current_timestamp()),
            "remarks" : self.get_remarks(stage_status)
           }
        update_datarepository({"stage_result": msg_dict})
        stage_payload = get_object_from_datarepository("stage_payload")
        if stage_payload:
            msg_dict.update(stage_payload)

        result = producer_inst.send_messages(topic_name, msg_dict)
        if not result:
            print_error("couldn't publish message to topic")
        else:
            print_info("Message Published successfully")

    def get_message(self, consumer_inst, step_num, goto_step, step=None,
                    stage_exec=False):
        """
        This function internally calls kafka utils
        to consume messages
        """
        messages = None
        do_continue = 'continue'
        to_cancel = False
        if stage_exec:
            topic_name = getSystemData(self.datafile, self.system_name, "stage_topic")
            wait_timeout_secs = step.get("wait_timeout") if step.get("wait_timeout") else 120
            wait_timeout_secs = int(wait_timeout_secs)
        else:
            topic_name = getSystemData(self.datafile, self.system_name, "step_topic")
            wait_timeout_secs = 1.0
        result = consumer_inst.subscribe_to_topics(topics=[topic_name])
        if not result:
            print_info("Cannot subscribe to topics")
        else:
            if stage_exec:
                print_info("WAITING FOR KAFKA Message")
                print_info("STAGE execution : ", step.get('stage_start'))
                print_info("If not received in {0}secs, will continue with next step "
                           "in testcase".format(wait_timeout_secs))
            messages = consumer_inst.get_messages(timeout=wait_timeout_secs,
                                                  get_all_messages=None)
            consumer_inst.kafka_consumer.commit()
        if messages:
            do_continue = self.verify_message(messages)
        else:
            if stage_exec:
                print_error("No message received from Kafka")

        if do_continue == 'skip':
            step_count = step.get("stage_step_count") if step.get("stage_step_count") else 0
            goto_step = str(step_num + step_count)
            do_continue = 'continue'
        elif do_continue == 'cancel':
            do_continue = 'break'
            to_cancel = True
            update_datarepository({"EXEC_STATUS" : "Failure"})
            update_datarepository({"FAILURE_REASON" : "OPERATION ABORTED BY USER !!"})
            update_datarepository({'to_cancel': to_cancel})
            if self.cleanup_stage:
                goto_step = str(self.cleanup_stage)
                do_continue ='continue'

        return do_continue, goto_step, to_cancel

    def get_cleanup_stage(self):
        """
        This function finds the step number for cleanup stage
        """
        for index, step in enumerate(self.step_list):
            if step.get("stage_start") == "cleanup":
                self.cleanup_stage = index + 1
                break

def execute_steps(step_list, data_repository, system_name, parallel, queue, skip_invoked=True,
                  step_num=None):
    """
        Take in a list of steps
        iterate through each of them and decide if each should run (pre-run check)
        get status and report to term and log
    """

    kafka_sys = get_object_from_datarepository("kafka_system")
    stage_begin = False
    stage_result_list = []
    stage_impact_list = []

    if parallel is True:
        system_console_log = get_system_console_log(data_repository['wt_filename'],
                                                    data_repository['wt_logsdir'],
                                                    '{0}_consoleLogs'.format(system_name))
    goto_stepnum = False
    tc_step_exec_obj = TestCaseStepsExecutionClass(step_list, data_repository, goto_stepnum,
                                                   system_name, parallel, queue,
                                                   skip_invoked=skip_invoked)

    if kafka_sys:
        kafka_obj = KafkaBasedExecution(step_list, kafka_sys)
        producer_inst, consumer_inst = kafka_obj.get_kafka_obj()
        kafka_obj.get_cleanup_stage()
        default_stage_list = get_object_from_datarepository("default_stage_list")

    if step_num is None:
        step_num = 0
        while step_num < len(step_list):
            step = step_list[step_num]
            current_step = step_num + 1
            if step.get("skip") == "yes":
                step_num = current_step
                continue

            # Kafka processing before step execution
            if kafka_sys and not goto_stepnum:
                do_continue, goto_stepnum, to_cancel = kafka_obj.get_message(consumer_inst,
                                                                             current_step,
                                                                             goto_stepnum,
                                                                             step)
                if do_continue == "break":
                    tc_step_exec_obj.update_cancel_status()
                    break

            if step.get("stage_start") and kafka_sys and not goto_stepnum:
                stage_name = step.get("stage_start")
                if stage_name not in default_stage_list:
                    stage_begin = True
                    do_continue, goto_stepnum, to_cancel = kafka_obj.get_message(consumer_inst,
                                                                                 current_step,
                                                                                 goto_stepnum,
                                                                                 step,
                                                                                 stage_exec=True)
                if do_continue == "break":
                    tc_step_exec_obj.update_cancel_status()
                    break

            step_num, goto_stepnum, do_continue = tc_step_exec_obj.execute_step(step_num,
                                                                                goto_stepnum)
            # Result processing for stage
            if stage_begin and not goto_stepnum:
                stage_result_list.append(tc_step_exec_obj.step_status_list[-1])
                stage_impact_list.append(tc_step_exec_obj.step_impact_list[-1])

            # Publishing kafka message after step execution
            if kafka_sys and step.get("stage_end"):
                if step.get("stage_end") not in default_stage_list and not to_cancel:
                    stage_status = Utils.testcase_Utils.compute_status_using_impact(
                        stage_result_list, stage_impact_list)
                    if not stage_result_list:
                        stage_status = "SKIPPED"
                    kafka_obj.publish_message(producer_inst, step.get("stage_end"), stage_status)
                    stage_begin = False
                    stage_result_list.clear()
                    stage_impact_list.clear()

                if step.get("stage_end") == 'cleanup':
                    do_continue = 'break'
                    to_cancel = get_object_from_datarepository('to_cancel')
                    if to_cancel:
                        tc_step_exec_obj.update_cancel_status()

            if do_continue == "break":
                break
        if kafka_sys:
            consumer_inst.kafka_consumer.close()
    else:
        for _step_num in step_num:
            if 0 <= _step_num < len(step_list):
                _, goto_stepnum, _ = tc_step_exec_obj.execute_step(_step_num, goto_stepnum)
            else:
                print_error("Step number {0} does not exist. Skipping.".format(_step_num+1))

    if parallel is True:
        try:
            # put result into multiprocessing queue and later retrieve in corresponding driver
            # parallel testcase sequenial keywords
            queue.put((tc_step_exec_obj.step_status_list, tc_step_exec_obj.kw_resultfile_list,
                       tc_step_exec_obj.system_name, tc_step_exec_obj.step_impact_list,
                       data_repository['wt_junit_object']))
        except Exception as e:
            print_error(e)

    else:
        if skip_invoked:
            return tc_step_exec_obj.step_status_list, tc_step_exec_obj.kw_resultfile_list, \
                   tc_step_exec_obj.step_impact_list
        else:
            return tc_step_exec_obj.step_status_list, tc_step_exec_obj.kw_resultfile_list, \
                   tc_step_exec_obj.step_impact_list, tc_step_exec_obj.data_repository


def main(step_list, data_repository, system_name=None, parallel=False, queue=False):
    """ Executes a testcase """
    steps_execution_status = execute_steps(step_list, data_repository,
                                           system_name, parallel, queue)
    return steps_execution_status
