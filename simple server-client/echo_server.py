import socket,time,sys
host=socket.gethostname()
print(host)
port=12345
time.sleep(1)
with socket.socket() as s:
    s.bind((host,port))
    s.listen()
    c,addr=s.accept()
    with c:
        print('Connected with',addr)
        while(True):
            data=c.recv(1024)
            if not data:
                break
            c.send(data)
