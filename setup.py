import os

from setuptools import find_packages, setup

with open("README.md", encoding="utf8") as file:
    long_description = file.read()

setup(
    author="Maximilian Mekiska",
    author_email="maxmekiska@gmail.com",
    url="https://github.com/maxmekiska/fukkatsu",
    description="A python library for runtime LLM supported code corrections.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="fukkatsu",
    version="0.0.11",
    packages=find_packages(include=["fukkatsu", "fukkatsu.*"]),
    install_requires=[
        "setuptools >= 41.0.0",
        "openai >= 0.27.5, <= 0.28",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords=["machinelearning", "llm", "runtime", "codecorrection"],
    python_rquieres=">= 3.7.0, <= 3.11.0",
)
