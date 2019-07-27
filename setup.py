import setuptools
import inspect
import sys
import os

requirements = [
    'beautifulsoup4==4.7.1',
    'lxml==4.3.3',
    'soupsieve==1.9.1',
    'PyInquirer==1.0.3'
]

VERSION_PATH = os.path.join(os.path.dirname(__file__), 'VERSION')
with open(VERSION_PATH, 'r') as version_file:
    VERSION = version_file.read().strip()

README_PATH = os.path.join(os.path.dirname(__file__), 'README.rst')
with open(README_PATH, 'r') as readme_file:
    LONG_DESCRIPTION = readme_file.read().strip()

setuptools.setup(
    name='find-recipes',
    version=VERSION,
    description='find-recipes: Command line application for searching and consulting recipes by filtering by ingredient',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',
    url='https://github.com/y4izus/find-recipes',
    author='Yaiza García',
    license='MIT',
    classifiers=[
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Spanish',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Healthcare Industry',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.7'
    ],
    packages=setuptools.find_packages(exclude=['test*']),
    install_requires=requirements,
    python_requires='>=3.7',
    entry_points={
        'console_scripts': ['find-recipes=find_recipes:main'],
    }
)
