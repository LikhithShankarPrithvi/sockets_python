import selectors
import socket
import types
import sys

sel=selectors.DefaultSelector()

def accept_wrapper(sock):
    conn,addr=sock.accept()
    print('accepting connection from',addr)
    conn.setblocking(False)
    data=types.SimpleNamespace(addr=addr,inb=b'',outb=b'')
    events=selectors.EVENT_READ |selectors.EVENT_WRITE
    sel.register(conn,events,data=data)

def service_connection(key,mask):
    sock=key.fileobj
    data=key.data
    if mask & selectors.EVENT_READ:
        recv_data=sock.recv(1024)
        if recv_data:
            data.outb+=recv_data
        else:
            print('Closing connection to',data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing',repr(data.outb),'to',data.addr)
            sent=sock.send(data.outb)
            data.outb=data.outb[sent:]

if(len(sys.argv)!=3):
    print('exiting the connection ',sys.argv,'<host><port>')
    sys.exit(1)

lsock=socket.socket()  #listening socket
host,port=sys.argv[1],sys.argv[2]
lsock.bind((host,int(port)))
lsock.listen()
print('listening on',(host,port))
lsock.setblocking(False)
sel.register(lsock,selectors.EVENT_READ,data=None)

try:
    while(True):
        events=sel.select(timeout=None)
        for key,mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key,mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
