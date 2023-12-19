import socket

HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 6000  # port number

# Add authentication details
valid_username = 'tanvir'
valid_password = 'tanvir'

def authenticate(username, password):
    return username == valid_username and password == valid_password

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on port {PORT}")
    conn, addr = s.accept()

    with conn:
        print('Connected by', addr)

        # Authentication process
        #conn.sendall(b'Username: ')
        username = conn.recv(1024).decode().strip()
        #conn.sendall(b'Password: ')
        password = conn.recv(1024).decode().strip()
        if not authenticate(username, password):
            print("!! Authentication failed !! Closing connection.. !!")
            conn.sendall(b' !!Authentication failed !! Closing connection..')
        else:
            conn.sendall(b'Authentication successful')


        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(b'Hello From Tanvir PC')
            print('From Client:', data.decode())

            if data.strip() == b"close":
                print("Connection Closed!!")
                break
