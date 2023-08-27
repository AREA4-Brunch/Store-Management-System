from setuptools import setup, find_packages


setup(
    name='std-authentication',
    version='0.3.0',  # MAJOR.MINOR.PATCH format
    packages=find_packages(),
    description="User authentication and role-based access control checks and their setup, shared among services relying on the store's `user_management_system`.",
    author='Sale',
    author_email='sale.radenkovic@gmail.com',
    url='https://github.com/AREA4-Brunch',  # should be to iep coursework repo

    install_requires=[
        "redis==5.0.0",
        "Flask==2.3.2",
        "Flask-JWT-Extended==4.5.2",
    ],
)
