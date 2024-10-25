import traceback
from textwrap import wrap
from typing import List

from Crypto.Util.number import bytes_to_long, long_to_bytes


def norm_hex(data):
	res = '0' * (len(data) % 2) + data
	if res == '00':
		return res
	while res.startswith('00'):
		res = res[2:]
	return res


def i2h(data: int):
	res = hex(int(data))[2:]
	return norm_hex(res)


def i2b(data: int):
	return long_to_bytes(data)


def i2a(data: int):
	return h2a(i2h(data))


def h2i(data: str):
	return int(data, 16)


def h2b(data: str):
	return bytes.fromhex(norm_hex(data))


def h2a(data: str):
	res = wrap(norm_hex(data), 2)
	return [int(i, 16) for i in res]


def b2i(data: bytes):
	return bytes_to_long(data)


def b2h(data: bytes):
	res = data.hex()
	return norm_hex(res)


def b2a(data: bytes):
	return h2a(b2h(data))


def a2i(data: List[int]):
	return h2i(a2h(data))


def a2h(data: List[int]):
	return "".join([i2h(i) for i in data])


def a2b(data: List[int]):
	while data[0] == 0:
		data = data[1:]
	return bytes(data)


def convert(func, data):
	src = func[0]
	joined_data = "".join(data)
	try:
		if src == 'i':
			return globals()[func](int(joined_data))

		if src == 'h':
			return globals()[func](joined_data)

		if src == 'b':
			# data = re.sub(r"\\x([0123456789abcdefABCDEF]{2})", lambda x:chr(int(x.group()[2:],16)), joined_data)
			return globals()[func](joined_data.encode('latin1').decode("unicode-escape").encode("latin-1"))

		if src == 'a':
			if ',' in joined_data:
				return globals()[func]([int(i) for i in data.split(",")])
			else:
				return globals()[func]([int(i) for i in data])
	except:  # pylint: disable=bare-except
		traceback.print_exc()
	return None
