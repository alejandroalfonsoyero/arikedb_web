#!/usr/bin/python3
from setuptools import find_packages, setup


with open('README.md', 'r') as f:
    long_description = f.read()

with open('arikedb_web_cli/__init__.py', 'r') as f:
    version = list(
        filter(lambda line: "__version__ =" in line, f.readlines())
    )[0].split("\"")[1]

setup(
    name="arikedb_web_cli",
    version=version,
    description="ArikeDB Web Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alejandro Alfonso",
    author_email="alejandroalfonso1994@gmail.com",
    url="https://github.com/Arikedb/arikedb-web-cli",
    packages=find_packages(exclude=['tests', 'demo']),
    include_package_data=True,
    install_requires=[r.strip() for r in open("requirements.txt").readlines()]
)
