#!/usr/bin/env python
import os
import distutils.core

if os.environ.get('USER', '') == 'vagrant':
    del os.link

distutils.core.setup(
    name='arago-hiro-actionhandler-stonebranch',
    version='1.0.0',
    author='Johannes Harth',
    author_email='jharth@arago.co',
    description='Arago HIRO ActionHandler plugin for Stonebranch',
    license='MIT',
    url='https://github.com/arago/python-hiro-stonebranch-actionhandler',
    python_requires='>=3.4',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Environment :: Plugins',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'stonebranch-actionhandler ='
            ' arago.hiro.actionhandler.plugin.stonebranch.StonebranchActionHandlerDaemon:StonebranchActionHandlerDaemon.main',
        ],
    },
    packages=[
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
        'git+https://github.com/arago/python-arago-common.git@96c1618fc8ab861951930f768d02cb25e2adf9dd#egg=arago-common-base-2.1',
        'git+https://github.com/166MMX/python-arago-pyactionhandler.git@abd1f97975e64269f88940d9ecfebc07e4e76d20#egg=arago-pyactionhandler-2.5',
    ],
    scripts=[
        'bin/hiro-stonebranch-actionhandler.py'
    ],
    data_files=[
        (
            '/opt/autopilot/conf/external_actionhandlers/',
            [
                'config/external_actionhandlers/stonebranch-actionhandler.conf',
                'config/external_actionhandlers/stonebranch-instances.conf',
                'config/external_actionhandlers/stonebranch-actionhandler-log.conf',
            ],
        ),
        (
            '/opt/autopilot/conf/external_actionhandlers/capabilities/',
            [
                'config/external_actionhandlers/capabilities/stonebranch-actionhandler.yaml'
            ],
        ),
        (
            '/etc/init.d/', [
                'etc/init.d/hiro-stonebranch-actionhandler'
            ],
        )
    ],
)
