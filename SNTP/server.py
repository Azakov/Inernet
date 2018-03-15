import socket
from threading import Thread
import struct
from argparse import ArgumentParser
from time import time


class Server(Thread):
    def __init__(self, lies):
        super().__init__()
        self.lies = lies
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.server_socket.bind(("", 123))
        except OSError:
            self.server_socket.bind(("", 6000))

        while True:
            self.data, self.addr = self.server_socket.recvfrom(1024)
            self.receive_timestamp = time() + self.lies + 2208988800
            self.start()

    def run(self):
        li_vn_mode, stratum, poll, precision, root_delay, root_dispersion, \
        reference_identifier, reference_timestamp, originate_timestamp, \
        rec, transmit_timestamp = struct.unpack("!BBBBIIIQQQQ", self.data)
        self.packet = struct.pack("!BBBBIIIQQQQ", 0b00100100, 1, 0, 0,
                                  0, 0, 0, 0,
                                  int(transmit_timestamp + (self.lies * 2 ** 32)),
                                  int(self.receive_timestamp * 2 ** 32),
                                  int((time() + 2208988800 + self.lies) * 2 ** 32))
        self.server_socket.sendto(self.packet, self.addr)
        pass


def get_shift():
    parser = ArgumentParser()
    parser.add_argument("-s", "--shift", type=int, default=0, help="Ложь на shift секунд")
    return parser.parse_args()


def main():
    args = get_shift()
    serv = Server(args.shift)
    pass

if __name__ == '__main__':
    main()
