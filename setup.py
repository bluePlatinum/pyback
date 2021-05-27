import setuptools
from pybacked import __version__


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybacked",
    version=__version__,
    author="Roko Jukic",
    author_email="jukic.rok@gmail.com",
    description="a simple backup utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bluePlatinum/pybacked",
    project_urls={
        "Bug Tracker": "https://github.com/bluePlatinum/pybacked/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
