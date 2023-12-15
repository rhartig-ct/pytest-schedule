import codecs
import os

from setuptools import find_packages, setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-schedule",
    version="0.1.3",
    author="Cipher Tech Solutions, Inc",
    author_email="opensource@ciphertechsolutions.com",
    maintainer="Cipher Tech Solutions, Inc",
    maintainer_email="opensource@ciphertechsolutions.com",
    license="MIT",
    url="https://github.com/ciphertechsolutions/pytest-schedule",
    description="Sort tests by their previous execution time and partition them into roughly equal groups",
    long_description=read("README.rst"),
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["pytest>=7.0.0", "pytest-xdist>=3.1.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "pytest11": [
            "schedule = pytest_schedule.hooks",
        ],
    },
)
