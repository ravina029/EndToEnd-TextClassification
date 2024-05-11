#import setuptools
from setuptools import find_packages,setup


__version__ = "0.0.0"
AUTHOR_USER_NAME = "ravina029"
AUTHOR_EMAIL = "vermaravina029@gmail.com"


setup(
    name="HatespeechTextClassification",
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    install_requires=[],
)