from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='twilio_phone_calls',
    version='1.0',
    packages=['twilio_phone_calls'],
    install_requires=install_requires,
)
