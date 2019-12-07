# This is a basic REST micro service example for python using the flask library
# Docs: http://flask.pocoo.org/docs/1.0/
import re
import time
import os
import glob
import json
from flask import Flask, jsonify, request
from ne_details import nes
from func_timeout import func_timeout, FunctionTimedOut

app = Flask(__name__)


# ----------------
# Sample REST APIs
# ----------------


@app.route('/', methods=['GET'])
def index():
    return 'REST Service for Warrior FW is up and running...'

# Get a list of resources
@app.route('/nes', methods=['GET'])
def get_ne_details():
    return jsonify(list(nes.values()))


# Get a single resource
@app.route('/nes/<ne_id>', methods=['GET'])
def find_single_ne(ne_id):
    if ne_id not in nes:
        return '', 404
    return jsonify(nes[ne_id])



@app.route('/set', methods=['POST'])
def set():
    #os.chdir("/usr/src/app/")
    #Process data
    data = request.json
    import json
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

    # creating necessary files and running the test case
    status = os.system("python sample.py data.json set ")
    if status != 0:
       return jsonify({"SCRIPT_STATUS":"FAIL"}), 200
      
    return_data = process_logs()

    if return_data["script_status"] == "PASS":
        return jsonify(return_data), 200
    elif return_data["script_status"] == "FAIL":
        return jsonify(return_data), 200
    else:
        print('Execute failed...')
        return 'Error Message', 500

@app.route('/measure', methods=['POST'])
def measure():
    #os.chdir("/usr/src/app/")
    #Process data
    data = request.json
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

    # creating necessary files and running the test case
    os.system("python sample.py data.json measure")
    return_data = process_logs()

    if return_data["script_status"] == "PASS":
        return jsonify(return_data), 200
    elif return_data["script_status"] == "FAIL":
        return jsonify(return_data), 200
    else:
        print('Execute failed...')
        return 'Error Message', 500

def process_logs():
    if os.environ.get("HOME"):
        home_path = os.environ["HOME"]
        exe_dir = "Warriorspace/Execution"

        logs_dir = os.path.join(home_path, exe_dir)
        act_path = os.path.join(logs_dir, "*")
        list_of_files = glob.glob(act_path)
        logs_dir_full = max(list_of_files, key=os.path.getctime)
        log_file_name = os.path.split(logs_dir_full)[-1]
        final_path = os.path.join(logs_dir_full, "Logs")

        #os.chdir(final_path)
        print(final_path, log_file_name)
        tc_name = "cli_test_case_template"
        file_desc = open(os.path.join(final_path, "{}_consoleLogs.log".format(tc_name)))

        #file_desc = (open("{}_consoleLogs.log".format(tc_name)))
        file_content = file_desc.read()
        import re
        match = re.search("TESTCASE\:{}\s*STATUS\:(PASS|FAIL)".format(tc_name), file_content)
        #print(match)
        result = {}
        result.update({"script_status" : match.group(1)})
        #print(result)
        with open('data.txt', 'w') as outfile:
            json.dump(result, outfile)
        print("The location of result file {}".format(os.path.join(os.getcwd(), "data.txt")))
        return result

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    print(data)
    # process the data

    response_object = data

    success = True

    # return status code and response
    if success:
        return jsonify(response_object), 200
    else:
        print('Execute failed...')
        return 'Error Message', 500



@app.route('/execute1', methods=['POST'])
def execute1():
    data = request.json
    print(data)
    # process the data

    response_object = data

    try:
        helloReturn = func_timeout(5, hello, args=('5'))

    except FunctionTimedOut:
        response_object = "Timed out"

    success = True

    # return status code and response
    if success:
        return jsonify(response_object), 200
    else:
        print('Execute failed...')
        return 'Error Message', 500

def hello(x):
    print(x, " is the timeout..")
    time.sleep(6)
    return 'Hello World'
app.run(host="0.0.0.0", port=5002)
