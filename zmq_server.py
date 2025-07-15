# Save this as zmq_server.py and run: python zmq_server.py

import zmq
import time
import random

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("ZeroMQ server running on port 5555...")

def get_coordinates(camera_id):
    objects = []
    for i in range(3):
        objects.append({
            "type": "person",
            "time": time.time(),
            "camera_id": camera_id,
            "coords": {
                "centerX": random.randint(0, 640),
                "centerY": random.randint(0, 480)
            },
            "title": "test",
            "description": "test"
        })
    return objects


while True:
    # Wait for next request from client
    message = socket.recv_json()
    camera_id = message.get('camera_id', 0)
    # Generate random objects for demo
    objects = get_coordinates(camera_id)
    socket.send_json(objects)
