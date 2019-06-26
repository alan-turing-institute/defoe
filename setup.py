import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="defoe",
    version="0.0.1",
    author="ATI-SE",
    description="Analysis of historical books and newspapers data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alan-turing-institute/defoe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
