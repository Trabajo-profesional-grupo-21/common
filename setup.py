from setuptools import setup

setup(
    name='common',
    version='0.1',
    packages=['connection'],
    install_requires=[
        'pika'
    ],
    author='TPP - G21',
    author_email='asegura@fi.uba.ar, msfontenla@fi.uba.ar, iiragui@fi.uba.ar, sfernandezc@fi.uba.ar',
    description='Modulos compartidos por nuestras apps',
    url='https://github.com/Trabajo-profesional-grupo-21/common',
)