import requests
import socket
import threading
requests.packages.urllib3.disable_warnings() # noqa


class ScanPort:
    def __init__(self, target, start_port=None, end_port=None):
        self.target = target
        self.from_port = start_port
        self.to_port = end_port
        self.ports = []

    def scanner(self, target, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            sock.connect((target, port))
            self.ports.append(port)
        except Exception as f: # noqa
            pass

    def __call__(self, *args, **kwargs):
        if self.from_port is None:
            self.from_port = 1
        if self.to_port is None:
            self.to_port = 10000
        try:
            num = 1
            for port in range(self.from_port, self.to_port+1):
                num += 1
                t1 = threading.Thread(target=self.scanner, args=[self.target, port])
                t1.start()
                if num >= 50:
                    for stop_thread in range(1, 100):
                        t1.join()
                    num = 0

        except Exception as e: # noqa
            pass


def scanport(target, start_port=None, end_port=None):
    return ScanPort(target, start_port, end_port)()
