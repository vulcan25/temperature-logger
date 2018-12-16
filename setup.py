# -*- coding: utf-8 -*-

from setuptools import setup

from temperature_logger import __version__


REPOSITORY = 'https://github.com/vulcan25/temperature-logger'

setup(
    name='temperature-logger',
    version=__version__,
    description='A temperature logging client for flask, works on Raspberrypi with the DS18B20.',
    author='vulcan25',
    #author_email='',
    url=REPOSITORY,
    download_url='{}/tarball/{}'.format(REPOSITORY, __version__),
    modules=['temperature_logger'],
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    license='MIT',
    keywords=['Raspberry pi']
)