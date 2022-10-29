#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Giorgio Zoppi",
    author_email='giorgio.zoppi@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="SharedProcessPool is package that implements embarassing parallel using shared memory this will avoid pickling from input and output data.",
    entry_points={
        'console_scripts': [
            'sharedprocesspool=sharedprocesspool.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sharedprocesspool',
    name='sharedprocesspool',
    packages=find_packages(include=['sharedprocesspool', 'sharedprocesspool.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/giorgiozoppi/sharedprocesspool',
    version='0.1.0',
    zip_safe=False,
)
