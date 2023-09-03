from setuptools import setup, find_packages


setup(
    name='pypayment',
    version='0.1.0',  # MAJOR.MINOR.PATCH format
    description="Wrappers and utils for solidity smart contracts used for payment in the project.",
    author='Sale',
    author_email='sale.radenkovic@gmail.com',
    url='https://github.com/AREA4-Brunch',  # should be to iep coursework repo
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "web3>=6.9.0",
    ],
)
