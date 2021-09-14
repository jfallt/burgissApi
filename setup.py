from pkg_resources import Requirement, resource_filename
from setuptools import setup, find_packages
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


VERSION = '0.0.1'
DESCRIPTION = 'An api request package for Burgiss'
LONG_DESCRIPTION = 'A package that makes it easy to make requests to the Burgiss API by simplifying the JWT token auth and various endpoints'

setup(
    name="burgiss-api",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Jared Fallt",
    author_email="fallt.jared@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    keywords='burgiss',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
