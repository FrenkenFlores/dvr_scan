from dvr_scan.auth import login_required
from flask import Blueprint, render_template, Response, request
from .camera import Camera, BOUNDARY


cameras = {
    # 0: Camera(id=0, width=640, height=480, pipeline=(
    #     "uridecodebin uri=https://gstreamer.freedesktop.org/data/media/sintel_trailer-480p.webm ! "
    #     "queue ! "
    #     "videoscale ! "
    #     "video/x-raw, width=640, height=480 ! "
    #     "videoconvert ! "
    #     "appsink"
    # )),
    # 1: Camera(id=1, width=640, height=480, pipeline=(
    #     "v4l2src ! "
    #     "video/x-raw, width=640, height=480, framerate=30/1 ! "
    #     "videoconvert ! "
    #     "appsink"
    # )),
    # 2: Camera(id=2, width=640, height=480, pipeline=(
    #     "souphttpsrc location=http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg ! "
    #     "jpegdec ! "
    #     "videoconvert ! "
    #     "appsink"
    # )),
    3: Camera(id=3, width=640, height=480, pipeline=(
        "videotestsrc pattern=0 ! "
        "video/x-raw, width=640, height=480, framerate=30/1 ! "
        "videoconvert ! "
        "appsink"
    )),
    4: Camera(id=4, width=640, height=480, pipeline=(
        "videotestsrc pattern=0 ! "
        "video/x-raw, width=640, height=480, framerate=30/1 ! "
        "videoconvert ! "
        "appsink"
    )),
    5: Camera(id=5, width=640, height=480, pipeline=(
        "videotestsrc pattern=0 ! "
        "video/x-raw, width=640, height=480, framerate=30/1 ! "
        "videoconvert ! "
        "appsink"
    )),
}

bp = Blueprint("monitor", __name__, url_prefix="/monitor")

@bp.route("/", methods=["GET"])
@login_required
def monitor():
    return render_template("/monitor/panel.html", cameras=cameras)


@bp.route('/video_feed/', methods=["GET"])
def video_feed():
    camera_id = request.args.get('camera_id', None)
    if not camera_id or int(camera_id) not in cameras:
        raise Exception("Error, camera is not selected")
    return Response(
        cameras[int(camera_id)].get_frames(),
        mimetype=f'multipart/x-mixed-replace; boundary={BOUNDARY}'
    )
