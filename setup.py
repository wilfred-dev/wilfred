from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="wilfred",  # Replace with your own username
    version="0.0.3-alpha1",
    author="Vilhelm Prytz",
    author_email="vlhelm@prytznet.se",
    description="A CLI for managing game servers using Docker.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wilfred-dev/wilfred",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    python_requires=">=3.6",
    install_requires=["docker", "click", "colorama"],
    entry_points={"console_scripts": ["wilfred=wilfred.wilfred:main",]},
)
