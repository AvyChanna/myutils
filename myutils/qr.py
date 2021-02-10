from pyzxing import BarCodeReader


def qr(filename: str):
	reader = BarCodeReader()
	return [i['raw'] for i in reader.decode(filename)]
