#!/usr/bin/env python
import os
import distutils.core

if os.environ.get('USER', '') == 'vagrant':
    del os.link

distutils.core.setup(
    name='arago-hiro-actionhandler-stonebranch',
    version='0.1.0',
    author='Johannes Harth',
    author_email='jharth@arago.co',
    description='Arago HIRO ActionHandler plugin for Stonebranch',
    license='MIT',
    url='https://github.com/arago/python-hiro-stonebranch-actionhandler',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Environment :: Plugins',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    packages=[
        'arago.hiro.actionhandler.plugin.stonebranch',
    ],
    install_requires=[
        'arago-common-base',
    ],
)
