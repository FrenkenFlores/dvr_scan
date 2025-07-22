from pydoc import text
import cv2
import time



MODEL_FILE = "models/ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb"
CONFIG_FILE = "models/ssd_mobilenet_v2_coco_2018_03_29/ssd_mobilenet_v2_coco_2018_03_29.pbtxt"
LABEL_FILE = "models/ssd_mobilenet_v2_coco_2018_03_29/coco_class_labels.txt"

FONTFACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
THICKNESS = 1


class ObjectsDetector:
    def __init__(self, model, config, labels):
        self.mean = [0, 0, 0]
        self.in_height = 300
        self.in_width = 300
        # Load class labels from file
        with open(labels, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]
        self.net = cv2.dnn.readNetFromTensorflow(model, config)

    def detect(self, frame, camera_id=0, threshold=0.5):
        events = []
        blob = cv2.dnn.blobFromImage(frame, 1.0, (self.in_width, self.in_height), self.mean, crop=False, swapRB=True)
        self.net.setInput(blob)
        detections = self.net.forward()
        rows = frame.shape[0]
        cols = frame.shape[1]
        # For every Detected Object
        for i in range(detections.shape[2]):
            # Find the class and confidence 
            classId = int(detections[0, 0, i, 1])
            score = float(detections[0, 0, i, 2])

            # Recover original cordinates from normalized coordinates
            x = int(detections[0, 0, i, 3] * cols)
            y = int(detections[0, 0, i, 4] * rows)
            w = int(detections[0, 0, i, 5] * cols - x)
            h = int(detections[0, 0, i, 6] * rows - y)

            if score > threshold:
                event = {
                    "camera_id": camera_id,
                    "type": self.labels[classId],
                    "title": "Detected {}".format(self.labels[classId]),
                    "description": "Detected {} with confidence {:.2f} at ({}, {}) on camera {}".format(self.labels[classId], score, x, y, camera_id),
                    "box": (x, y, w, h),
                    "score": score
                }
                print(event["description"])
                events.append(event)
            break
        return events


    def display(self, frame, events):
        # For every Detected Object
        for event in events:
            x, y, w, h = event["box"]
            # Get text size 
            textSize = cv2.getTextSize(event["type"], FONTFACE, FONT_SCALE, THICKNESS)
            dim = textSize[0]
            baseline = textSize[1]
            # Use text size to create a black rectangle
            cv2.rectangle(frame, (x, y - dim[1] - baseline), (x + dim[0], y + baseline), (0, 0, 0), cv2.FILLED)
            # Display text inside the rectangle
            cv2.putText(frame, event["type"], (x, y - 5), FONTFACE, FONT_SCALE, (0, 255, 255), THICKNESS, cv2.LINE_AA)
            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)




if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cv2.namedWindow("Camera")


    od = ObjectsDetector(model=MODEL_FILE, config=CONFIG_FILE, labels=LABEL_FILE)
    while cv2.waitKey(1) != 27:
        ret, frame = cap.read()
        if not ret:
            break
        events = od.detect(frame)
        od.display(frame, events)
        cv2.imshow("Camera", frame)
    cap.release()
    cv2.destroyAllWindows()
