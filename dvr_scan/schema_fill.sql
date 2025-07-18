-- INSERT INTO camera (pipeline) VALUES ("videotestsrc ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! appsink");
-- INSERT INTO camera (pipeline) VALUES ("videotestsrc ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! appsink");
-- INSERT INTO camera (pipeline) VALUES ("videotestsrc ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! appsink");
-- INSERT INTO camera (pipeline) VALUES ("videotestsrc ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! appsink");
-- INSERT INTO camera (pipeline) VALUES ("videotestsrc ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! appsink");
-- INSERT INTO camera (pipeline) VALUES ("videotestsrc ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! appsink");
-- Different stream sources
-- INSERT INTO camera (pipeline) VALUES ("uridecodebin uri=https://gstreamer.freedesktop.org/data/media/sintel_trailer-480p.webm ! queue ! videoscale ! video/x-raw, width=640, height=480 ! videoconvert ! appsink");
-- INSERT INTO camera (pipeline) VALUES ("v4l2src ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! appsink");
INSERT INTO camera (pipeline) VALUES ("souphttpsrc location=http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg ! jpegdec ! videoconvert ! appsink");
