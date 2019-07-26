import os
import socket
import time

def get_local_ip_addr():
    gw = os.popen("ip -4 route show default").read().split()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((gw[2], 0))
    return s.getsockname()[0]

def is_server_listening():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_listening = sock.connect_ex(('0.0.0.0', 5001))

    if is_listening == 0:
        print "Im listening"
        sock.close()
        return True
    else:
        print "Im NOT listening"
        sock.close()
        return False
