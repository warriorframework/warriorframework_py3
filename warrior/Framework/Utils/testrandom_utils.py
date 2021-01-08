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

"""This module contains functions for repetitive random testing with 
   variables in xls file"""

import os
import random
import sqlite3
import copy
import json
from itertools import product
from warrior.Framework import Utils
from warrior.Framework.Utils.print_Utils import print_info, print_warning, print_error,\
    print_debug, print_exception

try:
    import pandas as pd
except Exception as exception:
    print_exception(exception)

def update_generic_database(exec_tag, testcase_name, sample_records):
    """ update tc generic iteration results in persistent db"""
    #code to connect db and persist iteration results
    db_path = os.getenv("WAR_TOOLS_DIR") + "/generic_samples.db"
    con = sqlite3.connect(db_path)
    sql_create_table = """ CREATE TABLE IF NOT EXISTS GEN_RESULTS_TABLE (
                                        id integer PRIMARY KEY,
                                        tag text NOT NULL,
                                        testcase text NOT NULL,
                                        records text
                                    ); """
    con.execute(sql_create_table)
    records = con.execute("SELECT records from GEN_RESULTS_TABLE where tag == ? \
            and testcase == ?", (exec_tag, testcase_name, ))
    db_samples = []
    for record in records:
        db_samples.extend(json.loads(record[0]))
    if db_samples:
        for rec in sample_records:
            copy_rec = copy.deepcopy(rec)
            del copy_rec['log_file']
            del copy_rec['duration_in_seconds']
            del copy_rec['result']
            copy_rec = str(copy_rec)
            copy_rec = copy_rec.replace('{','')
            copy_rec = copy_rec.replace('}','')
            for db_rec in db_samples:
                remove_flag = True
                for field in copy_rec.split(','):
                    if field not in str(db_rec):
                        remove_flag = False
                        break
                if remove_flag:
                    db_samples.remove(db_rec)
        sample_records.extend(db_samples)
        con.execute("UPDATE GEN_RESULTS_TABLE set records=? where tag == ? and testcase == ?", \
            (json.dumps(sample_records), exec_tag, testcase_name))
    else:
        con.execute("INSERT into GEN_RESULTS_TABLE values(NULL,?,?,?)", \
            (exec_tag, testcase_name, json.dumps(sample_records)))
    con.commit()
    con.close()

def delete_samples_generic_database(exec_tag, testcase_name=None):
    """ delete existing samples of given testcase """
    db_path = os.getenv("WAR_TOOLS_DIR") + "/generic_samples.db"
    con = sqlite3.connect(db_path)
    statement = "SELECT name FROM sqlite_master WHERE type='table';"
    if ('GEN_RESULTS_TABLE',) in con.execute(statement).fetchall():
        if exec_tag and testcase_name:
            con.execute("DELETE from GEN_RESULTS_TABLE where tag == ? and \
                testcase == ?", (exec_tag, testcase_name, ))
        else:
            con.execute("DELETE from GEN_RESULTS_TABLE where tag == ?", (exec_tag, ))
        con.commit()
    con.close()

def get_samples_from_generic_db(exec_tag, testcase_name=None):
    """ get existing samples from generic db"""
    all_samples = []
    records = []
    db_path = os.getenv("WAR_TOOLS_DIR") + "/generic_samples.db"
    con = sqlite3.connect(db_path)
    statement = "SELECT name FROM sqlite_master WHERE type='table';"
    if ('GEN_RESULTS_TABLE',) in con.execute(statement).fetchall():
        if exec_tag and testcase_name:
            records = con.execute("SELECT records from GEN_RESULTS_TABLE where tag == ? \
                    and testcase == ?", (exec_tag, testcase_name, ))
        else:
            records = con.execute("SELECT records from GEN_RESULTS_TABLE where tag == ?", (exec_tag, ))
    for record in records:
        all_samples.extend(json.loads(record[0]))
    df = pd.DataFrame(all_samples)
    if not df.empty:
        df = df.drop(['log_file'], axis=1)
        df = df.drop(['duration_in_seconds'], axis=1)
        df = df.drop(['result'], axis=1)
        all_samples = df.to_dict('records')
    return all_samples

def generate_report_from_generic_db(exec_tag, testcase_name, data_repository):
    """ get existing samples from generic db"""
    all_samples = []
    records = []
    genericdatafile = data_repository.get('genericdatafile', None)
    df = pd.read_excel(genericdatafile)
    shuffle_columns = data_repository.get('gen_shuffle_columns', False)
    no_of_combinations = 1
    if shuffle_columns:
        df_dict = {}
        for column in df.columns:
            df_dict[column] = [x for x in df[column].sample(frac=1) if not pd.isnull(x)]
            no_of_combinations *= len(df_dict[column])
    else:
        #drop rows with 'ignore' set to 'yes'
        if 'ignore' in df.columns:
            df = df[df["ignore"] != "yes"]
            df = df.drop(['ignore'], axis = 1)
        no_of_combinations = len(df.index)
    db_path = os.getenv("WAR_TOOLS_DIR") + "/generic_samples.db"
    con = sqlite3.connect(db_path)
    statement = "SELECT name FROM sqlite_master WHERE type='table';"
    if ('GEN_RESULTS_TABLE',) in con.execute(statement).fetchall():
        output_dir = os.path.expanduser("~")
        if data_repository.get("xml_results_dir"):
            output_dir = data_repository["xml_results_dir"]
        elif data_repository.get("ow_resultdir"):
            output_dir = data_repository["ow_resultdir"]
        if exec_tag and testcase_name:
            file_name = "{}/{}_{}_report.xlsx".format(output_dir,\
                        exec_tag, os.path.basename(testcase_name).strip('.xml'))
            records = con.execute("SELECT records from GEN_RESULTS_TABLE where tag == ? \
                    and testcase == ?", (exec_tag, testcase_name, ))
        else:
            file_name = "{}/{}_report.xlsx".format(output_dir, exec_tag)
            records = con.execute("SELECT records from GEN_RESULTS_TABLE where tag == ?", (exec_tag, ))
    for record in records:
        all_samples.extend(json.loads(record[0]))
    writer = pd.ExcelWriter("{}".format(file_name))
    df_db = pd.DataFrame(all_samples)
    passed = 0
    failed = 0
    if len(df_db.index):
        passed = (df_db.result == 'PASS').sum()
        failed = (df_db.result == 'FAIL').sum()
    df_summary = pd.DataFrame([{"Testcase" : os.path.basename(testcase_name),
                                "Total Samples": no_of_combinations,
                                "Total Samples Executed":len(df_db.index),
                                "Passed" : passed,
                                "Failed" : failed}])
    df_summary.to_excel(writer, index=False, sheet_name='summary')
    df_db.to_excel(writer, index=False, sheet_name=os.path.basename(testcase_name))
    writer.save()
    writer.close()
    return file_name

def get_samples_shuffle_columns(df, no_of_samples, records_in_db):
    """ get samples for shuffle columns"""
    generic_data_dict = []
    all_dict = []
    df_dict = {}
    supported_combinations = 100000
    no_of_combinations = 1
    for column in df.columns:
        df_dict[column] = [x for x in df[column].sample(frac=1) if not pd.isnull(x)]
        no_of_combinations *= len(df_dict[column])
    if no_of_combinations > supported_combinations:
        print_error("Total no. of random combinations found in given xls file : {}, "
                    "max supported combinations with --select_random_values option set is {}"
                    ", please reduce column size in given variable data xls file"\
                            .format(no_of_combinations, supported_combinations))
        exit(1)
    column_names = df_dict.keys()
    column_values = df_dict.values()
    for tup in product(*column_values):
        dict1 = {}
        i = 0
        for column_name in column_names:
            dict1[column_name] = tup[i]
            i+=1
        all_dict.append(dict1)
    print_info("================================================================================")
    print_info("Total no. of combinations found in variable xls file : {}".format(len(all_dict)))
    print_info("Total no. of combinations already tested : {}".format(len(records_in_db)))
    print_info("Total no. of combinations remaining to test : {}".format(len(all_dict) - len(records_in_db)))
    print_info("Total no. of random combinations selected in this test : {}".format(no_of_samples))
    print_info("================================================================================")
    #get samples not in db.
    for db_sample in records_in_db:
        if db_sample in all_dict:
            all_dict.remove(db_sample)
    if len(all_dict) == 0:
        print_error("All the samples are tested. use --reset_execution to restart test again")
        exit(1)
    if no_of_samples <= len(all_dict):
        generic_data_dict = random.sample(all_dict, no_of_samples)
    else:
        print_error("given no_of_samples {} is greater than remaining samples to test {}." \
                    "please reduce no. of samples".format(no_of_samples, len(all_dict)))
    print_info("selected samples : {}".format(generic_data_dict))
    print_info("================================================================================")
    return generic_data_dict

def get_samples(df, selected_rows, no_of_samples, records_in_db):
    """ get samples without shuffling columns """
    df_fixed = None
    df_random = None
    generic_data_dict = []
    #drop rows with 'ignore' set to 'yes'
    if 'ignore' in df.columns:
        df = df[df["ignore"] != "yes"]
        df = df.drop(['ignore'], axis = 1)
    print_info("================================================================================")
    print_info("Total no. of samples found in variable xls file : {}".format(len(df.index)))
    print_info("Total no. of samples already tested : {}".format(len(records_in_db)))
    print_info("Total no. of samples remaining to test : {}".format(len(df.index) - len(records_in_db)))
    print_info("Total no. of random samples selected in this test : {}".format(no_of_samples))
    if selected_rows:
        print_info("Selected rows to test : {}".format(selected_rows))
    print_info("================================================================================")
    #select user selected rows
    if selected_rows:
        selected_rows = [row-1 for row in selected_rows] 
        df_fixed = df.iloc[selected_rows]
        df = df.drop(selected_rows, axis=0)
    #select records in df which are not in db_df
    db_df = pd.DataFrame(records_in_db)
    if db_df.columns.tolist():
        df = df.merge(db_df, how = 'outer' ,indicator=True).\
                loc[lambda x : x['_merge']=='left_only']
        df = df.drop(['_merge'], axis = 1)
    if no_of_samples and len(df.index) == 0:
        print_error("All the samples are tested. use --reset_execution to restart test again")
        exit(1)
    if no_of_samples and no_of_samples <= len(df.index):
        #select random samples
        df_random = df.sample(n=no_of_samples)
    elif no_of_samples and no_of_samples > len(df.index):
        print_error("Given no. of samples {} is greater than remaining samples to" \
                " test {}. please reduce no. of samples".format(no_of_samples, len(df.index)))
        exit(1)
    df = pd.concat([df_fixed, df_random])
    generic_data_dict = df.to_dict('records')
    print_info("selected samples : {}".format(generic_data_dict))
    print_info("================================================================================")
    return generic_data_dict

def get_generic_datafile(testcase_filepath, data_repository):
    """ get generic data file"""
    #First priority for generic data file through CLI
    genericdatafile = None
    if 'genericdatafile' in data_repository:
        genericdatafile = data_repository['genericdatafile']
    #Next priority is for genericdatafile in testcase details
    elif Utils.xml_Utils.nodeExists(testcase_filepath, "GenericDataFile"):
        genericdatafile = Utils.xml_Utils.getChildTextbyParentTag(testcase_filepath, \
                    'Details', 'GenericDataFile')
    if genericdatafile:
        abs_cur_dir = os.path.dirname(testcase_filepath)
        genericdatafile = Utils.file_Utils.getAbsPath(genericdatafile, abs_cur_dir)
        if not Utils.file_Utils.fileExists(genericdatafile):
            print_error("Given variables excel file path doesn't exist. Exiting !!"
                        " File path - {}".format(genericdatafile))
            exit(1)
    data_repository["genericdatafile"] = genericdatafile
    return genericdatafile

def get_iterations_from_generic_data(testcase_filepath, data_repository={}):
    """ get iterations from generic data"""
    '''genericdatafile can be passed to test by below two methods and its priority
       in order'''
    generic_data_dict = []
    genericdatafile = data_repository.get('genericdatafile', None)
    no_of_samples = data_repository.get('gen_no_of_samples', None)
    shuffle_columns = data_repository.get('gen_shuffle_columns', False)
    selected_rows = data_repository.get('gen_select_rows', None)
    purge_db = data_repository.get("gen_purge_db", None)
    exec_tag = data_repository.get("gen_exec_tag", 'default')
    gen_report = data_repository.get("gen_report", None)
    if gen_report:
        report_file = generate_report_from_generic_db(exec_tag, testcase_filepath,
                                                      data_repository)
        print_info("Report file : {}".format(report_file))
        exit(0)
    #set default random samples to 1
    if not selected_rows and not no_of_samples:
        no_of_samples = 1
    df = pd.read_excel(genericdatafile)
    if selected_rows:
        selected_rows = [int(element.strip()) for element in selected_rows.split(",")]
        invalid_index = [index for index in selected_rows if index-1 not in df.index]
        if invalid_index:
            print_error("selected rows {} not present \
                         in given xls file. please give valid comma seperated \
                         index no's in --select_rows".format(invalid_index))
            exit(1)
    #db operations
    if purge_db:
        delete_samples_generic_database(exec_tag, testcase_filepath)
    records_in_generic_db = get_samples_from_generic_db(exec_tag, testcase_filepath)
    if shuffle_columns:
        generic_data_dict = get_samples_shuffle_columns(df, no_of_samples,
                                                        records_in_generic_db)
    else:
        generic_data_dict = get_samples(df, selected_rows, no_of_samples,
                                        records_in_generic_db)
    if not generic_data_dict:
        print_warning("couldn't get samples from given xls for repetitive testing!!"
                      " Please check data in given variables excel file. Exiting!!")
        exit(1)
    gen_dict = {"gen_dict" : generic_data_dict}
    Utils.data_Utils.update_datarepository(gen_dict)
    return generic_data_dict
