import cv2
import numpy as np
import onnxruntime as ort

from config import (
    MODEL_PATH,
    INPUT_SIZE,
    CONFIDENCE_THRESHOLD,
    PERSON_CLASS_ID
)


class PersonDetector:

    def __init__(self):

        self.session = ort.InferenceSession(
            MODEL_PATH,
            providers=["CPUExecutionProvider"]
        )

        self.input_name = self.session.get_inputs()[0].name

    def preprocess(self, frame):

        h, w = frame.shape[:2]

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = cv2.resize(image, (INPUT_SIZE, INPUT_SIZE))

        image = image.astype(np.float32) / 255.0

        image = np.transpose(image, (2, 0, 1))

        image = np.expand_dims(image, axis=0)

        return image, w, h

    def detect(self, frame):

        blob, width, height = self.preprocess(frame)

        outputs = self.session.run(
            None,
            {self.input_name: blob}
        )[0]

        detections = []

        for det in outputs[0]:

            cx, cy, bw, bh, score, cls = det

            if score < CONFIDENCE_THRESHOLD:
                continue

            if int(cls) != PERSON_CLASS_ID:
                continue

            # Convert normalized center-format box to pixel x1,y1,x2,y2
            x1 = int((cx - bw / 2) * width)
            y1 = int((cy - bh / 2) * height)
            x2 = int((cx + bw / 2) * width)
            y2 = int((cy + bh / 2) * height)

            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(width - 1, x2)
            y2 = min(height - 1, y2)

            detections.append({
                "box": (x1, y1, x2, y2),
                "score": float(score)
            })

        return detections