####################################################################
#                                                                  #
# Wilfred                                                          #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                  #
# Licensed under the terms of the MIT license, see LICENSE.        #
# https://github.com/wilfred-dev/wilfred                           #
#                                                                  #
####################################################################

import sys
from setuptools import setup, find_packages
from wilfred.version import version

assert sys.version_info >= (3, 6, 0), "Wilfred requires Python 3.6+"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wilfred",
    version=version,
    author="Vilhelm Prytz",
    author_email="vlhelm@prytznet.se",
    description="A CLI for managing game servers using Docker.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://wilfredproject.org",
    project_urls={
        "Documentation": "https://docs.wilfredproject.org",
        "Code": "https://github.com/wilfred-dev/wilfred",
        "Issue tracker": "https://github.com/wilfred-dev/wilfred/issues",
    },
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Natural Language :: English",
    ],
    python_requires=">=3.6",
    install_requires=[
        "docker",
        "click",
        "colorama",
        "appdirs",
        "requests",
        "tabulate",
        "halo",
        "sqlalchemy",
        "pyyaml",
        "pypiwin32 ; platform_system=='Windows'",
    ],
    entry_points={"console_scripts": ["wilfred=wilfred.wilfred:main"]},
)
