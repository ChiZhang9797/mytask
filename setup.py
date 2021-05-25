import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='mytask',
    version='0.0.1',
    packages=['mytask'],
    include_package_data=True,
    install_requires=[
        'Click',
        'SQLAlchemy',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'mytask = mytask.__main__:cli',
        ],
    },
)