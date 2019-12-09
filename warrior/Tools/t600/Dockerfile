From python:3.6

WORKDIR /usr/src/app/
ADD app.py /usr/src/app/
ADD ne_details.py /usr/src/app/
ADD requirements.txt /usr/src/app/
ADD sample.py /usr/src/app/
ADD cli_data_file_template.xml .
ADD cli_test_case_template.xml .
ADD cli_test_data_template.xml .
ADD cli_var_conf_template.xml .
RUN pip3 install -r requirements.txt
ADD common_actions.py /usr/local/lib/python3.6/site-packages/warrior/Actions/CommonActions/

#Install git
# RUN apt-get update
# RUN apt-get install -y git
#
#
# RUN git clone -b feature/WAR-2271 https://github.com/warriorframework/warriorframework_py3.git

#CMD ["cp", "/usr/src/app/warriorframework_py3/warrior/Actions/CommonActions/common_actions.py", "/usr/local/lib/python3.6/site-packages/warrior/Actions/CommonActions/"]

ENV FLASK_ENV development FLASK_APP /usr/src/app/app.py
CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000





