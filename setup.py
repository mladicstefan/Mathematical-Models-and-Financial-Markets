from setuptools import setup, find_packages

setup(
    name="fintech",
    version="0.2",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
