from flask import Blueprint, jsonify, request
import zmq
from .db import get_db
import json

bp = Blueprint('api', __name__, url_prefix='/api')

# Set up ZeroMQ context and socket (REQ)
context = zmq.Context()
zmq_socket = context.socket(zmq.REQ)
zmq_socket.connect("tcp://localhost:5555")  # Change to your ZMQ endpoint

@bp.route('/center/<int:camera_id>')
def get_centers(camera_id):
    try:
        # Send camera_id as request
        zmq_socket.send_json({'camera_id': camera_id})
        # Wait for reply (with timeout)
        if zmq_socket.poll(2000):  # 2000 ms timeout
            msg = zmq_socket.recv_json()
            # Expecting a list of objects with coords
            objects = []
            db = get_db()
            for item in msg:
                coords = item.get("coords", {})
                centerX = coords.get("centerX")
                centerY = coords.get("centerY")
                if centerX is not None and centerY is not None:
                    objects.append({"centerX": centerX, "centerY": centerY})
                    db.execute((
                        "INSERT INTO events (camera_id, type, title, description) "
                        "VALUES (:camera_id, :type, :title, :description)"
                        ), {
                        "camera_id": item.get("camera_id"),
                        "type": item.get("type"),
                        "title": item.get("title"),
                        "description": item.get("description")
                        }
                    )
            db.commit()
            db.close()
            return jsonify(objects)
        else:
            return jsonify([]), 504  # Gateway Timeout
    except Exception as e:
        return jsonify([]), 502  # Bad Gateway
