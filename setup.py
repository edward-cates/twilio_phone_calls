from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='twilio_phone_calls',
    version='0.0',
    packages=[
        'twilio_phone_calls',
    ],
    install_requires=install_requires,
)
