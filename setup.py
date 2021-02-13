from setuptools import setup, find_packages

setup(
    name='origins',
    version='1.0.0',
    url='https://github.com/mypackage.git',
    author='Sabi Hasx',
    author_email='None',
    description='London Housing market data',
    packages=find_packages(),    
    install_requires=['numpy >= 1.11.1', 'requests==2.25.1'],
)
