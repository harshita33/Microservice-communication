from flask import Flask, jsonify
from pymongo import MongoClient
import time

time.sleep(9)


app = Flask(__name__)

# Set up the MongoDB connection
client = MongoClient('mongodb://0.0.0.0:27017/')
db = client['student_management']
collection = db['students']

# Simple Flask route for retrieving all student records
@app.route('/read', methods=['GET'])
def read_students():
    students = []
    for student in collection.find():
        students.append({'srn': student['srn'], 'name': student['name'], 'email': student['email']})
    return jsonify({'students': students})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
