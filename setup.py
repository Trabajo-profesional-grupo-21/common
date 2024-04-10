from setuptools import setup, find_packages

setup(
    name='common',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pika'
    ],
    author='TPP - G21',
    author_email='asegura@fi.uba.ar, msfontenla@fi.uba.ar, iiragui@fi.uba.ar, sfernandezc@fi.uba.ar',
    description='Modulos compartidos por nuestras apps',
    url='https://github.com/Trabajo-profesional-grupo-21/common',
)