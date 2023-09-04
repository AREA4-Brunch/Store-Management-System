from setuptools import setup, find_packages


setup(
    name='db-store-management',
    version='1.2.0',  # MAJOR.MINOR.PATCH format
    packages=find_packages(),
    description="Models and structure of `store_management` database.",
    author='Sale',
    author_email='sale.radenkovic@gmail.com',
    url='https://github.com/AREA4-Brunch',  # should be to iep coursework repo

    install_requires=[
        "Flask-SQLAlchemy",
    ],
)
