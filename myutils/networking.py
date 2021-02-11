import socket

import requests


class sock(socket.socket):
	def __init__(self, *args, timeout: int = 2, **kwargs):
		super().__init__(*args, **kwargs)
		self.settimeout(timeout)

	def cin(self) -> bytes:
		return self.recv(5000)

	def cout_nl(self, s):
		if not isinstance(s, bytes):
			s = str(s).encode('latin-1')
		s += b'\n'
		self.sendall(s)

	def cout(self, s):
		if not isinstance(s, bytes):
			s = str(s).encode('latin-1')
		self.sendall(s)


def url(s, session=None):
	if session is None:
		return requests.get(s)
	return session.get(s)


class cryptohack(sock):
	def connect(self, port, *args, **kwargs):
		super().connect(("socket.cryptohack.org", port), *args, **kwargs)
