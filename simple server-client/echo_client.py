import socket,time,sys
host=socket.gethostname()
port=12345
time.sleep(1)
with socket.socket() as s:
    s.connect((host,port))
    s.sendall(b'Hai ra babai')
    data=s.recv(1024)
    print('recieved',repr(data))
