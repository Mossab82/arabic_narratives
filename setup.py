from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="anar",
    version="1.0.0",
    author="Mossab Ibrahim",
    author_email="mibrahim@ucm.es",
    description="Arabic Narrative Analysis and Recognition System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mossab82/arabic_narratives",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.0",
        "networkx>=2.5",
        "torch>=1.8.0",
        "transformers>=4.5.0",
        "fastapi>=0.65.0",
        "pydantic>=1.8.0",
        "uvicorn>=0.13.0",
        "pytest>=6.0.0",
        "pytest-asyncio>=0.15.0"
    ],
    extras_require={
        "dev": [
            "black",
            "isort",
            "mypy",
            "pytest-cov"
        ]
    },
    include_package_data=True,
    package_data={
        "anar": [
            "data/*.json",
            "models/*.pt"
        ]
    }
)
