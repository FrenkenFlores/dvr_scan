from dataclasses import dataclass
import cv2

# Boundary for multipart response
BOUNDARY = "frame"


@dataclass
class Camera:
    id: int
    width: int = 500
    height: int = 500
    pipeline: str = (
        "videotestsrc ! "
        f"video/x-raw, width={width}, height={height}, framerate=30/1 ! "
        "videoconvert ! "
        "appsink"
    )
    stream: cv2.VideoCapture = None
    def __post_init__(self):
        self.stream = cv2.VideoCapture(self.pipeline, cv2.CAP_GSTREAMER)

    def __del__(self):
        if self.stream is not None:
            self.stream.release()

    def get_frames(self):
        while True and self.stream.isOpened():
            success, frame = self.stream.read()
            if not success:
                print("Failed to read data")
                break
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield frame in MJPEG format
            yield (
                b'--' + f'{BOUNDARY}'.encode() + b'\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            )
