from ultralytics import YOLO
import numpy as np
import cv2
from disease_info import disease_data

model = YOLO("models/yolov8.pt")

def predict_image(image_bytes):
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    results = model(img)[0]

    if len(results.boxes) == 0:
        return {
            "label": "no_disease",
            "confidence": 0.0,
            "info": disease_data["no_disease"]
        }

    box = results.boxes[0]
    cls_id = int(box.cls[0])
    conf = float(box.conf[0])
    label = model.names[cls_id]

    return {
        "label": label,
        "confidence": conf,
        "info": disease_data.get(label, {})
    }
