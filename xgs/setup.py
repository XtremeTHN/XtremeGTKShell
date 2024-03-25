from setuptools import find_packages, setup

setup(
    name="xgs",
    packages=find_packages(),
    version="0.1.0",
    description="A python library for making a Gtk Shell with python. Inspired of Aylurs Gtk Shell",
    author="XtremeTHN",
    entry_points={
        "console_scripts": [
            'xgs = xgs.cli:main'
        ]
    },
    install_requires=["pygobject", "pygobject-stubs"]
)
