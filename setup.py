from setuptools import setup, find_packages

setup(
    name="quickfilereader",
    version="0.1.0",
    description="A library for reading files in one line.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Manu Adam Akimidis",
    author_email="manu.softwareengineer@gmail.com",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approaved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["PyPDF2>=3.0.1", "Spire.Doc>=12.7.1", "pandas>=2.2.3"]
    
)