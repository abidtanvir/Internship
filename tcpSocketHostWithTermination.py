import socket

HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 6000  # Choose a port number

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on port {PORT}")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print('Received:', data.decode())
            conn.sendall(b' yes Received: ' + data)

            if data.strip() == b"close":
                print("Closing connection...")
                break
