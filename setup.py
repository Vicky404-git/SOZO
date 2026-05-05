from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="sozo",
    version="1.0.0",  # <-- Officially v1.0.0!
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sozo=sozo.main:main",
        ],
    },
)
