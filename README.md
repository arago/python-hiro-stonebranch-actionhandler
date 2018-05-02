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

- [Create Virtual Environment](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments)
- `pip install git+https://github.com/arago/python-arago-common.git#egg=arago-common-base`
- `pip install git+https://github.com/arago/python-arago-pyactionhandler.git#egg=arago-pyactionhandler`
- [Install a list of requirements specified in a Requirements File.](https://packaging.python.org/tutorials/installing-packages/#requirements-files)
- [Package project](https://packaging.python.org/tutorials/distributing-packages/#packaging-your-project)