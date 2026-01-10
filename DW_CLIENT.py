import socket

HOST = "192.168.50.2"
PORT = 6000

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((HOST,PORT))

while True:
    data = sock.recv(4096)
    if not data:
        break

    line = data.decode().strip()
    print("NEW CSV ROW:", line)

    dwF.file_write()

