from dvr_scan.auth import login_required
from flask import Blueprint, render_template, Response, request, redirect, url_for, abort
from .camera import Camera, BOUNDARY
from .db import get_db


# The number of cameras on each page
PAGINATION = 2
bp = Blueprint("monitor", __name__, url_prefix="/monitor")


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
                'width': c['width'],
                'height': c['height'],
                'framerate': c['framerate'],
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
                width=camera_data["width"],
                height=camera_data["height"],
                framerate=camera_data["framerate"]
                pipeline=camera_data["pipeline"]
            )
        )
    elif request.method == "POST":
        return redirect(url_for("monitor.monitor_camera", camera_id=int(request.form.get("camera_id"))))


@bp.route('/video_feed/<int:camera_id>', methods=["GET"])
def video_feed(camera_id: int):
    db = get_db()
    camera_data = db.execute("SELECT * FROM camera WHERE id = :camera_id", {"camera_id": camera_id}).fetchone()
    db.close()
    if not camera_data:
        raise Exception("Error, camera is not selected")
    return Response(
        Camera(
            id=camera_data["id"],
            width=camera_data["width"],
            height=camera_data["height"],
            framerate=camera_data["framerate"],
            pipeline=camera_data["pipeline"]
        ).get_frames(),
        mimetype=f'multipart/x-mixed-replace; boundary={BOUNDARY}'
    )
