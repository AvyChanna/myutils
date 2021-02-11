import json
import socket

import requests


class sock(socket.socket):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.timeout()

	def timeout(self, timeout=2):
		self.settimeout(timeout)

	def raw_cin(self, length=5000):
		return self.recv(length)

	def cin(self, length=5000):
		return self.raw_cin(length).decode('latin-1')

	def cin_json(self, length=5000):
		return json.loads(self.cin(length))

	def cout_nl(self, s):
		if not isinstance(s, bytes):
			s = json.dumps(s).encode('latin-1')
		s += b'\n'
		self.sendall(s)

	def cout(self, s):
		if not isinstance(s, bytes):
			s = json.dumps(s).encode('latin-1')
		self.sendall(s)


def url(s, session=None):
	if session is None:
		return requests.get(s)
	return session.get(s)


class cryptohack(sock):
	def connect(self, port, *args, **kwargs):
		super().connect(("socket.cryptohack.org", port), *args, **kwargs)
