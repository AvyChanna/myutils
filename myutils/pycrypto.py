#
# *** Here be demons ***
#
# tldr; switch away from pycrypto. Use pycryptodome as a drop-in replacement.
# Or use pycrypodomex and replace module name to Cryptodome in your source files
#
# Padding functions are available in PyCryptodome.
# These are self-defined in case they are not available.
#

# (Kali has 'Cryptodome', coz it has both of them installed.)

try:
	from Cryptodome.Cipher import AES  # pylint: disable=unused-import
	from Cryptodome.Cipher import PKCS1_OAEP as PKCS_OAEP  # pylint: disable=unused-import
	from Cryptodome.Cipher import PKCS1_v1_5 as PKCS_15  # pylint: disable=unused-import
	from Cryptodome.Util.number import bytes_to_long, long_to_bytes  # pylint: disable=unused-import
	from Cryptodome.Util.Padding import pad  # pylint: disable=unused-import
	from Cryptodome.Util.Padding import unpad  # pylint: disable=unused-import
except:  # pylint: disable=bare-except
	# Try importing 'Crypto' instead (works for both)
	from Crypto.Cipher import AES  # type: ignore
	from Crypto.Cipher import PKCS1_OAEP as PKCS_OAEP  # type: ignore
	from Crypto.Cipher import PKCS1_v1_5 as PKCS_15  # type: ignore
	from Crypto.Util.number import bytes_to_long, long_to_bytes  # type: ignore

	# PyCryptodome has pad/unpad builtin. Import them.
	try:
		from Crypto.Util.Padding import pad, unpad  # type: ignore
	except:
		# If using PyCrypto, define them ourselves
		from Crypto.Util.py3compat import bchr, bord

		# Block size is set to 16, original one did not have any default one.
		def pad(data_to_pad, block_size=16, style='pkcs7'):  # type: ignore
			"""Apply standard padding.
			:Parameters:
			data_to_pad : byte string
				The data that needs to be padded.
			block_size : integer
				The block boundary to use for padding. The output length is guaranteed
				to be a multiple of ``block_size``.
			style : string
				Padding algorithm. It can be *'pkcs7'* (default), *'iso7816'* or *'x923'*.
			:Return:
			The original data with the appropriate padding added at the end.
			"""

			padding_len = block_size - len(data_to_pad) % block_size
			if style == 'pkcs7':
				padding = bchr(padding_len) * padding_len
			elif style == 'x923':
				padding = bchr(0) * (padding_len - 1) + bchr(padding_len)
			elif style == 'iso7816':
				padding = bchr(128) + bchr(0) * (padding_len - 1)
			else:
				raise ValueError("Unknown padding style")
			return data_to_pad + padding

		def unpad(padded_data, block_size=16, style='pkcs7'):  # type: ignore
			"""Remove standard padding.
			:Parameters:
			padded_data : byte string
				A piece of data with padding that needs to be stripped.
			block_size : integer
				The block boundary to use for padding. The input length
				must be a multiple of ``block_size``.
			style : string
				Padding algorithm. It can be *'pkcs7'* (default), *'iso7816'* or *'x923'*.
			:Return:
				Data without padding.
			:Raises ValueError:
				if the padding is incorrect.
			"""

			pdata_len = len(padded_data)
			if pdata_len % block_size:
				raise ValueError("Input data is not padded")
			if style in ('pkcs7', 'x923'):
				padding_len = bord(padded_data[-1])
				if padding_len < 1 or padding_len > min(block_size, pdata_len):
					raise ValueError("Padding is incorrect.")
				if style == 'pkcs7':
					if padded_data[-padding_len:] != bchr(padding_len) * padding_len:
						raise ValueError("PKCS#7 padding is incorrect.")
				else:
					if padded_data[-padding_len:-1] != bchr(0) * (padding_len - 1):
						raise ValueError("ANSI X.923 padding is incorrect.")
			elif style == 'iso7816':
				padding_len = pdata_len - padded_data.rfind(bchr(128))
				if padding_len < 1 or padding_len > min(block_size, pdata_len):
					raise ValueError("Padding is incorrect.")
				if padding_len > 1 and padded_data[1 - padding_len:] != bchr(0) * (padding_len - 1):
					raise ValueError("ISO 7816-4 padding is incorrect.")
			else:
				raise ValueError("Unknown padding style")
			return padded_data[:-padding_len]
