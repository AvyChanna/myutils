import argparse
import itertools

from myutils.conversion import convert

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("conversion_descriptor", choices=[f"{i}2{j}" for i, j in itertools.permutations('ihba', 2)], type=str)
	parser.add_argument("input_data", nargs='+', type=str)
	args = parser.parse_args()
	res = convert(args.conversion_descriptor, args.input_data)
	if res is not None:
		print(res)
