"""
    Setup file for vibegame.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.6.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""

from setuptools import setup, find_packages

setup(
    name="vibegame",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pygame",
        "pyxel",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "vibegame=vibegame.game:main",
        ],
    },
)
