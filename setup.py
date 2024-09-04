from setuptools import setup

setup(
	name="myutils",
	use_scm_version=True,
	description="h2g2's crypto utils package",
	long_description="h2g2's crypto utils package",
	url="https://github.com/AvyChanna/myutils",
	author="AvyChanna",
	author_email="AvyChanna@h2g2.com",
	include_package_data=True,
	packages=["myutils"],
	setup_requires=['setuptools_scm'],
	extras_require={
		"gmpy2": [
			"gmpy2",
		],
	},
	install_requires=[
		"more_itertools",
		"requests",
		"labmath",
		"pyzxing",
	],
)
