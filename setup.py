from setuptools import setup, find_packages

setup(
    name="sozo",
    version="0.1",
    packages=find_packages(),
    install_requires=["typer", "rich", "dateparser"],
    entry_points={
        "console_scripts": [
            "sozo=sozo.main:main",
        ],
    },
)