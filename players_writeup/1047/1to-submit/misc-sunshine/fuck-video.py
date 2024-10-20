import os
import sys
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, UDP
import readline
import code


import socket
import bitstring
from optparse import OptionParser


MAX_RTP_PKT_LEN = 1500
MAX_RTP_SEQ_NUM = 65535

TYPE_SINGLE_NALU_01 = 1
TYPE_SINGLE_NALU_23 = 23
TYPE_STAPA = 24
TYPE_NALU_FUA = 28
START_BYTES = b"\x00\x00\x00\x01"

PT_H264 = 96

types = set()
print_cnt = 0

class RFC3984(object):

    def parse_frame(self, pay):
        # print(pay[:20])
        # global print_cnt
        # print_cnt += 1
        # if print_cnt == 20:
        #     sys.exit(0)

        frame = None

        bt = bitstring.BitArray(bytes=pay)

        bc = 0; lc=0;
 
        fb=bt[bc] # i.e. "F"
        nri=bt[bc+1:bc+3].uint # "NRI"
        nlu0=bt[bc:bc+3] # "3 NAL UNIT BITS" (i.e. [F | NRI])
        typ=bt[bc+3:bc+8].uint # "Type"

        print("F, NRI, Type :", fb, nri, typ)
        #print "nlu0 : ", nlu0 
        print(">>>type", typ)

        if (typ >= TYPE_SINGLE_NALU_01) and (typ <= TYPE_SINGLE_NALU_23):
            print(">>> Single NALU", typ)
            #frame = head+pay[lc:]
            frame = START_BYTES + pay[lc:] 

        bc+=8; lc+=1;

        start=bt[bc] # start bit
        end=bt[bc+2] # end bit
        nlu1=bt[bc+3:bc+8] # 5 nal unit bits

        nlu = nlu0+nlu1
        head = START_BYTES + nlu.bytes
        bc+=8; lc+=1;

        if typ == TYPE_NALU_FUA:
            if (start):
                print(">>> First FUA", nlu1.uint)
                frame = head+pay[lc:]
            else:
                print(">>> FUA", nlu1.uint )
                frame = pay[lc:]     

        return frame

class RTP(object):

    def __init__(self, file_name):
        self._first_pkt = False
        self._rtp_sn = -1
        self._payload_type = None

        self._file = open(file_name, 'wb')

        self._codec_depay = { PT_H264: RFC3984}
        self._rfc3984 = RFC3984()
        
        self._first_fua = False

    def parse_csrc(self, pkt, cc, lc):
        bt = bitstring.BitArray(bytes=pkt) 
        cids = []
        bc = 8*lc
        for i in range(cc):
            cids.append(bt[bc:bc+32].uint)
            bc+=32; lc+=4;
        print("csrc identifiers:",cids)

        return lc
 
    #if extend header flag raise, we need to parse extend header
    def parse_ext_hdr(self, pkt, lc):
        # this section haven't been tested.. might fail
        bt = bitstring.BitArray(bytes=pkt) 
        bc = 8*lc
        hid=bt[bc:bc+16].uint
        bc+=16; lc+=2;

        hlen=bt[bc:bc+16].uint
        bc+=16; lc+=2;

        print("ext. header id, header len",hid,hlen)

        hst=bt[bc:bc+32*hlen]
        bc+=32*hlen; lc+=4*hlen;

        return lc

    def parse_hader(self, pkt):

        bt=bitstring.BitArray(bytes=pkt)
        if self._first_pkt == False:
            self._first_pkt = True
 
        version=bt[0:2].uint # version
        p=bt[3] # P
        x=bt[4] # X
        cc=bt[4:8].uint # CC
        m=bt[9] # M
        pt=bt[9:16].uint # PT
        sn=bt[16:32].uint # sequence number
        timestamp=bt[32:64].uint # timestamp
        ssrc=bt[64:96].uint # ssrc identifier

 
        print("version, p, x, cc, m, pt",version,p,x,cc,m,pt)
        print("sequence number, timestamp",sn,timestamp)

        self._rtp_sn = sn
                         
        lc=12 # so, we have red twelve bytes

        # lc = self.parse_csrc(pkt, cc, lc)
        # assert lc == 12

        # frame = self._rfc3984.parse_frame(pkt[lc:])
        frame = pkt[lc:]
   
        if frame != None:
            self._file.write(frame)
   
    def recv_pkt(self, pkt):
       self.parse_hader(pkt)


SERVER_ADDR = "192.168.137.1"

if __name__ == "__main__":
    reader = RawPcapReader("WLAN.pcap")

    printed = 0
    last_seq_num = -1
    rtp_parser = RTP("./output.h264")
    for (pkt_data, pkt_meta) in reader:
        ether_pkt = Ether(pkt_data)
        assert 'type' in ether_pkt.fields
        if ether_pkt.type != 0x800: continue

        ip_pkt = ether_pkt[IP]
        if ip_pkt.proto != 17:
            # Discard non-UDP packets
            continue
        if ip_pkt.src != SERVER_ADDR:
            continue
    
        udp_pkt = ip_pkt[UDP]
        if udp_pkt.sport != 47998:
            continue
        
        # variables = globals().copy()
        # variables.update(locals())
        # shell = code.InteractiveConsole(variables)
        # shell.interact()

        data = bytes(udp_pkt[1])
        
        seq = int.from_bytes(data[2:4], 'big')
        assert seq == last_seq_num+1
        last_seq_num = seq

        printed += 1
        rtp_parser.recv_pkt(data)

print(types)