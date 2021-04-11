from setuptools import setup

# import os.path
# install_reqs = None
# with open('requirements.txt', 'r') as f:
# 	install_reqs = [s for s in [line.split('#', 1)[0].strip(' \t\n') for line in f] if s != '']

setup(
    name="myutils",
    use_scm_version=True,
    description="h2g2's crypto utils package",
    long_description="h2g2's crypto utils package",
    url="https://github.com/AvyChanna/myutils",
    author="Avneet Singh",
    author_email="AvyChanna@h2g2.com",
    include_package_data=True,
    packages=["myutils"],
    setup_requires=['setuptools_scm'],
    extras_require={
        "crypto": [
            "pycryptodome",
        ],
        "cryptox": [
            "pycryptodomex",
        ],
    },
    # install_requires=install_reqs,
    install_requires=[
        "gmpy2",
        "more_itertools",
        "requests",
        "labmath",
        "pyzxing",
    ],
)
