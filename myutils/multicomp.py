import os
import threading
from multiprocessing import Pool
from subprocess import run


class worker:
	def __init__(self, function, iterable, workers=len(os.sched_getaffinity(0)), chunksize=1000):
		self.pool = None
		self.workers = workers
		self.function = function
		self.iterable = iterable
		self.chunksize = chunksize

	def collect(self):
		l = len(self.iterable)
		for ndx in range(0, l, self.chunksize):
			yield self.iterable[ndx:min(ndx + self.chunksize, l)]

	def get_res(self):
		if self.workers:
			self.pool = Pool(processes=self.workers)
		else:
			self.pool = Pool()
		ret = None
		for lst in self.collect():
			ret = self.pool.map(self.function, lst)
			for i in ret:
				if i is not None:
					return i


def run_with_timeout(func, *func_args, timeout_duration: int = 10, default_return=None, **func_kwargs):
	def runFunctionCatchExceptions(func, *args, **kwargs):
		try:
			result = func(*args, **kwargs)
		except Exception as e:  # pylint: disable=broad-except
			return e
		return result

	class InterruptableThread(threading.Thread):
		def __init__(self, default):
			threading.Thread.__init__(self)
			self.result = default

		def run(self):
			self.result = runFunctionCatchExceptions(func, *func_args, **func_kwargs)

	it = InterruptableThread(default_return)
	it.start()
	it.join(timeout_duration)
	if it.is_alive():
		return default_return
	return it.result


def run_cmd(*popenargs, inp=None, capture_output=True, timeout=None, **kwargs):
	return run(*popenargs, inp, capture_output=capture_output, timeout=timeout, check=False, **kwargs)
