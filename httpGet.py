import os
import sys
from scapy.all import *

def httpGet():
    syn = IP(dst='www.bbc.co.uk')/TCP(dport=80, flags='S')
    syn_ack= sr1(syn,timeout=1)
    getStr = 'GET / HTTP/1.1\r\nHost: www.bbc.co.uk\r\n\r\n'
    request = IP(dst='www.bbc.co.uk')/TCP(dport=80,sport=syn_ack[TCP].dport,seq=syn_ack[TCP].ack,ack=syn_ack[TCP].seq+1,flags='A')/getStr
    reply = sr1(request)

    if (TCP in reply and reply[TCP].seq==syn_ack[TCP].seq+1):
        return 'OK.'
    else:
        return 'bad response.'

if __name__ == '__main__':
    httpGet()


