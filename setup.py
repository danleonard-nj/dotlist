import setuptools
import json

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dotlist",
    version="0.01",
    author="Dan Leonard",
    author_email="me@dan-leonard.com",
    description="A little iterable with big ideas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dan-leonard.com/articles/dotlist-docs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
