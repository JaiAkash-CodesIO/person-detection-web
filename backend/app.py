from flask import Flask, Response, jsonify, render_template, request
import cv2

from detector import PersonDetector
from config import RTSP_URL

app = Flask(__name__)

# Camera object
camera = None

# Load ONNX detector
detector = PersonDetector()

# Global person count
person_count = 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/connect_camera", methods=["POST"])
def connect_camera():

    global camera

    data = request.get_json()

    source = data.get("source")

    # Release previous camera
    if camera is not None:
        camera.release()

    if source == "laptop":

        camera = cv2.VideoCapture(0)

    elif source == "rtsp":

        camera = cv2.VideoCapture(RTSP_URL)

    else:

        return jsonify({
            "success": False,
            "message": "Invalid camera source"
        })

    return jsonify({
        "success": camera.isOpened()
    })


def generate():

    global camera
    global person_count

    while True:

        if camera is None:
            continue

        success, frame = camera.read()

        if not success:
            continue

        try:

            detections = detector.detect(frame)

            person_count = len(detections)

            for det in detections:

                x1, y1, x2, y2 = det["box"]
                score = det["score"]

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Person {score:.2f}",
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

        except Exception as e:

            print("Detector Error:", e)

        ret, buffer = cv2.imencode(".jpg", frame)

        if not ret:
            continue

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )


@app.route("/video_feed")
def video_feed():

    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/status")
def status():

    global camera
    global person_count

    connected = False

    if camera is not None:
        connected = camera.isOpened()

    return jsonify({

        "camera": connected,

        "persons": person_count

    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )