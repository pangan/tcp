import socket
import sys
import threading
import re
import datetime 

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

def resp_html():
    html_file = open('template.html','r')
    html = html_file.readlines()
    return html

def time_stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Create a TCP/IP socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1 )
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
    #print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    #print >>sys.stderr, 'connection from', client_address

    data = connection.recv(1024)
    data_dic = parse_data(data)
    for html_lines in resp_html():
        connection.sendall(html_lines)
    connection.close()
    a += 1
    if data_dic:
    
        if 'c' in data_dic:
            if data_dic['c'] == 'forward':
                print >>sys.stderr, '[%s] FORWARD   ' %time_stamp(), client_address
            if data_dic['c'] == 'reverce':
                print >>sys.stderr, '[%s] REVERCE   ' %time_stamp(), client_address
            if data_dic['c'] == 'right':
                print >>sys.stderr, '[%s] RIGHT     ' %time_stamp(), client_address
            if data_dic['c'] == 'left':
                print >>sys.stderr, '[%s] LEFT      ' %time_stamp(), client_address
            if data_dic['c'] == 'startstop':
                print >>sys.stderr, '[%s] START/STOP' %time_stamp(), client_address


        if 'x' in data_dic:
            
            print >>sys.stderr, '[%s] EXIT', client_address
            #threading.Thread(target = do_motor).stop()
            exit_flag = True
            sock.close()
            exit(1)
            




