# Real-Time Video Sensor Streaming Dashboard

A web-based network management dashboard streaming live camera video (MJPEG) and sensor telemetry (WebSockets) over local network interfaces.

## Features
- **MJPEG Video Streaming:** Low-latency video transmission via HTTP multipart boundaries (`/video_feed`).
- **Hardware Agnostic:** Automatically binds to OpenCV `VideoCapture(0)` or seamlessly generates synthetic frames with diagnostic overlays if camera hardware is unavailable.
- **WebSocket Telemetry:** Pushes environmental and range telemetry at 1 Hz via Flask-SocketIO.
- **Modern Responsive UI:** Dark-themed dashboard with live metric gauges and sliding 30-second Chart.js historical visualization.

## Architecture
```
[ OpenCV Camera / Sensor Sim ]
               |
               v
     [ Flask Application ]
      /                 \
(MJPEG stream)    (Socket.IO Telemetry)
    /                     \
   v                       v
[ Video Canvas ]     [ Live Gauges & Chart.js ]
```

## Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Dashboard
```bash
python app.py
```

### 3. Open in Browser
Navigate to `http://localhost:5000` to view the live dashboard.
