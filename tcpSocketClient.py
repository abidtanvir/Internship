import socket

HOST = '192.168.178.23'  # Replace with Windows PC's IP address
PORT = 6000  # Use the same port number as the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello from Tanvir RPi!')
    data = s.recv(1024)

print('Server received:', repr(data))