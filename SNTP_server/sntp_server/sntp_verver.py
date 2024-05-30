import signal
import socket
import select
from struct import pack, unpack
from time import time
from .config import get_server_config


SETTINGS = get_server_config()

BUFFER_SIZE = 4096
HEAD_FORMAT = ">BBBBII4sQQQQ"
UTC_OFFSET = 2208988800
MODE = 4


class SNTPServer:
    def __init__(self):
        self._stratum = SETTINGS["stratum"]
        self._leap_indicator = SETTINGS["leap_indicator"]
        self._version_number = SETTINGS["version_number"]
        self._offset = SETTINGS["offset"]
        self._socket = self._create_and_bind_socket(SETTINGS["server_ip"], SETTINGS["server_port"])
        self._is_running = False
        signal.signal(signal.SIGINT, self._shutdown_server)

    def run(self):
        self._is_running = True
        while self._is_running:
            if self._is_socket_ready():
                request, addr = self._socket.recvfrom(BUFFER_SIZE)
                response = self._process_request(request)
                self._socket.sendto(response, addr)

    def _process_request(self, request: bytes) -> bytes:
        transmit_timestamp = self._extract_transmit_timestamp(request)
        receive_timestamp = self._get_current_ntp_time()
        return self._create_response(transmit_timestamp, receive_timestamp)

    def _create_response(self, transmit_timestamp, receive_timestamp) -> bytes:
        return pack(
            HEAD_FORMAT,
            self._leap_indicator << 6 | self._version_number << 3 | MODE,
            self._stratum,
            0, 0, 0, 0, b'', 0,
            transmit_timestamp,
            receive_timestamp,
            self._get_current_ntp_time()
        )

    def _is_socket_ready(self) -> bool:
        read_list, _, _ = select.select([self._socket], [], [], 1)
        return bool(read_list)

    def _get_current_ntp_time(self) -> int:
        current_time = time() + UTC_OFFSET + self._offset
        return int(current_time * (2 ** 32))

    def _shutdown_server(self, _, __):
        self._is_running = False
        self._socket.close()

    @staticmethod
    def _extract_transmit_timestamp(request: bytes) -> int:
        return unpack(HEAD_FORMAT, request)[10]

    @staticmethod
    def _create_and_bind_socket(ip: str, port: int) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip, port))
        return sock
