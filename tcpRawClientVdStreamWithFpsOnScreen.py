import cv2
import socket
import pickle
import struct

# Raspberry Pi IP address and port
SERVER_IP = '192.168.1.103'  # Replace with the IP address of your Windows PC
SERVER_PORT = 6000

# Open the webcam
cap = cv2.VideoCapture(0)

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

try:
    while True:
        # Capture frame from the webcam
        ret, frame = cap.read()

        # Serialize frame
        data = pickle.dumps(frame)
        data_size = struct.pack('!I', len(data))

        # Send frame length
        client_socket.sendall(data_size)

        # Send frame data
        client_socket.sendall(data)

finally:
    cap.release()
    client_socket.close()
