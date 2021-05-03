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


from pymongo import MongoClient
from warrior.Framework.Utils.print_Utils import print_info, print_error
import warrior.Framework.Utils as Utils
from warrior.Framework.Utils.data_Utils import get_object_from_datarepository, update_datarepository
from warrior.Framework.Utils.data_Utils import getSystemData

class MongoActions(object):
    def __init__(self):
        """
            Set defaults for MySqlActions.
        """
        self.resultfile = Utils.config_Utils.resultfile
        self.datafile = Utils.config_Utils.datafile
        self.logsdir = Utils.config_Utils.logsdir
        self.filename = Utils.config_Utils.filename

    def update_mongo_db(self, system_name, collection, update_json=None, filter_json=None):
        '''
            Update or Insert doc in Mongo db collection
        '''
        wdesc = "Update or Insert doc in Mongo db collection"
        status, output, dictionary = False, {}, {}
        try:
            #mongo parameters
            host = getSystemData(self.datafile, system_name, "ip")
            port = getSystemData(self.datafile, system_name, "port")
            database = getSystemData(self.datafile, system_name, "db")
            #username = getSystemData(self.datafile, system_name, "username")
            #password = getSystemData(self.datafile, system_name, "password")
            collection = get_object_from_datarepository(collection)
            client = MongoClient(host, int(port))
            db = client[database]
            col = db[collection]
            if update_json and filter_json:
                update_json = get_object_from_datarepository(update_json)
                filter_json = get_object_from_datarepository(filter_json)
                updated_doc = col.find_one(filter_json)
                if not updated_doc:
                    print_error("no doc matched the given filter '{}' in collection '{}'".format(filter_json, collection))
                else:
                    result = col.update_one(filter_json, update_json)
                    if result:
                        print_info('successfully updated doc in mongo db collection : {}'.format(collection))
                        updated_doc = col.find_one(filter_json)
                        print_info("updated doc : {}".format(updated_doc))
                        status = True
                    else:
                        print_error('cannot update doc in mongo db')
            elif update_json and not filter_json:
                update_json = get_object_from_datarepository(update_json)
                result = col.insert_one(update_json)
                if result:
                    status = True
                    print_info('successfully updated mongo db collection : {}, _id : {}'.format(collection, result.inserted_id))
                else:
                    print_error('cannot insert doc in mongo db')
            elif not update_json and filter_json:
                filter_json = get_object_from_datarepository(filter_json)
                result = col.find_one(filter_json)
                if result:
                    status = True
                    print_info('successfully found doc with fiven filter')
                else:
                    print_error('cannot find doc in mongo db')
            else:
                print_error('atleast one of update_doc or filter_doc are mandatory')
        except Exception as err:
            print_error("ERROR: error while updating db: {}".format(err))
            update_datarepository({"error_description":'Error while updating mongo db'})
        return status, output
