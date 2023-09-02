from setuptools import setup, find_packages


setup(
    name='flask-app-extended',
    version='1.1.2',  # MAJOR.MINOR.PATCH format
    packages=find_packages(),
    description="Library for creating a flask.Flask object and managing configurations.",
    author='Sale',
    author_email='sale.radenkovic@gmail.com',
    url='https://github.com/AREA4-Brunch',  # should be to iep coursework repo

    install_requires=[
        "Flask>=0.11",
    ],
)
