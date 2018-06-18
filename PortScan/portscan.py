import socket
from collections import OrderedDict
import struct
import re
from random import randint
from multiprocessing import Pool



class PortScannerAsync:
    def __init__(self, ip, udp = False):
        self.addr = ip
        self.pool = Pool(1)
        self.udp = udp

    def start(self, start=1, end=65535):
        rng = [(self.addr, i) for i in range(start, end)]
        if self.udp:
            func = port_udp
        else:
            func = port_tcp
        return self.pool.imap(func, rng)

ID = randint(1, 65535)
DNSPACK = struct.pack("!HHHHHH", ID, 256, 1, 0, 0, 0) + b"\x06google\x03com\x00\x00\x01\x00\x01"
TCP_PACKS = OrderedDict([
    ("dns" , struct.pack("!H", len(DNSPACK)) + DNSPACK),
    ("smtp" , b'HELO'),
    ("http" , b'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n'),
    ("pop3" , b"AUTH")
])
UDP_PACKS = OrderedDict([
    ("dns" , DNSPACK),
    ("ntp" , struct.pack('!BBBb11I', (2 << 3) | 3, *([0]*14)))
])
#194.54.80.11
#212.193.68.254
def print_result():
    res = PortScannerAsync("194.54.80.11  ", udp=False).start(24, 26)
    i = 0
    while True:
        try:
            nxt = res.next(timeout=6)
            if nxt:
                print("Port {} open (service: {})".format(*nxt))
                i = i+1
            else:
                i =i+1
                print(i)
                print(nxt)
        except TimeoutError:
            break
        except StopIteration:
            break


def port_tcp(addr):
    ip, port = addr
    socket.setdefaulttimeout(1)
    for prot in TCP_PACKS:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect(addr)
                sock.sendall(TCP_PACKS[prot])
                data = sock.recv(12)
                print(data)
                if ip == 25:
                    print("here")
                return port, check_sign(data)
            except:
                continue


def port_udp(addr):
    ip, port = addr
    res = "not detected"
    socket.setdefaulttimeout(2)
    for prot in UDP_PACKS:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                sock.sendto(UDP_PACKS[prot], addr)
                data, _ = sock.recvfrom(48)
                print(data)
                parse = struct.unpack("bbh", data[:4])
                print(parse)
                res = check_sign(data)
                if parse[0] == 19:
                    res = "Зарезервировано для обеспечения безопасности, тип ICMP - 19 "
                print(res)
            except:
                continue
    if res != "not detected":
        return port, res


def check_sign(pack):
    if pack[:4].startswith(b"HTTP"):
        return 'http'
    elif re.match(b"[0-9]{3}", pack[:3]):
        return "smtp"
    if struct.pack("!H", ID) in pack:
        return "dns"
    elif pack.startswith(b"+"):
        return "pop3"
    else:
        try:
            struct.unpack('!BBBb11I', pack)
        except:
            return "not detected"
        else:
            return "ntp"

if __name__ == "__main__":
    print_result()
