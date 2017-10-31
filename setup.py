import sys
from setuptools import setup, find_packages

setup(name='sangiin_p39',
	version='0.1.0',
	description='Japan Sangiin member checker',
	long_description=open("README.md").read(),
	author='Hiroaki Kawai',
	author_email='hiroaki.kawai@gmail.com',
	url='https://github.com/hkwi/sangiin_p39/',
	packages=find_packages(),
)
