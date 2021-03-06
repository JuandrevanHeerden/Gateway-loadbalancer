#! /usr/bin/env python3
import sys 
import logging 
import signal

from scapy.all import *
from scapy.contrib.geneve  import *

def signal_handler(signal, frame):
        print("\nprogram exiting gracefully") 
        sys.exit(0) 

logging.getLogger("scapy").setLevel(logging.CRITICAL) 
bind_layers(UDP, GENEVE, dport=6081)

signal.signal(signal.SIGINT, signal_handler)

def process_packet(p):

        payload = p[GENEVE].getlayer(IP)
        q = p.getlayer(IP)
        temp = q.copy()
        temp[IP].src = q[IP].dst
        temp[IP].dst = q[IP].src
        send(temp,verbose=0)

try:
        print("Starting packet processing....")
        packets=sniff(filter="port 6081",prn=process_packet)

except KeyboardInterrupt:
        print('interrupted')
        sys.exit(0)
