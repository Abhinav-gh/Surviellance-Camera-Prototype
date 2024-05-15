# This is the simple live feed app made in flask. It works on longer disatnces than previous app.py. You can reduce the frame rate and the resolution as per requirement
from flask import Flask, render_template, Response
import cv2
import time
FRAME_RATE = 20
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')

def generate_frames():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 128)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 96)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]
    frame_rate = FRAME_RATE  # Frames per second
    prev = 0
    while True:
        time_elapsed = time.time() - prev
        success, frame = camera.read()
        if success and time_elapsed > 1/frame_rate:
            prev = time.time()
            ret, buffer = cv2.imencode('.jpg', frame, encode_param)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        elif not success:
            camera.release()
            break



@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


