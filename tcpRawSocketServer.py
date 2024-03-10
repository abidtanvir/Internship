import socket

# Host and port to bind the server
HOST = '192.168.178.23'  # You can change this to your PC's IP address if needed
PORT = 6000 # Choose a port for your server to listen on

# Size of buffer for receiving data
BUFFER_SIZE = 1024

def receive_video():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the host and port
        server_socket.bind((HOST, PORT))
        print("Server listening on port", PORT)

        # Start listening for incoming connections
        server_socket.listen(1)

        # Accept a connection from a client
        client_socket, address = server_socket.accept()
        print("Connection from", address)

# Receive video data in chunks and print it
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            #print("Received:", data)
        
        print("Video received successfully")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the client socket
        client_socket.close()
        # Close the server socket
        server_socket.close()

if __name__ == "__main__":
    receive_video()