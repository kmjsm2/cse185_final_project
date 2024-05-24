import os
from setuptools import setup, find_packages

# version-keeping code based on pybedtools
curdir = os.path.abspath(os.path.dirname(__file__))
MAJ = 0
MIN = 0
REV = 0
VERSION = '%d.%d.%d' % (MAJ, MIN, REV)
with open(os.path.join(curdir, 'gene_vis/version.py'), 'w') as fout:
        fout.write(
            "\n".join(["",
                       "# THIS FILE IS GENERATED FROM SETUP.PY",
                       "version = '{version}'",
                       "__version__ = version"]).format(version=VERSION)
        )


setup(
    name='gene_vis',
    version=VERSION,
    description='CSE185 Project create scatter and volcano plot for gene.results file',
    author='Nayoung Kim, MyungJoo Kim, Soyeon Lee',
    author_email='nak003@ucsd.edu, myk001@ucsd.edu, sol020@ucsd.edu',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "gene_vis=gene_vis.gene_vis:main"
        ],
    },
)