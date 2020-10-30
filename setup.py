import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webpt", 
    version="1.2.1",
    author="Sahar Avitan",
    author_email="avitansahar@gmail.com",
    description="Library for website analysis and requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saharavitan/webpt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
