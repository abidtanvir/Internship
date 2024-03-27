import asyncio
import websockets
import logging
import cv2

logging.basicConfig(level=logging.INFO)

async def capture_frames(websocket):
    cap = cv2.VideoCapture(0)  # Open webcam
    if not cap.isOpened():
        logging.error("Failed to open webcam")
        return

    try:
        while True:
            # Capture frame from webcam
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to bytes
            _, encoded_frame = cv2.imencode('.jpg', frame)
            frame_bytes = encoded_frame.tobytes()

            # Send frame to server
            try:
                await websocket.send(frame_bytes)
            except websockets.exceptions.ConnectionClosedOK:
                logging.info("Connection closed by server.")
                break

            await asyncio.sleep(0.1)  # Adjust the sleep time as needed

    finally:
        cap.release()  # Release webcam

async def connect_to_server():
    uri = "ws://192.168.178.23:6000"  # Change to your server's IP address and port
    try:
        async with websockets.connect(uri) as websocket:
            logging.info("Connected to server successfully.")
            await capture_frames(websocket)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt detected, closing connection.")

if __name__ == "__main__":
    asyncio.run(connect_to_server())
