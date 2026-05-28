from flask import Flask, render_template, Response, jsonify
import threading
import cv2

# Import your gesture logic
from gesture_engine import GestureEngine

app = Flask(__name__)

engine = GestureEngine()
thread = None


def run_engine():
    engine.start()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start')
def start():
    global thread
    if not engine.running:
        thread = threading.Thread(target=run_engine)
        thread.daemon = True
        thread.start()
    return jsonify({"status": "started"})


@app.route('/stop')
def stop():
    engine.stop()
    return jsonify({"status": "stopped"})


def generate_frames():
    while True:
        frame = engine.get_frame()
        if frame is None:
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/status')
def status():
    return jsonify({
        "running": engine.running,
        "gesture": engine.current_gesture
    })


if __name__ == '__main__':
    import threading
    threading.Thread(target=engine.start, daemon=True).start()
    app.run(debug=True)