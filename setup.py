"""Installation script for 'traffic_management' package.

Disclaimer
----------
This script has been prepared following the instructions from:
https://packaging.python.org/tutorials/packaging-projects/
(as of 29.09.2019).
"""


import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="traffic_management",
    version="0.0.1",
    author="Dominika Dlugosz",
    author_email="dominika.a.m.dlugosz@gmail.com",
    description="Traffic management system - 'Foundations of AI' class assignment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/animaviridis/traffic-management",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['numpy>=1.16', 'pyddl']
)
