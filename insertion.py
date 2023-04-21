from flask import Flask, request, jsonify
from pymongo import MongoClient
import time

time.sleep(9)


app = Flask(__name__)

# Set up the MongoDB connection
client = MongoClient('mongodb://0.0.0.0:27017/')
db = client['student_management']
collection = db['students']

# Simple Flask route for inserting a single student record
@app.route('/insert', methods=['POST'])
def insert_student():
    data = request.json
    srn = data['srn']
    name = data['name']
    email = data['email']
    new_student = {'srn': srn, 'name': name, 'email': email}
    result = collection.insert_one(new_student)
    return jsonify({'message': 'Student added successfully.', 'id': str(result.inserted_id)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
