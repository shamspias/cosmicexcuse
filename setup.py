"""
Setup configuration for CosmicExcuse package
"""

import os

from setuptools import find_packages, setup

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from __version__.py
version = {}
with open(os.path.join("cosmicexcuse", "__version__.py")) as fp:
    exec(fp.read(), version)

setup(
    name="cosmicexcuse",
    version=version["__version__"],
    author="Shamsuddin Ahmed",
    author_email="info@shamspias.com",
    description="Generate quantum-grade excuses for your code failures using fake AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shamspias/cosmicexcuse",
    project_urls={
        "Bug Tracker": "https://github.com/shamspias/cosmicexcuse/issues",
        "Documentation": "https://cosmicexcuse.readthedocs.io/",
        "Source Code": "https://github.com/shamspias/cosmicexcuse",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Natural Language :: Bengali",
    ],
    python_requires=">=3.9",
    install_requires=[
        "typing-extensions>=4.0.0;python_version<'3.8'",
    ],
    extras_require={
        "dev": [
            "pytest>=8.4.1",
            "pytest-cov>=6.2.1",
            "black>=22.1.0",
            "flake8>=7.1.1",
            "mypy>=1.17.1",
            "sphinx>=8.1.3",
            "sphinx-rtd-theme>=3.0.2",
        ],
        "api": [
            "flask>=3.1.2",
            "fastapi>=0.116.1",
            "uvicorn>=0.30.6",
        ],
        "discord": [
            "discord.py>=2.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cosmicexcuse=cosmicexcuse.cli:main",
            "cosmic-excuse=cosmicexcuse.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cosmicexcuse": ["data/**/*.json"],
    },
    zip_safe=False,
    keywords=[
        "excuse",
        "generator",
        "quantum",
        "ai",
        "humor",
        "development",
        "error-handling",
        "markov-chain",
        "debugging",
        "comedy",
    ],
)
