"""Python setup.py for ubahn_displayer package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("ubahn_displayer", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="ubahn_displayer",
    version=read("ubahn_displayer", "VERSION"),
    description="Awesome ubahn_displayer created by shanecolfer",
    url="https://github.com/shanecolfer/Ubahn-Displayer/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="shanecolfer",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["ubahn_displayer = ubahn_displayer.__main__:main"]
    },
    extras_require={"test": read_requirements("requirements-test.txt")},
)
