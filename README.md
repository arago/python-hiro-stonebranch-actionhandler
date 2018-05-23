# Python 3 HIRO Stonebranch action handler

An action handler implementation for HIRO using the REST interface of Stonebranch.

Currently implemented interfaces
* Create a Linux/Unix Task
* Launch a Task
* Retrieve Task Instance Status
* Retrieve Task Instance Output
* Delete a Task

New Tasks can be setup against an agent and/or agent-cluster or broadcast

## Getting started

- [Python 3.4](https://github.com/pyenv/pyenv)
- [Create Virtual Environment](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments)
- `pip install git+https://github.com/arago/python-arago-common.git#egg=arago-common-base`
- `pip install git+https://github.com/arago/python-arago-pyactionhandler.git#egg=arago-pyactionhandler`
- [Install a list of requirements specified in a Requirements File.](https://packaging.python.org/tutorials/installing-packages/#requirements-files)
- [Package project](https://packaging.python.org/tutorials/distributing-packages/#packaging-your-project)

## Building with pex
```
virtualenv pex
./pex/bin/pip install pex

virtualenv build
./build/bin/pip install --upgrade pip wheel
./build/bin/pip wheel --wheel-dir=./wheelhouse --process-dependency-links git+https://github.com/arago/python-hiro-stonebranch-actionhandler.git#egg=arago-hiro-actionhandler-stonebranch

./pex/bin/pex "--python-shebang=/usr/bin/env python3" --no-index --find-links=wheelhouse arago-hiro-actionhandler-stonebranch --entry-point=arago.hiro.actionhandler.plugin.stonebranch.StonebranchActionHandlerDaemon:StonebranchActionHandlerDaemon.main --output-file=stonebranch-actionhandler.pex
```

## Test
```
PYTHONPATH="$(pwd):$PYTHONPATH" venv/bin/python3 bin/hiro-stonebranch-actionhandler.py --handler-config-file=ah_test/stonebranch-actionhandler.conf --logging-config-file=ah_test/stonebranch-actionhandler-log.conf --instances-config-file=ah_test/stonebranch-instances.conf --debug start
venv/bin/ah-client.py -u tcp://localhost:7292 --parameter instance = example --parameter agent = 'LINUX-AGNT0001' --parameter command = 'curl --help' a::b::c::d
```