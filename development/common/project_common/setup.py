from setuptools import setup, find_packages


setup(
    name='project-common',
    version='0.2.0',  # MAJOR.MINOR.PATCH format
    packages=find_packages(),
    description="Common utilities and pieces of code across the project.",
    author='Sale',
    author_email='sale.radenkovic@gmail.com',
    url='https://github.com/AREA4-Brunch',  # should be to iep coursework repo

    install_requires=[
        "Flask==2.3.2",
        "dependency-injector==4.41.0",
        "flask_app_extended>=1.1.0",
    ],
)
