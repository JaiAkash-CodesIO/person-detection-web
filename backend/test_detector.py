import cv2
import numpy as np
import onnxruntime as ort

session = ort.InferenceSession("models/best.onnx")

image = cv2.imread("test.jpg")

img = cv2.resize(image, (640, 640))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = img.astype(np.float32) / 255.0
img = np.transpose(img, (2, 0, 1))
img = np.expand_dims(img, 0)

outputs = session.run(None, {"images": img})[0]

print("Output shape:", outputs.shape)

# Print first 20 detections
for i in range(20):
    print(outputs[0][i])