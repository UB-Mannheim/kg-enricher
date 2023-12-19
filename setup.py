#!/usr/bin/env python3

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kg-enricher",
    version='0.1.0',
    author="Renat Shigapov",
    license="MIT",
    description="A Python library for enriching strings, entities and KGs using Wikibase knowledge graphs. "
                "It's adapted for people, organizations and German geographic entities, both modern and historical.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UB-Mannheim/madata",
    install_requires=['geopandas', 'shapely', 'requests', 'appengine-python-standard'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
