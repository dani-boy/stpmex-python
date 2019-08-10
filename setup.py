import codecs
import os
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


# from: https://packaging.python.org/guides/single-sourcing-package-version/
def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


# from: https://packaging.python.org/guides/single-sourcing-package-version/
def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


install_requires = [
    'zeep>=3.1.0,<3.2.0',
    'pyopenssl>=18.0.0,<18.1.0',
    'clabe>=0.2.1,<0.3.0',
    'pydantic>=0.31.1<0.32.0',
    'dataclasses>=0.6;python_version<"3.7"',
]

test_requires = [
    'pytest',
    'pytest-vcr',
    'pycodestyle',
    'pytest-cov',
    'black',
    'isort[pipfile]',
]

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='stpmex',
    version=find_version('stpmex', '__init__.py'),
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Client library for stpmex.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/stpmex-python',
    packages=['stpmex'],
    package_data=dict(stpmex=['py.typed']),
    python_requires='>=3.6',
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=test_requires,
    extras_require=dict(test=test_requires),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
