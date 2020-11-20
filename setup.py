import os

from setuptools import find_packages, setup

setup(
    name="evol-dynamics",
    version="1.0.0",
    author="Nikoleta Glynatsi",
    author_email=("glynatsi@evolbio.mpg.de"),
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="",
    license="The MIT License (MIT)",
    description="A package to carry out evolutionary experiments.",
)
