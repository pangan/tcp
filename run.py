import sys
import threading
import datetime 

from webinterface import WebServer
import signal

def myhandler(signum, frame):
    webif.close()
    exit(1)


global s
s = 0

global exit_flag
exit_flag = False

def do_motor():
    if not exit_flag:
        threading.Thread(target = do_motor).start()
    
    

def time_stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

signal.signal(signal.SIGINT, myhandler)

webif = WebServer(port=8080,template='template.html', debug=True)

a=0
do_motor()

while True:
	    
    data_dic = webif.read()
    if data_dic:
    
        if 'c' in data_dic:
            if data_dic['c'] == 'forward':
                print >>sys.stderr, '[%s] FORWARD   ' %time_stamp(), webif.client
            if data_dic['c'] == 'reverce':
                print >>sys.stderr, '[%s] REVERCE   ' %time_stamp(), webif.client
            if data_dic['c'] == 'right':
                print >>sys.stderr, '[%s] RIGHT     ' %time_stamp(), webif.client
            if data_dic['c'] == 'left':
                print >>sys.stderr, '[%s] LEFT      ' %time_stamp(), webif.client
            if data_dic['c'] == 'startstop':
                print >>sys.stderr, '[%s] START/STOP' %time_stamp(), webif.client


        if 'x' in data_dic:
            
            print >>sys.stderr, '[%s] EXIT' %time_stamp(), webif.client
            exit_flag = True
            webif.close()
            exit(1)
            




