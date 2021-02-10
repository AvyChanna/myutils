from typing import List

import labmath as lm


class rsa:  # pylint: disable=too-many-instance-attributes
	def _has_n_p(self):
		self.q = self.n // self.q
		self.after_factoring()

	def _has_n_only(self):
		if self.phi:
			# N and phi known, factorization possible
			b = self.n + 1 - self.phi
			dd2 = (b * b) - (4 * self.n)
			dd = lm.isqrt(dd2)
			assert dd * dd == dd2
			self.p = (b + dd) // 2
			self.q = (b - dd) // 2
			self.after_factoring()
		elif self.d and self.e:
			ktot = (self.d * self.e) - 1
			t = ktot
			while t % 2 == 0:
				t //= 2
			spotted = False
			a = 2
			while not spotted and a < 100:
				k = t
				while k < ktot:
					cand = pow(a, k, self.n)
					if cand != 1 and cand != (self.n - 1) and pow(cand, 2, self.n) == 1:
						self.p = lm.gcd(cand + 1, self.n)
						spotted = True
						break
					k *= 2
				a += 2
			if not spotted:
				# Non deterministic algo. Doesn't works all the time :/
				# At this point, factored = False and ok = True,
				# so everything will work but you won't have prime factorization or phi
				return
			self.q = self.n // self.p
			self.after_factoring()
		else:
			self.ok = False

	def _has_p_only(self):
		if self.phi:
			self.q = self.phi // (self.p - 1)
			self.after_factoring()
		else:
			self.ok = False

	def init_check(self):
		if self.n:
			if self.p:
				self._has_n_p()
			else:
				self._has_n_only()
		else:
			if self.p:
				self._has_p_only()
			else:
				self.ok = False

	def after_factoring(self):
		assert self.n % self.p == 0
		assert self.p * self.q == self.n
		assert lm.bpsw(self.p)
		assert lm.bpsw(self.q)
		self.factored = True
		self.phi = (self.p - 1) * (self.q - 1)
		# Need atleast one of e, d to calculate another
		if self.e:
			assert lm.gcd(self.e, self.phi) == 1
			self.d = lm.modinv(self.e, self.phi)
		elif self.d:
			assert lm.gcd(self.d, self.phi) == 1
			self.e = lm.modinv(self.d, self.phi)
		else:
			self.ok = False

	def __init__(self, n: int = 0, p: int = 0, d: int = 0, e: int = 0x10001, phi: int = 0) -> None:  # pylint: disable=too-many-arguments
		self.n = n
		self.p = p
		self.q = 0
		self.d = d
		self.e = e
		self.phi = phi
		self.ok = True
		self.factored = False
		self.init_check()
		if not self.factored:
			print("Can not get factors")
		if not self.ok:
			print("Do not have n/e/d")

	def encrypt(self, m):
		if self.ok:
			return pow(m, self.e, self.n)
		return None

	def decrypt(self, ct):
		if self.ok:
			return pow(ct, self.d, self.n)
		return None

	def sign(self, m):
		return self.decrypt(m)

	def verify(self, m, sig):
		if self.ok:
			return self.sign(m) == sig
		return None


class multi_rsa:
	def __init__(self, n: int, prime_list: List[int] = None, d: int = None, e: int = 0x10001, phi: int = None):  # pylint: disable=too-many-arguments
		self.n = n
		self.pi = prime_list
		self.d = d
		self.e = e
		self.phi = phi
		self.ok = True
		self.factored = False
		self.init_check()
		if not self.factored:
			print("Can not get factors")
		if not self.ok:
			print("Do not have n/e/d")

	def init_check(self):
		if self.pi is not None and len(self.pi) != 0:
			prod = 1
			for i in self.pi:
				assert lm.bpsw(i)
				prod *= i
			if self.n == prod:
				self.after_factoring()
				return
		if self.phi:
			self.after_totient()
		elif self.d and self.e:
			pass
		else:
			self.ok = False

	def after_totient(self):
		if self.e:
			assert lm.gcd(self.e, self.phi) == 1
			self.d = lm.modinv(self.e, self.phi)
		elif self.d:
			assert lm.gcd(self.d, self.phi) == 1
			self.e = lm.modinv(self.d, self.phi)
		else:
			self.ok = False

	def after_factoring(self):
		primes = {}
		for p in self.pi:
			primes[p] = primes.get(p, 0) + 1
		self.phi = lm.carmichael(primes)
		self.factored = True
		self.after_totient()

	def encrypt(self, m):
		if self.ok:
			return pow(m, self.e, self.n)
		return None

	def decrypt(self, ct):
		if self.ok:
			return pow(ct, self.d, self.n)
		return None

	def sign(self, m):
		return self.decrypt(m)

	def verify(self, m, sig):
		if self.ok:
			return self.sign(m) == sig
		return None
