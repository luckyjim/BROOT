from setuptools import setup
import sys

# sys.path.append('shower_radio/src')

import broot

setup(
    name="BROOT",
    description="Viewer for CERN format ROOT",
    version=sradio.__version__,
    author=sradio.__author__,
    classifiers=[
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    url="https://github.com/grand-mother/NUTRIG1",
    package_dir={"broot": "src/broot"},
    scripts=["src/broot_main.py"],
    license='MIT',
    python_requires='>=3.8',
    install_requires=["appJar", "matplotlib", "uproot", "numpy"]
)
