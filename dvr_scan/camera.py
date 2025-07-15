from dataclasses import dataclass
import cv2
import time
import re


# Boundary for multipart response
BOUNDARY = "frame"
MAX_RETRIES = 5


@dataclass
class Camera:
    id: int
    width: int = 640
    height: int = 480
    framerate: str = "30/1"
    pipeline: str = (
        "videotestsrc ! "
        f"video/x-raw, width={width}, height={height}, framerate={framerate} ! "
        "videoconvert ! "
        "appsink"
    )
    stream: cv2.VideoCapture = None
    def __post_init__(self):
        self.stream = cv2.VideoCapture(self.pipeline, cv2.CAP_GSTREAMER)
        if not self.stream.isOpened():  # ← Critical check!
            raise RuntimeError(f"Failed to open GStreamer pipeline: {self.pipeline}")
        # Update metadata for the custom pipelines
        self.width = int(re.search(r'width=[0-9]+', self.pipeline).group().split("=")[-1])
        self.height = int(re.search(r'height=[0-9]+', self.pipeline).group().split("=")[-1])
        self.framerate = str(re.search(r'framerate=[0-9]+/[0-9]+', self.pipeline).group().split("=")[-1])

    def __del__(self):
        if self.stream is not None:
            self.stream.release()

    def get_frames(self):
        retry_count = 0
        last_frame_time = time.time()
        while self.stream.isOpened():
        # Timeout check (1 second per frame max)
            if time.time() - last_frame_time > 1.0:
                retry_count += 1
                if retry_count >= MAX_RETRIES:
                    print("Frame timeout, restarting pipeline")
                    self._restart_pipeline()
                    retry_count = 0
                continue
            success, frame = self.stream.read()
            if not success:
                print("Frame read failed, retrying...")
                time.sleep(0.1)
                continue
            retry_count = 0
            last_frame_time = time.time()
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield frame in MJPEG format
            yield (
                b'--' + f'{BOUNDARY}'.encode() + b'\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            )
