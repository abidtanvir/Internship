import asyncio
import websockets
import logging
import cv2
import numpy as np

logging.basicConfig(level=logging.INFO)

# Function to display video frames
def display_frame(frame):
    cv2.imshow('Video Stream', frame)
    key = cv2.waitKey(1)  # Needed to update the window
    return key

async def handle_client(websocket, path):
    logging.info(f"New connection from {websocket.remote_address}")

    try:
        async for frame_bytes in websocket:
            # Convert frame bytes to numpy array
            frame_data = np.frombuffer(frame_bytes, dtype=np.uint8)

            # Process the frame data as needed
            # For example, you can display it using OpenCV
            frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
            key = display_frame(frame)

            # Check if 'q' key is pressed
            if key == ord('q'):
                logging.info("Terminating video capture and closing connection.")
                break

    except websockets.exceptions.ConnectionClosedError:
        logging.info(f"Connection with {websocket.remote_address} closed.")
    finally:
        cv2.destroyAllWindows()  # Close OpenCV windows

async def start_server():
    async with websockets.serve(handle_client, "0.0.0.0", 6000):
        logging.info("WebSocket server started")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    cv2.namedWindow('Video Stream', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Video Stream', 640, 480)
    asyncio.run(start_server())
