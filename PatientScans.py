from flask import Flask, session, redirect, url_for, escape, request
import os 
from flask_sqlalchemy import SQLAlchemy
import datetime
import json
#import pika
#from pika.adapters.blocking_connection import BlockingConnection

message = None

app = Flask(__name__)
app.secret_key = os.urandom(25)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PatientRX_temp.db'

db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)

class Employee(db.Model):
    __table__ = db.Model.metadata.tables['Employee_Data']

class Patient(db.Model):
    __table__ = db.Model.metadata.tables['Patient_Registration']

class Vitals(db.Model):
    __table__ = db.Model.metadata.tables['Patient_Vitals']



@app.route('/api/patientscans', methods = ['GET'])
def age():
    #global message, request_channel
    print("Request for scans")
    patient_id = request.args.get('patient_id')
    #send_request(request_channel, patient_id)
    patient = Vitals.query.filter_by(patientID = patient_id).first()
    scans = patient.prescribeScan
    response = json.dumps({"scans":scans})
    print(response)
    return response, 200
   
'''
def connect():
    
    global request_channel
    cred = pika.PlainCredentials('user', 'bitnami')

    param = pika.ConnectionParameters(host = "localhost", credentials=cred)
    # host = rabbitmq server and cred = guest,guest

    connection = BlockingConnection(param)
    
    request_channel = connection.channel()
    response_channel = connection.channel()
    
    request_channel.exchange_declare(exchange = "request.tx", exchange_type='direct')
    response_channel.exchange_declare(exchange = "response.tx", exchange_type='direct')
    
    request_channel.queue_declare(queue = "requestqueue")
    response_channel.queue_declare(queue = "responsequeue")
    
    request_channel.queue_bind(queue = "requestqueue", exchange = "request.tx", routing_key = "request")
    request_channel.queue_bind(queue = "responsequeue", exchange = "response.tx", routing_key = "response")

    response_channel.basic_consume(get_patient_history, queue = "responsequeue")

def send_request(request_channel, patient_id):
    req = json.dumps({"patient_id":patient_id})
    request_channel.basic_publish(exchange = "request.tx", routing_key = "request", body = req)

def get_patient_history(channel, method, properties, body):
    global message
    message = body

'''

if __name__ == '__main__':
    #connect()
    app.run(debug=True, host='localhost', port=5000)