import functools
import operator

def bxor(*inputs):
	return bytes(i^j for i,j in zip(*inputs))
