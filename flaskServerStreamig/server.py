# Import necessary modules
from flask import Flask, render_template, Response, request, jsonify
from aiortc import RTCPeerConnection, RTCSessionDescription
import cv2
import json
import uuid
import asyncio
import time

# Create a Flask app instance
app = Flask(__name__, static_url_path='/static')

# Set to keep track of RTCPeerConnection instances
pcs = set()

# Function to generate video frames from the camera and calculate FPS
def generate_frames():
    camera = cv2.VideoCapture(0)
    #fps = 0
    #start_time = time.time()
    
    frame_count = 0
    start_time = time.time()
    fps = 0 
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            frame_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time >= 1.0:
                fps = frame_count / elapsed_time
                print(f"FPS: {fps:.6f}")  # Print FPS to console
                start_time = time.time()
                frame_count = 0

            else:
                time.sleep(0.01)  # Adjust the delay if necessary to maintain desired FPS

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route to render the HTML template
@app.route('/')
def index():
    return render_template('index.html')

# Asynchronous function to handle offer exchange
async def offer_async():
    params = await request.json
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    # Create an RTCPeerConnection instance
    pc = RTCPeerConnection()

    # Generate a unique ID for the RTCPeerConnection
    pc_id = "PeerConnection(%s)" % uuid.uuid4()
    pc_id = pc_id[:8]

    # Create and set the local description
    await pc.createOffer(offer)
    await pc.setLocalDescription(offer)

    # Prepare the response data with local SDP and type
    response_data = {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}

    return jsonify(response_data)

# Wrapper function for running the asynchronous offer function
def offer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    future = asyncio.run_coroutine_threadsafe(offer_async(), loop)
    return future.result()

# Route to handle the offer request
@app.route('/offer', methods=['POST'])
def offer_route():
    return offer()

# Route to stream video frames
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
