from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyditor",
    version="0.1.3",
    author="sshu2017",
    author_email="sshu2017@yahoo.com",
    description="A minimalist Python runner for coding interviews",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sshu2017/pyditor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "pyditor=pyditor.__main__:main",
        ],
    },
    keywords="python editor runner coding interview tkinter",
    project_urls={
        "Bug Reports": "https://github.com/sshu2017/pyditor/issues",
        "Source": "https://github.com/sshu2017/pyditor",
    },
)
