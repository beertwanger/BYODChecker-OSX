import os
import sys
from scapy.all import *

def pingGateway(gw):
    ping = IP(dst=gw)/ICMP()
    reply = sr1(ping, timeout=1)
    if not (reply is None):
        return str(gw) + ' OK.'
    else:
        return str(gw) + ' not reachable.'

if __name__ == '__main__':
    pingGateway(sys.argv[1:])


