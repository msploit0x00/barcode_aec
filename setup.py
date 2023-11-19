from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in barcode_aec/__init__.py
from barcode_aec import __version__ as version

setup(
	name="barcode_aec",
	version=version,
	description="barcode print",
	author="ds",
	author_email="ds",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
