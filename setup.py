#!/usr/bin/env python3
"""
Setup script for Walmart Product Content Generator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="walmart-content-generator",
    version="1.0.0",
    author="Walmart Content AI Team",
    author_email="dev@walmart-ai.com",
    description="AI-powered Walmart product content generator with Ollama and OpenAI support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yusuf44777/walmart_project_last",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "ollama": [
            "requests>=2.31.0",
        ],
        "openai": [
            "openai>=1.35.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "walmart-content=walmart:main",
            "walmart-train=create_walmart_model:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.json"],
    },
    keywords="walmart, ai, content-generation, ollama, openai, product-descriptions, e-commerce",
    project_urls={
        "Bug Reports": "https://github.com/yusuf44777/walmart_project_last/issues",
        "Source": "https://github.com/yusuf44777/walmart_project_last",
        "Documentation": "https://github.com/yusuf44777/walmart_project_last/wiki",
    },
)
