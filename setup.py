from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = 'v0.1.2'
DESCRIPTION = 'ConPhar'
#LONG_DESCRIPTION = ''

# Setting up
setup(
    name="conphar",
    version=VERSION,
    author="Angel J. Ruiz-Moreno",
    author_email="<angel.j.ruiz.moreno@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'plotly','numpy', 'matplotlib', 'seaborn', 'pymol','scikit-learn'],
    keywords=['python', 'pharmacophore', 'drugdesign', 'cheminformatics', 'chemoinformatics', 'protein'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
    include_package_data=True,
    package_data={'': ['bin/*']},
)