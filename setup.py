# -*- coding: utf-8 -*-
# Created by CaoDa on 2019/4/30

from setuptools import setup, find_packages, Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension(
        "searcher",  # location of the resulting .so
        ["searcher.pyx"]
    )
]

setup(
    name='IP To Region',
    packages=find_packages(),
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
)
