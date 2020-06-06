import setuptools  # type: ignore

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="C-Mock-Generator",
    version="0.9.0",
    author="Björn Lange",
    author_email="bjoern.lange@tu-dortmund.de",
    description="A simple Mockito style oriented mock generator for C",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BjoernLange/C-Mock-Generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    package_data={
        '': ['resource/*.h', 'resource/*.c']
    },
    python_requires='>=3.6',
    license='MIT License',
    platforms=['Linux'],
)
