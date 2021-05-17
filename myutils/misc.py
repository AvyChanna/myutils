import functools
import operator

def bxor(*inputs):
	return bytes(functools.reduce(lambda x,y:x^y, i) for i in zip(*inputs))

def blockize(data, k=16):
	return [data[i:i+k] for i in range(0, len(data), k)]
def wr(data):
	with open("a.txt", "wb") as f:
		f.write(data)
