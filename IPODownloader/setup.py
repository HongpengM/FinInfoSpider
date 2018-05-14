import os
from setuptools import find_packages, setup

print(os.path.join(os.path.dirname(__file__), 'readme.md'))
with open(os.path.join(os.path.dirname(__file__), 'readme.md'), encoding='utf-8') as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='pubCompany',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple spider to search and download public company files.',
    long_description=README,
    url='https://www.example.com/',
    author='Hongpeng M',
    author_email='mahongpengmars@163.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Spider',
    ],
)
