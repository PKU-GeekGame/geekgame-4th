import os

from scapy.all import rdpcap

os.chdir(os.path.dirname(__file__))

packets = rdpcap("WLAN.pcap")
writers = {}

for packet in packets:
  if not packet.haslayer("IP") or not packet["IP"].src == "192.168.137.1":
    continue

  if not packet.haslayer("UDP") or not 47990 <= packet["UDP"].sport <= 48000:
    continue

  sport = packet["UDP"].sport
  dport = packet["UDP"].dport

  if sport not in writers:
    writers[sport] = open(f"{sport}.bin", "wb")

  writers[sport].write(packet["UDP"].load)

for port in writers:
  writers[port].close()
