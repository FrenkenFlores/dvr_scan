from dataclasses import dataclass
import cv2
import time
import re
import random


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
        if not self.stream.isOpened():
            print(f"Failed to open GStreamer pipeline: {self.pipeline}")
            self.stream.release()
            self.width = 0
            self.height = 0
            self.framerate = ""
            self.pipeline = (
                "videotestsrc ! "
                f"video/x-raw, width={self.width}, height={self.height}, framerate={self.framerate} ! "
                "videoconvert ! "
                "appsink"
            )
            self.stream = cv2.VideoCapture(
                self.pipeline,
                cv2.CAP_GSTREAMER
            )
        # Update metadata for the custom pipelines
        if found := re.search(r'width=[0-9]+', self.pipeline):
            self.width = int(found.group().split("=")[-1])
        if found := re.search(r'height=[0-9]+', self.pipeline):
            self.height = int(found.group().split("=")[-1])
        if found := re.search(r'framerate=[0-9]+/[0-9]+', self.pipeline):
            self.framerate = str(found.group().split("=")[-1])

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
            yield frame
