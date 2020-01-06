import sys
from setuptools import setup, find_packages
from wilfred.version import version

assert sys.version_info >= (3, 6, 0), "Wilfred requires Python 3.6+"

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="wilfred",
    version=version,
    author="Vilhelm Prytz",
    author_email="vlhelm@prytznet.se",
    description="A CLI for managing game servers using Docker.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wilfred-dev/wilfred",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    python_requires=">=3.6",
    install_requires=[
        "docker",
        "click",
        "colorama",
        "appdirs",
        "requests",
        "tabulate",
        "yaspin",
    ],
    entry_points={"console_scripts": ["wilfred=wilfred.wilfred:main"]},
)
