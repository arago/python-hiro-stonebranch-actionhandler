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
    entry_points={
        'console_scripts': [
            'stonebranch-actionhandler = arago.hiro.actionhandler.plugin.stonebranch.StonebranchActionHandlerDaemon:main',
        ],
    },
    namespace_packages=[
        'arago',
        'arago.hiro',
        'arago.hiro.actionhandler',
        'arago.hiro.actionhandler.plugin',
        'arago.hiro.actionhandler.plugin.stonebranch',
        'arago.hiro.actionhandler.plugin.stonebranch.action',
    ],
    install_requires=[
        'arago-common-base',
        'arago-pyactionhandler',
        'requests',
    ],
    dependency_links=[
        'git+https://github.com/arago/python-arago-common.git@96c1618fc8ab861951930f768d02cb25e2adf9dd#egg=arago-common-base',
        'git+https://github.com/arago/python-arago-pyactionhandler.git@25bed7c011f86615d97ec366c806c5269089aedd#egg=arago-pyactionhandler',
    ],
)
