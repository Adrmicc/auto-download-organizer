from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="auto-download-organizer",
    version="1.0.0",
    author="Adrmicc",
    description="Automatic file organizer for Downloads folder with duplicate cleaning and logging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Adrmicc/auto-download-organizer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "click>=8.1.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "organize=src.cli:main",
        ],
    },
)
