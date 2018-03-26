# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

import sys
if sys.version_info < (3,4):
    sys.exit('Sorry, Python < 3.4 is not supported')

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='rumba-backend',

    version='1.0',

    description='Backend for the Rumba project.',
    long_description=long_description,

    # Author details
    author='i2cat-SEG',
    author_email='segdev@i2cat.net',

    #  TODO Choose your license
    #license='MIT',

    # What does your project relate to?
    keywords='live-streaming',

    # List of packages
    packages=find_packages(),

    # List of run-time dependencies.
    install_requires=requirements,
)