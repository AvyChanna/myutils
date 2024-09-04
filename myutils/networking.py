import json
import socket
import sys

from typing import Optional

import requests


class Remote:
	def __init__(self, ip, port):
		self.sock = socket.socket()
		self.ip = ip
		self.port = port
		self._open = False
		self.sock.connect((ip, port))
		self._open = True
		self.newline = b"\n"

	def __repr__(self):
		return "<{0} ({1}:{2}) at {3}>".format(
			self.__class__.__name__, self.ip, self.port, hex(id(self))
		)

	def close(self):
		self.sock.close()
		self._open = False

	def is_open(self):
		return self._open

	def read(self, n):
		assert self.is_open()
		return self.sock.recv(n)

	def write(self, buf):
		assert self.is_open()
		if isinstance(buf, str):
			return self.sock.send(bytes(buf.encode("latin-1")))
		elif isinstance(buf, (bytes, bytearray)):
			return self.sock.send(buf)
		else:
			raise NotImplementedError("Unsupported buffer type {0}".format(type(buf)))

	def send(self, buf):
		self.write(buf)

	def sendline(self, line):
		if isinstance(line, (bytes, bytearray)):
			self.write(line + self.newline)
		elif isinstance(line, str):
			self.write(line + "\n")
		else:
			raise NotImplementedError("Unsupported buffer type {0}".format(type(line)))

	def sendjson(self, data, json_kwargs=None):
		data_json = data
		data_str = ""
		if json_kwargs is None:
			json_kwargs = {}

		if not isinstance(data, dict):
			# generic objects to json
			s_list = filter(lambda x: not x.startswith("_"), dir(data))
			s_dict = {}
			for i in s_list:
				temp = getattr(data, i)
				if not callable(temp):
					s_dict[i] = temp
			data_json = s_dict

		try:
			data_str = json.dumps(data_json, **json_kwargs)
		except TypeError as t:
			if json_kwargs.get("encoder", None) is None:
				print("You gave me a shitty encoder. Shame on you", file=sys.stderr)
			else:
				print("Data not serializable. Maybe write an encoder?", file=sys.stderr)
			raise t

		self.sendline(data_str)

	def recv(self, n):
		return self.read(n)

	def recvn(self, n):
		buf = self.read(n)
		if len(buf) != n:
			raise (ValueError("Incomplete socket read"))
		return buf

	def recvall(self, n=0x100000):
		return self.read(n)

	def recvuntil(self, delim, drop=False):
		buf = b""
		while delim not in buf:
			buf += self.recvn(1)
		return buf if not drop else buf[: -len(delim)]

	def recvline(self, drop=True):
		return self.recvuntil(self.newline, drop)

	def recvjson(self):
		return json.loads(self.recvline())


class Cryptohack(Remote):
	def __init__(self, port):
		super().__init__("socket.cryptohack.org", port)


def url(s, method="get", session: Optional[requests.Session] = None):
	if session is None:
		return requests.request(method, s)
	return session.request(method, s)
