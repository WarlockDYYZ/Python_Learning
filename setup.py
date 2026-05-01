from setuptools import setup, find_packages

setup(
   name="data_analyzer",
   version="0.1.0",
   packages=find_packages(),
   entry_points={
       'console_scripts': [
           'data-analyzer = data_analyzer.cli:main'
       ]
   },
   install_requires=[
       'pandas>=1.5.0',
       'numpy>=1.23.0',
       'matplotlib>=3.6.0',
       'scipy>=1.9.0'
   ]
)