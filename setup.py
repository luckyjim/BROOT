from setuptools import setup
import sys

sys.path.append('src')

import broot

setup(
    name="BROOT",
    description="Browser for ROOT files from CERN collaboration.",
    version=broot.__version__,
    author=broot.__author__,
    classifiers=[
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    url="https://github.com/luckyjim/BROOT",
    package_dir={"broot": "src/broot"},
    scripts=["script/BROOT.py"],
    license='MIT',
    python_requires='>=3.7',
    install_requires=["appJar", "matplotlib", "uproot", "numpy","scipy"]
)
