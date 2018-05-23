import logging

from arago.hiro.actionhandler.plugin.stonebranch import StonebranchRestClient, StonebranchInstance
from arago.hiro.actionhandler.plugin.stonebranch.action import StonebranchExecUnixCommandAction

clientRepository = {}
clientRepository['prototype'] = StonebranchRestClient(StonebranchInstance(
    host='stonebranch.cloud',
    username='username',
    password='password',
))


def test():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('test')

    client = clientRepository['prototype']
    StonebranchExecUnixCommandAction.exec_task(client, {
        'instance': 'prototype',
        'agent': 'name',
        'command': 'true',
    })

    logger.info('done')


test()
