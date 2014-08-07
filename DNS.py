import os
import sys
from scapy.all import *
ns = sys.argv[1]
query = IP(dst=ns)/UDP()/DNS(rd=1,qd=DNSQR(qname="www.bbc.co.uk"))
reply = sr1(query, timeout=1)
if (DNS in reply) and (reply.rcode==0L):
    print ns + ' OK.'
else:
    print 'DNS failure.'
 

