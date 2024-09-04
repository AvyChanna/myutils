import argparse
import itertools

from myutils.conversion import convert

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	subparser = parser.add_subparsers()

	conv_parser = subparser.add_parser("conv")
	conv_parser.set_defaults(parser_cmd="conv")
	conv_parser.add_argument("descriptor", choices=[f"{i}2{j}" for i, j in itertools.permutations("ihba", 2)], type=str)
	conv_parser.add_argument("input_data", nargs='+', type=str)

	args = parser.parse_args()

	if args.parser_cmd == "conv":
		res = convert(args.descriptor, args.input_data)
		if res is not None:
			print(res)
		else:
			print()
