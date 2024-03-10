import socket
import os
import time

# IP address and port of the server
SERVER_IP = '192.168.178.23'  #  server's IP address
SERVER_PORT = 6000  # port where server is listening on

# Get the path to the desktop directory
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

# Path to the video file on Raspberry Pi
VIDEO_FILE_PATH = os.path.join(desktop_path, 'carTest.mp4')  

# Size of buffer for sending data
BUFFER_SIZE = 1024

def send_video():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connected to server")

        # Open the video file
        with open(VIDEO_FILE_PATH, 'rb') as f:
            start_time = time.time()  # Record the start time
            
            # Read and send the video data in chunks
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                client_socket.sendall(data)
            
            print("Video sent successfully")
            
            end_time = time.time()  # Record the end time

            # Calculate and print the total time taken
            total_time = end_time - start_time
            print("Total time taken:", total_time, "seconds")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    send_video()
