"""A setuptools based setup module.
"""
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='faster',  # Required
    version='0.1.10',  # Required
    description='A pip tool help you get the best pip source',  # Required
    long_description=long_description,  # Optional

    url='https://github.com/lfzark/faster',  # Optional
    author='ark1ee',

    author_email='onlyarter@gmail.com',  # Optional

    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],

    keywords='pip tools',  # Optional

    packages=["faster"],  # Required

    install_requires=[],  # Optional

    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    package_data={'faster': [
        'pip.json'], },

    entry_points={ 
        'console_scripts': [
            'faster=faster.faster:start',
        ],
    },
)