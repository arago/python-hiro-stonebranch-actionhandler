import logging

from arago.hiro.actionhandler.plugin.stonebranch import StonebranchAction, StonebranchRestClient, StonebranchInstance

StonebranchAction.clientRepository['prototype'] = StonebranchRestClient(StonebranchInstance(
    host='stonebranch.cloud',
    username='username',
    password='password',
))


def test():
    logging.basicConfig(level=logging.DEBUG)

    StonebranchAction.exec_task({
        'instance': 'prototype',
        'agent': 'name',
        'command': 'true',
    })

    logging.info('done')


test()
