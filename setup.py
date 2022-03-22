from distutils.core import setup
from setuptools import find_namespace_packages

VERSION = '0.1'

setup(
    name="tokyo-annotation",
    packages=find_namespace_packages(include=['tokyo_annotation.*']),
    version=VERSION,
    license="MIT",
    description="Tokyo Annotation",
    author="Dion Ricky Saputra",
    author_email="code@dionricky.com",
    url="https://github.com/dion-ricky/tokyo-annotation",
    keywords=["data annotation"],
    install_requires=[

    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)