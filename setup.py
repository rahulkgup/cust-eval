from setuptools import setup, find_packages

setup(
    name="cust-eval",
    version="0.1.0",
    author="Rahul Gupta",
    author_email="rahulkgup@gmail.com",
    description="A package for customer evaluation",
    packages=find_packages(),
    install_requires=[
        "lifetimes",
        "argparse",
        "pandas",
        "scipy",
    ],
    entry_points={
        "console_scripts": [
            "cust-eval=cust_eval.cli:main",
        ],
    },
)
