import cv2
from flask import Flask, Response

app = Flask(__name__)

cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)

def video():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ret, jpeg = cv2.imencode(".jpg" , frame)

        if not ret:
            break

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(video() ,  mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host = "192.168.8.104" , port = 5000)
