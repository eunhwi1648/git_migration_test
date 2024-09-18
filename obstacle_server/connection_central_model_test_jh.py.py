import socket
import struct
import cv2
import numpy as np
import os
from ultralytics import YOLO

central_server_ip = "192.168.0.13"
central_server_port = 4040

central_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
central_server_socket.connect((central_server_ip, central_server_port))

try:
    while True:
        header = b''
        
        while len(header) < 2:
            header += central_server_socket.recv(2 - len(header))
        
        # frame data
        if header == b'SF':
            size_data = b''
            while len(size_data) < 4:
                packet = central_server_socket.recv(4 - len(size_data))
                if not packet:
                    break
                size_data += packet
            frame_size = struct.unpack(">L", size_data)[0]

            frame_data = b''
            while len(frame_data) < frame_size:
                packet = central_server_socket.recv(frame_size - len(frame_data))
                if not packet:
                    break
                frame_data += packet
            
            central_server_socket.recv(1)

            if frame_data is not None:
                frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

                cv2.imshow("received frame", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("Error: Unable to decode frame")

except Exception as e:
    print(f"Error receiving or displaying frame: {e}")

finally:
    cv2.destroyAllWindows()