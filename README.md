# DVR Scan


## Compile OpenCV with Gstreamer

1. install gstreamer1.0
```bash
sudo apt-get install gstreamer1.0*
sudo apt install ubuntu-restricted-extras
```

2. install lib, dev package
```bash
sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
```

3. Clone OpenCV repo
```bash
git clone https://github.com/opencv/opencv.git
cd opencv/
git checkout 4.1.0
```
4. Building
```bash
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D PYTHON_EXECUTABLE=$(which python3) \
    -D BUILD_opencv_python2=OFF \
    -D CMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") \
    -D PYTHON3_EXECUTABLE=$(which python3) \
    -D PYTHON3_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
    -D PYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
    -D WITH_GSTREAMER=ON \
    -D BUILD_EXAMPLES=ON ..
```

## virtual environment
The builded version of OpenCV is installed globally, we must allow global modules:
```bash
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements.txt
```


## Optional streaming software packages
You might want to use FFMPEG instead of GStreamer.
```
apt install ffmpeg
```

## Test the environment
```bash
pytest tests/test_system.py
```

## Usage

```bash

flask --app dvr_scan/ init-db
flask --app dvr_scan/ run -p 7777 --debug
```

## Streaming resources
1. From file.

```py
pipeline=(
    "uridecodebin uri=https://gstreamer.freedesktop.org/data/media/sintel_trailer-480p.webm ! "
    "queue ! "
    "videoscale ! "
    "video/x-raw, width=640, height=480 ! "
    "videoconvert ! "
    "appsink"
)
```
2. From webcam.

```py
pipeline=(
    "v4l2src ! "
    "video/x-raw, width=640, height=480, framerate=30/1 ! "
    "videoconvert ! "
    "appsink"
)
```
3. From MJPEG stream
```py
pipeline=(
    "souphttpsrc location=http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg ! "
    "jpegdec ! "
    "videoconvert ! "
    "appsink"
)
```
4. Test resource
```py
pipeline=(
    "videotestsrc ! "
    "video/x-raw, width=640, height=480, framerate=30/1 ! "
    "videoconvert ! "
    "appsink"
)
```
```py
pipeline=(
    "videotestsrc pattern=11 ! "
    "video/x-raw, width=640, height=480, framerate=30/1 ! "
    "videoconvert ! "
    "appsink"
)
```


## Resources
- [Compile OpenCV with Gstreamer](https://galaktyk.medium.com/how-to-build-opencv-with-gstreamer-b11668fa09c)
- [Gstreamer for computer vision playlist](https://youtube.com/playlist?list=PLOPl1qcKp6ZWYEzHXsdTV3Ct6GQXLeYGt&si=YxA18pj5e15m4ktB)