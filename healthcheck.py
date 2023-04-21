from flask import Flask, jsonify
import pika
import time

time.sleep(9)


app = Flask(__name__)

# Set up the RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.1'))

# Simple Flask route for checking the health of the RabbitMQ connection
@app.route('/healthcheck')
def healthcheck():
    if connection.is_closed:
        return jsonify({"message": "RabbitMQ connection is closed."})
    else:
        return jsonify({"message": "RabbitMQ connection is open."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
