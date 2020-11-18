import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Webpt",
    version="2.2.5",
    install_requires=['requests', 'urllib3'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    author="Sahar Avitan",
    author_email="avitansahar@gmail.com",
    description="Library for penetration testing, website analysis and requests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saharavitan/webpt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
