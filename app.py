"""
Real-Time Video & Sensor Streaming Dashboard
Flask + OpenCV + Socket.IO server.
"""
import time
import io
from flask import Flask, render_template, Response, jsonify
from flask_socketio import SocketIO
from sensors import generate_telemetry

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
except ImportError:
    Image = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "abdullah-telecom-telemetry-key"
socketio = SocketIO(app, cors_allowed_origins="*")

camera = None
if cv2 is not None:
    try:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            camera = None
    except Exception:
        camera = None


def generate_synthetic_frame() -> bytes:
    """Generates a dynamic placeholder video frame when no hardware camera is present."""
    width, height = 640, 480
    if Image is not None:
        img = Image.new("RGB", (width, height), color=(18, 22, 34))
        draw = ImageDraw.Draw(img)

        # Draw grid
        for x in range(0, width, 40):
            draw.line([(x, 0), (x, height)], fill=(30, 40, 60), width=1)
        for y in range(0, height, 40):
            draw.line([(0, y), (width, y)], fill=(30, 40, 60), width=1)

        # Crosshair
        cx, cy = width // 2, height // 2
        draw.line([(cx - 30, cy), (cx + 30, cy)], fill=(0, 212, 255), width=2)
        draw.line([(cx, cy - 30), (cx, cy + 30)], fill=(0, 212, 255), width=2)
        draw.ellipse([(cx - 20, cy - 20), (cx + 20, cy + 20)], outline=(0, 212, 255), width=2)

        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        draw.text((20, 20), "TELEMETRY VIDEO STREAM [EMULATED LIVE]", fill=(0, 255, 170))
        draw.text((20, 45), f"TIMESTAMP: {ts}", fill=(200, 200, 220))
        draw.text((20, 440), "Edge AI Object Tracking: Standby", fill=(255, 180, 0))

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=80)
        return buffer.getvalue()
    else:
        # Fallback raw JPEG minimal header
        return b""


def get_frame() -> bytes:
    """Acquires frame from hardware camera or synthesizes one."""
    if camera and camera.isOpened():
        success, frame = camera.read()
        if success:
            ret, buffer = cv2.imencode(".jpg", frame)
            if ret:
                return buffer.tobytes()
    return generate_synthetic_frame()


def gen_frames():
    """MJPEG streaming generator."""
    while True:
        frame_bytes = get_frame()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")
        time.sleep(0.06)  # ~16 FPS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/telemetry")
def telemetry_api():
    return jsonify(generate_telemetry())


def telemetry_broadcaster():
    """Background task pushing live telemetry to connected WebSocket clients."""
    while True:
        data = generate_telemetry()
        socketio.emit("telemetry_update", data)
        socketio.sleep(1.0)


@socketio.on("connect")
def on_connect():
    print("[*] Dashboard client connected.")


if __name__ == "__main__":
    socketio.start_background_task(telemetry_broadcaster)
    print("==================================================================")
    print("  Real-Time Video Sensor Streaming Dashboard")
    print("  Access dashboard in browser at: http://localhost:5000")
    print("==================================================================")
    socketio.run(app, host="0.0.0.0", port=5000, debug=False, allow_unsafe_werkzeug=True)
