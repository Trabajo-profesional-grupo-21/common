from setuptools import setup, find_packages

setup(
    name='common',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'pika',
    ],
    author='TPP - G21',
    author_email='',
    description='Modulos compartidos por nuestras apps',
    url='https://github.com/Trabajo-profesional-grupo-21/common',
)