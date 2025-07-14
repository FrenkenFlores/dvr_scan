import cv2
import re


def test_gstreamer_support():
    s = cv2.getBuildInformation()
    gstreamer = re.search(r'GStreamer:.*YES', s)
    print(s)
    assert gstreamer, "❌ GStreamer is not available."


def test_gstreamer_pipeline():
    pipeline = (
        "v4l2src device=/dev/video0 ! "
        "video/x-raw, width=640, height=480, framerate=30/1 ! "
        "videoconvert ! "
        "appsink"
    )
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    assert cap.isOpened(), "❌ GStreamer pipeline failed to open."
    ret, frame = cap.read()
    assert ret, "❌ Failed to read a frame."
    assert frame is not None, "❌ Frame is None."
    assert frame.shape == (480, 640, 3), "❌ Unexpected frame shape."
