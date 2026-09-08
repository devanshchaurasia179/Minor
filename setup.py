"""
Setup script for EMG Authentication System
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("config/requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="emg-authentication",
    version="1.0.0",
    author="Minor Project Team",
    description="EMG-Based Biometric Authentication System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/emg-authentication",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'emg-train=scripts.train_models:main',
            'emg-analyze=scripts.run_analysis:main',
            'emg-visualize=scripts.visualize:main',
        ],
    },
)
