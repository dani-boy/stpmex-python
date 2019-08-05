import setuptools

install_requires = [
    'zeep>=3.1.0,<3.2.0',
    'pyopenssl>=18.0.0,<18.1.0',
    'clabe>=0.2.1,<0.3.0',
    'pydantic>=0.31.1<0.32.0'
]

# dataclasses is currently only builtin for 3.7. There is a backport on PyPi.
# There may be an official backport in the future, which is why we don't just
# check the python version.
try:
    import dataclasses
except ModuleNotFoundError:
    install_requires.append('dataclasses')

test_requires = ['pytest', 'pytest-vcr', 'pycodestyle', 'pytest-cov',
                 'black', 'isort[pipfile]']

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='stpmex',
    version='2.0.0',
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='Integration to stpmex.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/stpmex-python',
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
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
