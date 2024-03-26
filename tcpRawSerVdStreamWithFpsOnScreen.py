#DONE! Server: Working code for TCP that sends video to server. Server shows the FPS on opencv Window
import cv2
import socket
import pickle
import struct
import time

# Windows PC IP address and port
#SERVER_IP = '192.168.1.103'  # Replace with the IP address of your Windows PC
SERVER_IP = '192.168.0.101'  # sworno vai er basha
SERVER_PORT = 6000

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

# Accept connection from Raspberry Pi
client_socket, addr = server_socket.accept()

# OpenCV window for displaying the video stream
cv2.namedWindow('Video Stream', cv2.WINDOW_NORMAL)

# Initialize variables for measuring FPS
start_time = time.time()
frame_count = 0
fps = 0

try:
    while True:
        # Receive frame length
        data = client_socket.recv(4)
        if not data:
            break
        frame_length = struct.unpack('!I', data)[0]

        # Receive frame data
        data = b""
        while len(data) < frame_length:
            packet = client_socket.recv(frame_length - len(data))
            if not packet:
                break
            data += packet
        
        # Convert bytes to frame
        frame = pickle.loads(data)

        # Increment frame count
        frame_count += 1

        # Calculate FPS
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1.0:  # Update FPS every second
            fps = frame_count / elapsed_time
            start_time = time.time()
            frame_count = 0

        # Display FPS on the video frame
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display frame
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    server_socket.close()
    cv2.destroyAllWindows()
