import setuptools

with open("README.txt", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="flask-cfg",
  version="0.0.6",
  author="Thong Nguyen",
  author_email="thong@gnoht.com",
  description="A little package for loading Flask configurations from YAML files.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ikumen/flask-cfg",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 2",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)