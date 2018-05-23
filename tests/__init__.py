import logging

from arago.hiro.actionhandler.plugin.stonebranch.action.stonebranch_exec_unix_command_action import \
    StonebranchExecUnixCommandAction
from arago.hiro.actionhandler.plugin.stonebranch.stonebranch_instance import StonebranchInstance
from arago.hiro.actionhandler.plugin.stonebranch.stonebranch_rest_client import StonebranchRestClient

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
