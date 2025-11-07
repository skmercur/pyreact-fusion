"""
PyReact Fusion Template - Setup Configuration
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pyreact-fusion",
    version="1.0.0",
    author="Sofiane Khoudour",
    author_email="khoudoursofiane75@gmail.com",
    description="A production-ready full-stack application template with Python FastAPI backend and React frontend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skmercur/pyreact-fusion",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pyreact-fusion=backend.main:main",
        ],
    },
)

