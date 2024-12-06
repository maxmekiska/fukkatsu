import os

from setuptools import find_packages, setup

with open("README.md", encoding="utf8") as file:
    long_description = file.read()

setup(
    author="Maximilian Mekiska",
    author_email="maxmekiska@gmail.com",
    url="https://github.com/maxmekiska/fukkatsu",
    description="Dynamic Software Improvement and Mutation using LLMs for Stochastic Synthetic Code Injections.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="fukkatsu",
    version="0.0.14",
    packages=find_packages(include=["fukkatsu", "fukkatsu.*"]),
    install_requires=[
        "openai >= 1.56.0, <= 1.57.00",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords=["machinelearning", "llm", "runtime", "codecorrection"],
    python_requires=">= 3.9.0, < 3.13.0",
)
