from flask import Flask, jsonify
from pymongo import MongoClient
import time

time.sleep(9)


app = Flask(__name__)

# Set up the MongoDB connection
client = MongoClient('mongodb://0.0.0.0:27017/')
db = client['student_management']
collection = db['students']

# Simple Flask route for deleting a single student record
@app.route('/delete/<srn>', methods=['DELETE'])
def delete_student(srn):
    result = collection.delete_one({'srn': srn})
    if result.deleted_count == 1:
        return jsonify({'message': 'Student deleted successfully.'})
    else:
        return jsonify({'message': 'Student not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
