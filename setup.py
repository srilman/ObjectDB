from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="objectdb",
      version="0.0.1",
      author="Srinivas Lade",
      author_email="srinulade1@gmail.com",
      license="MIT",
      description="Simple File-Based Database for Data Structures",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/srilman/ObjectDB",
      packages=["object_db"],
      classifiers=(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ),
      )
