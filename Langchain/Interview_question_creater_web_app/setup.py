# Import necessary functions from setuptools for packaging the application
from setuptools import find_packages, setup

# Set up the package configuration for the web application
setup(
    name="Interview Question Creator Web App",  # Name of the application
    version='0.0.0',                             # Initial version of the application
    author="Muhammad Adil Naeem",                # Author's name
    author_email="madilnaeem0@gmail.com",        # Author's email address
    packages=find_packages(),                     # Automatically find and include all packages
    install_requires=[]                           # List of dependencies required for the application (currently empty)
)