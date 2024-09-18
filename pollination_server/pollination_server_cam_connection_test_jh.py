import cv2, socket, struct
import numpy as np

# pollination server ip, port
server_ip = "192.168.0.42"
server_port = 9003

# 소켓 생성 및 바인딩
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)
print(f"서버가 {server_ip} : {server_port}에서 대기 중입니다...")

# 클라이언트 연결 수립
conn, addr = server_socket.accept()
print(f"클라이언트 {addr}와 연결되었습니다.")

# 파일 객체 생성
file = conn.makefile("rb")

try:
    while True:
        msg = b''

        while b'\n' not in msg:
            msg += server_socket.recv(len(b'\n'))
        
        if msg != b'':
            header = msg[:2].decode("utf-8")
            frame_size = struct.unpack(">L", msg[2:6])[0]
            frame_data = msg[6:6+frame_size]

            if header == "SF":
                frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), cv2.IMREAD_COLOR)

                cv2.imshow("received frame", frame)
                cv2.waitkey(1)

except Exception as e:
    print(f"Error receiving or displaying frame: {e}")