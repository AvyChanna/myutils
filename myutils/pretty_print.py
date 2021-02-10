import json


def pprint(*args, ensure_ascii=False, allow_nan=True, indent='\t', separators=(', ', ': '), **kwargs):
	print(json.dumps(*args, ensure_ascii=ensure_ascii, allow_nan=allow_nan, indent=indent, separators=separators, **kwargs))
