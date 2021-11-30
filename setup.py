from setuptools import setup, find_packages

setup(
    name='code-20211129-rhysmansel',
    version='0.1.0',
    license='GNU GPL',
    author='Rhys Mansel',
    packages=find_packages(include=['tests', 'tests.*', 'src', 'src.*']),
    install_requires=['pandas==1.3.4'],
    entry_points={'console_scripts': ['bmi-gen=src.main:main']}
)
