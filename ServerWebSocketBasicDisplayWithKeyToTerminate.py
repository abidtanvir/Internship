import asyncio
import websockets
import logging
import cv2
import numpy as np
import time

logging.basicConfig(level=logging.INFO)

# Function to display video frames
def display_frame(frame, fps):

    cv2.rectangle(frame, (0, 0), (180, 40), (0, 0, 0), -1) #Black rectangle
    # Draw FPS on the frame
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Video Stream', frame)
    key = cv2.waitKey(1)  # Needed to update the window
    return key

async def handle_client(websocket, path):
    logging.info(f"New connection from {websocket.remote_address}")

    frame_count = 0
    start_time = time.time()
    fps = 0  # Initialize fps with a default value

    try:
        async for frame_bytes in websocket:
            # Convert frame bytes to numpy array
            frame_data = np.frombuffer(frame_bytes, dtype=np.uint8)

            # Process the frame data as needed
            # For example, you can display it using OpenCV
            frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)
            key = display_frame(frame, fps)  # passing FPS 

            # Check if 'q' key is pressed
            if key == ord('q'):
                logging.info("Terminating video capture and closing connection.")
                break

            frame_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time >= 1.0:
                fps = frame_count / elapsed_time
                logging.info(f"FPS: {fps:.2f}")
                start_time = time.time()
                frame_count = 0

            # Update FPS display on the frame
            key = display_frame(frame, fps)

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
