import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="navierstokes-petch",
    version="0.0.7",
    author="Petr Zakharov",
    author_email="zapetch@gmail.com",
    description="Navier-Stokes solvers and problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/petch/navier-stokes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)