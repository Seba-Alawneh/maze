from setuptools import setup, find_packages

setup(
    name="mazegen",
    version="1.0.0",
    description="Maze generator for 42 A-Maze-ing project",
    author="habu-har & salalawn",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.10",
)
