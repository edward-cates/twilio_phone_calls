from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='twilio_phone_calls',
    version='0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=install_requires,
)
