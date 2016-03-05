from distutils.core import setup
from setuptools import find_packages

setup(
    name='hangpanels',
    version='0.1.0',
    url='https://github.com/merqurio/hangpanels',
    license='MIT',
    author='Gabriel de Maeztu',
    author_email='gabriel.maeztu@gmail.com',
    description='This is a python API to interact with Hanhouts export Log.',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.4'
                 ],
    packages=find_packages(exclude=['docs', 'test*']),
    install_requires=['pandas']
)
