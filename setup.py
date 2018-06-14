import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="flask-conf",
  version="0.0.1",
  author="Thong Nguyen",
  author_email="ikumen@gnoht.com",
  description="A little package for managing Flask configurations.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ikumen/flask-conf",
  packages=setuptools.find_packages(),
  install_requires=['yaml'],
  classifiers=(
    "Programming Language :: Python :: 2",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ),
)