from dvr_scan.auth import login_required
from flask import Blueprint, render_template, Response, request, redirect, url_for, jsonify
from .camera import Camera
from .db import get_db
import cv2
from .ai import MODEL_FILE, CONFIG_FILE, LABEL_FILE, ObjectsDetector
import requests
from concurrent.futures import ThreadPoolExecutor





# Boundary for multipart response
BOUNDARY = "frame"
# The number of cameras on each page
PAGINATION = 2
bp = Blueprint("monitor", __name__, url_prefix="/monitor")
object_detector = ObjectsDetector(
    model=MODEL_FILE,
    config=CONFIG_FILE,
    labels=LABEL_FILE
)
executor = ThreadPoolExecutor(max_workers=2)

@bp.route("/", methods=["GET", "POST"])
@login_required
def monitor():
    return redirect(url_for("monitor.monitor_page", page_number=1))


@bp.route("/<int:page_number>", methods=["GET", "POST"])
@login_required
def monitor_page(page_number: int):
    if request.method == "GET":
        db = get_db()
        camera_data = db.execute("SELECT * FROM camera").fetchall()
        db.close()
        cameras = [
            {
                'id': c['id'],
                'pipeline': c['pipeline']
            } for c in camera_data
        ]
        n = PAGINATION * page_number
        n_1 = n - PAGINATION
        return render_template("/monitor/panel.html", cameras=cameras[n_1:n], current_page_number=page_number, max_pages=len(cameras) // PAGINATION)
    elif request.method == "POST":
        return redirect(url_for("monitor.monitor_camera", camera_id=int(request.form.get("camera_id"))))

@bp.route("/camera/<int:camera_id>", methods=["GET", "POST"])
@login_required
def monitor_camera(camera_id: int):
    if request.method == "GET":
        db = get_db()
        camera_data = db.execute("SELECT * FROM camera WHERE id = :camera_id", {"camera_id": camera_id}).fetchone()
        db.close()
        if not camera_data:
            return render_template("error.html"), 404
        return render_template(
            "/monitor/camera.html", camera=Camera(
                id=camera_data["id"],
                pipeline=camera_data["pipeline"]
            )
        )
    elif request.method == "POST":
        return redirect(url_for("monitor.monitor_camera", camera_id=int(request.form.get("camera_id"))))


@bp.route('/events', methods=['POST'])
def send_events():
    events = request.get_json()
    if not events:
        return jsonify({'error': 'No data provided'}), 400
    db = get_db()
    # Send events to the server or process them
    for event in events:
        db.execute((
            "INSERT INTO events (camera_id, type, title, description) "
            "VALUES (:camera_id, :type, :title, :description)"
            ), {
            "camera_id": event.get("camera_id"),
            "type": event.get("type"),
            "title": event.get("title"),
            "description": event.get("description")
            }
        )
        print("INSERT")
    db.commit()
    db.close()
    return jsonify({'status': 'ok'})


def process_frames(frames_gen, camera_id, events_url, track=False):
    for frame in frames_gen:
        if track:
            try:
                events = object_detector.detect(frame, camera_id=camera_id)
                object_detector.display(frame, events)
                if events:
                    requests.post(
                        events_url,
                        json=events,
                        timeout=1
                    )
                    
            except Exception as e:
                print(f"Error processing frame: {e}")

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (
            b'--' + f'{BOUNDARY}'.encode() + b'\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )


@bp.route('/video_feed/<int:camera_id>', methods=["GET"])
def video_feed(camera_id: int):
    db = get_db()
    camera_data = db.execute("SELECT * FROM camera WHERE id = :camera_id", {"camera_id": camera_id}).fetchone()
    db.close()
    if not camera_data:
        raise Exception("Error, camera is not selected")
    c = Camera(
            id=camera_data["id"],
            pipeline=camera_data["pipeline"]
        )
    frames = process_frames(c.get_frames(), c.id, f"{request.scheme}://{request.host}{url_for('monitor.send_events')}", track=True if "videotestsrc" not in c.pipeline else False)
    return Response(
        frames,
        mimetype=f'multipart/x-mixed-replace; boundary={BOUNDARY}'
    )
