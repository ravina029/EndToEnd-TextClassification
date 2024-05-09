#import setuptools
from setuptools import find_packages,setup


__version__ = "0.0.0"

REPO_NAME = "EndToEnd-TextClassification"
AUTHOR_USER_NAME = "ravina029"
SRC_REPO = "Hate Speech Classification"
AUTHOR_EMAIL = "vermaravina029@gmail.com"


setup(
    name="EndToEnd-TextClassification",
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(),
    install_requires=[],
)