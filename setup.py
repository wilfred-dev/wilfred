import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="nerdlan",  # Replace with your own username
    version="0.0.1",
    author="Vilhelm Prytz",
    author_email="vlhelm@prytznet.se",
    description="A CLI for managing game servers using Docker.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nerdlan/nerdlan",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    python_requires=">=3.6",
)
