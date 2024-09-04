from functools import reduce
from itertools import cycle, islice

from labmath import lcm


def bxor(*inputs):
	return bytes(reduce(lambda x, y: x ^ y, i) for i in zip(*inputs))


def bxor_cyclic(*iters, l=0):
	if l == 0:
		l = max(len(i) for i in iters)
	elif l == -1:
		l = lcm(len(i) for i in iters)
	iters = [islice(cycle(i), l) for i in iters]
	return bxor(*iters)


def blockize(data, k=16):
	return [data[i:i + k] for i in range(0, len(data), k)]


def wr(data):
	with open("a.txt", "wb") as f:
		f.write(data)

class ddict(dict):
	__getattr__ = dict.get
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__