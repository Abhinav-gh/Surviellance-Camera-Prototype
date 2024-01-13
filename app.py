from flask import Flask, render_template, Response, request
import cv2
import numpy as np
import base64
import os

app = Flask(__name__)

# Video capture object
camera = cv2.VideoCapture(0)

# Video writer object for recording
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None
recording = False

@app.route('/')
def index():
    return render_template('index_with_record.html')

def generate_frames():
    global recording, out
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            if recording:
                if out is None:
                    # Create the video writer when recording starts
                    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                # Write the frame to the video file
                out.write(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_record')
def start_record():
    global recording
    recording = True
    return 'Recording Started'

@app.route('/stop_record')
def stop_record():
    global recording, out
    recording = False
    if out is not None:
        # Release the video writer when recording stops
        out.release()
        out = None
    else:
        print("Video writer is not initialized.")
    return 'Recording Stopped'

@app.route('/save_snapshot', methods=['POST'])
def save_snapshot():
    try:
        data = request.json
        img_data_url = data['imageData']

        # Extract the base64 encoded part of the data URL
        img_data = img_data_url.split(',')[1]
        # Decode base64 data
        img_binary = base64.b64decode(img_data)

        # Save the image as a PNG file
        file_path = 'snapshot.png'
        with open(file_path, 'wb') as f:
            f.write(img_binary)

        return 'Snapshot saved as PNG: {}'.format(file_path)
    except Exception as e:
        return 'Error saving snapshot: {}'.format(str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
