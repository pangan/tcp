import socket
import sys
import threading
import re

global s
s = 0

global exit_flag
exit_flag = False

def do_motor():
    #global s
    #print s
    #s +=1
    if not exit_flag:
        threading.Thread(target = do_motor).start()
    
def parse_data(raw_data):
    m = re.search('\?(.+?) ', raw_data)
    if m:
        tmp_params = m.group(1).split('&')
        ret_dic = {}
        for item in tmp_params:
            var_tmp = item.split('=')
            ret_dic[var_tmp[0]]=var_tmp[1]

        return ret_dic

    else:
        return None

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('0.0.0.0', 8080)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
a=0
do_motor()

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
    data = connection.recv(1024)
    data_dic = parse_data(data)
    
    
    connection.sendall('Hello %s' %a)
    connection.close()
    a += 1
    if data_dic:
        print >>sys.stderr, 'received --->"%s"' % data_dic
        if 'x' in data_dic:
            print "exiting"
            #threading.Thread(target = do_motor).stop()
            exit_flag = True
            sock.close()
            exit(1)
            



