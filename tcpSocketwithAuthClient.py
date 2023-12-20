import socket

HOST = '192.168.178.23'  # Server PC's IP address
PORT = 6000  # same port number as the server

# Adding authentication details
username = 'tanvir'
password = 'tanvir'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(username.encode())
    #s.recv(1024)  # Wait for response before sending password
    s.sendall(password.encode())
    authentication_status = s.recv(1024)
    if b'Authentication successful' in authentication_status:
        print('Authentication Successfull !!')
        s.sendall(b'Hello from Tanvir RPi!')
        data = s.recv(1024)
        print('From Server:', repr(data))
        s.sendall(b"close")
        
    else:
        print('!! Authentication failed !! Connection Closed !!')
        s.sendall(b"close")

    