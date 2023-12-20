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
    version="0.0.12",
    packages=find_packages(include=["fukkatsu", "fukkatsu.*"]),
    install_requires=[
        "setuptools >= 41.0.0",
        "openai >= 0.27.5, <= 0.28",
        "google-generativeai >= 0.3.1, <= 0.4.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords=["machinelearning", "llm", "runtime", "codecorrection"],
    python_rquieres=">= 3.9.0, <= 3.11.0",
)
