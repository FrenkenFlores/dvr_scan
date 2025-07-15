from flask import Blueprint, jsonify, current_app
import time

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/center/<int:camera_id>')
def get_centers(camera_id):
    width = 640
    height = 480
    speed = 100
    t = time.time()
    num_objects = 3  # Example: 3 moving objects
    objects = []
    for i in range(num_objects):
        # Offset each object in time for separation
        t_offset = t + i * 2
        period = (width * 2) / speed
        phase = (t_offset % period) / period
        if phase < 0.5:
            centerX = int(phase * 2 * width)
        else:
            centerX = int((1 - (phase - 0.5) * 2) * width)
        centerY = int(height // 2 + (i - 1) * 60)  # Spread vertically
        objects.append({'centerX': centerX, 'centerY': centerY})
    return jsonify(objects)