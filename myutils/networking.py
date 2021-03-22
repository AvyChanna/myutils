import json
import socket
import sys

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

	def cout(self, b):
		self.sendall(b)

	def cout_bytes(self, s_bytes, break_data=0, end=b"\n"):
		s_bytes += end
		if break_data > 0:
			for i in range(0, len(s_bytes), break_data):
				self.send(s_bytes[i:i + break_data])
		else:
			self.sendall(s_bytes)

	def cout_json(self, s, break_data=0, json_encoder=None, end=b"\n"):
		if not isinstance(s, bytes):
			try:
				s_bytes = json.dumps(s, cls=json_encoder).encode('latin-1')
			except TypeError:
				if json_encoder is not None:
					print("Encoder didn't do a flying shit to your class. Shame on you", file=sys.stderr)
				else:
					print("Consider writing an encode for your class", file=sys.stderr)
				s_list = filter(lambda x: not x.startswith("_"), dir(s))
				s_dict = {}
				for i in s_list:
					temp = getattr(s, i)
					if not callable(temp):
						s_dict[i] = temp
				s_bytes = json.dumps(s_dict, cls=json_encoder).encode('latin-1')
		else:
			s_bytes = s
		self.cout_bytes(s_bytes, break_data, end)


def url(s, session=None):
	if session is None:
		return requests.get(s)
	return session.get(s)


class cryptohack(sock):
	def connect(self, port, *args, **kwargs):
		super().connect(("socket.cryptohack.org", port), *args, **kwargs)
