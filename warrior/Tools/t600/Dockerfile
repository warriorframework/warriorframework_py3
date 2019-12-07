From python:3.6

WORKDIR /usr/src/app

ADD app.py /usr/src/app/
ADD ne_details.py /usr/src/app/
ADD requirements.txt /usr/src/app/
ADD sample.py /usr/src/app/

RUN pip3 install -r requirements.txt

ENV FLASK_ENV development FLASK_APP /usr/src/app/app.py
CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000
