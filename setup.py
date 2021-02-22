from setuptools import setup
from setuptools import find_packages

setup(
    name='ratatoskr-tools',
    version='0.1',
    author='Jan Moritz Joseph',
    author_email='',
    description='API to automate ratatoskr simulation.',
    url='',
    license='MIT',
    packages=find_packages(exclude=['docs*', 'tests*']),

    entry_points={
        'console_scripts': ['']
    },

)
