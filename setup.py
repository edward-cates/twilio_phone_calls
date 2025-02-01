from setuptools import setup
from pathlib import Path

readme_text = Path("README.md").read_text()

setup(
    name='twilio_phone_calls',
    version='1.3', # Jan 31, 2025.
    packages=[
        'twilio_phone_calls',
        'twilio_phone_calls.audio',
        'twilio_phone_calls.twilio_pydantic',
    ],
    install_requires=[
        'fastapi==0.115.8',
        'gTTS==2.5.4',
        'librosa==0.10.2.post1',
        'noisereduce==3.0.3',
        'openai-whisper==20240930',
        'pydub==0.25.1',
        'pyright==1.1.393',
        'pytest==8.3.4',
        'python-multipart==0.0.20',
        'pywav==1.1',
        'scikit-learn==1.6.1',
        'soundfile==0.13.1',
        'SpeechRecognition==3.14.1',
        'twilio==9.4.4',
        'uvicorn==0.34.0',
        'websockets==14.2',
    ],
    author='Edward Cates',
    description='Python Implementation for Handling Twilio Phone Calls',
    # long_description='This package handles all the audio conversion so that you can just deal with text-to-text.',
    long_description=readme_text,
    long_description_content_type='text/markdown',
    url='https://github.com/edward-cates/twilio_phone_calls',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
