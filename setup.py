from setuptools import setup
from setuptools import find_packages

setup(
    name='ratatoskr-tools',
    version='2021.02',
    author='Jan Moritz Joseph, Yee Yang Tan',
    author_email='joseph@ice.rwth-aachen.de',
    description='API to automate ratatoskr simulation.',
    url='https://github.com/jmjos/ratatoskr-tools',
    license='MIT',
    packages=find_packages(exclude=['docs*', 'tests*']),
    package_data={
        'ratatoskr_tools.networkconfig': ['*.ini']
    },
    entry_points={
        'console_scripts': ['']
    },

)
