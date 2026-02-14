from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="agentic-infrastructure-framework",
    version="0.1.0",
    author="DuggyBoi",
    author_email="keaganduggan@gmail.com",
    description="A comprehensive Python framework for building autonomous agents with CrewAI and LangChain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Duggyboi/agentic-infrastructure-framework",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
)
