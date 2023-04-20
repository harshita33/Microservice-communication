import pika
from flask import Flask, request, jsonify
from pymongo import MongoClient
import json
import time

time.sleep(9)


app = Flask(__name__)

# Set up the MongoDB client
client = MongoClient("mongodb://0.0.0.0:27017/")
db = client["student_management_db"]
students_collection = db["students"]

# Set up the RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.1'))
channel = connection.channel()
channel.queue_declare(queue='insertion_queue')
channel.queue_declare(queue='deletion_queue')

# Microservice for inserting a student record
@app.route('/api/insert', methods=['POST'])
def insert_student():
    data = request.json
    result = students_collection.insert_one(data)
    return jsonify({"message": "Student record inserted successfully."})

# Microservice for retrieving all student records
@app.route('/api/read', methods=['GET'])
def read_students():
    students = []
    for student in students_collection.find():
        student['_id'] = str(student['_id'])
        students.append(student)
    return jsonify(students)

# Microservice for deleting a student record
@app.route('/api/delete', methods=['DELETE'])
def delete_student():
    srn = request.args.get('srn')
    students_collection.delete_one({"srn": srn})
    return jsonify({"message": "Student record deleted successfully."})

# Microservice for checking the health of the RabbitMQ connection
@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    if connection.is_closed:
        return jsonify({"message": "RabbitMQ connection is closed."})
    else:
        return jsonify({"message": "RabbitMQ connection is open."})

# RabbitMQ consumer for insertion messages
def callback_insert(ch, method, properties, body):
    data = json.loads(body)
    students_collection.insert_one(data)

# RabbitMQ consumer for deletion messages
def callback_delete(ch, method, properties, body):
    srn = body.decode('utf-8')
    students_collection.delete_one({"srn": srn})

# Start the RabbitMQ consumers
channel.basic_consume(queue='insertion_queue', on_message_callback=callback_insert, auto_ack=True)
channel.basic_consume(queue='deletion_queue', on_message_callback=callback_delete, auto_ack=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
