from setuptools import setup, find_packages
import veniq # use veniq
import os # use os
import sys # use sys

setup(
    name='veniq',
    version=veniq.__version__,
    description=veniq.__doc__.strip(),
    long_description='Veniq uses Machine Learning '
                     'to analyze source code, find possible refactorings, '
                     'and suggest those that seem optimal',
    url='https://github.com/cqfn/veniq',
    download_url='https://github.com/cqfn/veniq',
    author=veniq.__author__,
    author_email=['katya.garmash@gmail.com', 'vitasprotas@gmail.com'],
    license=veniq.__licence__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'veniq = veniq.__main__:main'
        ],
    },
    extras_require={},
    install_requires=open('requirements.txt', 'r').readlines(),
    tests_require=open('requirements.txt', 'r').readlines(),
    classifiers=[
        'Programming Language :: Python',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ]
)
