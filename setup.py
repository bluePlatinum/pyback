import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    description="A simple backup utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bluePlatinum/pybacked",
    project_urls={
        "Bug Tracker": "https://github.com/bluePlatinum/pybacked/issues",
        "Documentation": "https://pybacked.readthedocs.io/"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": ["pybacked=pybacked.cli:main"]
    },
)
