import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="note-python",
    version="1.3.4",
    author="Blues Inc.",
    author_email="support@blues.com",
    description="Cross-platform Python Library for the Blues Wireless Notecard,",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blues/note-python",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    install_requires=["filelock"],
    python_requires='>=3.6',
)