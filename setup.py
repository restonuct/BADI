"""
Setup configuration for B.A.D.I.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="badi",
    version="0.1.0-alpha",
    author="B.A.D.I. Contributors",
    description="Balanced Autonomous Digital Intelligence - An open-source AI assistant framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/badi",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=[
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "click>=8.1.0",
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.23.0",
        "sqlalchemy>=2.0.0",
        "alembic>=1.12.0",
        "chromadb>=0.4.0",
        "llama-cpp-python>=0.2.0",
        "openai>=1.0.0",
        "anthropic>=0.18.0",
        "google-generativeai>=0.3.0",
        "httpx>=0.24.0",
        "aiofiles>=23.0.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.5.0",
            "pre-commit>=3.4.0",
        ],
        "voice": [
            "openai-whisper>=20230918",
            "faster-whisper>=0.10.0",
            "sounddevice>=0.4.6",
        ],
        "gpu": [
            "vllm>=0.2.0",
            "torch>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "badi=badi.cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
