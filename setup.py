from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cobol-copybook-to-json",
    version="1.1.0",
    author="Arunkumar Selvam",  # Replace with your name
    author_email="aruninfy123@gmail.com",  # Replace with your email
    description="Convert COBOL copybooks to JSON schema format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arunkumars-mf/cobol-copybook-to-json",  # Replace with your repo URL
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: XML",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies based on your code
    ],
    entry_points={
        "console_scripts": [
            "cobol-to-json=cobol_copybook_to_json:main",
        ],
    },
    keywords="cobol copybook json schema converter mainframe",
    project_urls={
        "Bug Reports": "https://github.com/arunkumars-mf/cobol-copybook-to-json/issues",
        "Source": "https://github.com/arunkumars-mf/cobol-copybook-to-json",
    },
)
