import logging
import time
import uuid

from arago.pyactionhandler.action import Action

from arago.hiro.actionhandler.plugin.stonebranch.stonebranch_rest_client import StonebranchRestClient
from arago.hiro.actionhandler.plugin.stonebranch.task import Task
from arago.hiro.actionhandler.plugin.stonebranch.task_instance import TaskInstance


class StonebranchExecUnixCommandAction(Action):
    def __init__(self, num, node, zmq_info, timeout, parameters, client_repository):
        super().__init__(num, node, zmq_info, timeout, parameters)
        self.client_repository = client_repository

    def __call__(self):
        instance_name = self.parameters['instance']
        client = self.client_repository[instance_name]
        task_instance = self.exec_task(client, self.parameters)

        self.output = task_instance.stdOut
        self.error_output = task_instance.stdErr
        self.system_rc = 0
        self.statusmsg = task_instance.status
        self.success = task_instance.success
        pass

    @staticmethod
    def exec_task(client: StonebranchRestClient, parameters: dict) -> TaskInstance:
        task = Task(client=client, name='HIRO action %s' % uuid.uuid1(), parameters=parameters)
        client.task_create(task)
        task_instance = client.task_launch(task)
        status = 'UNKNOWN'
        final_status = ['FINISHED', 'CANCELLED', 'FAILED', 'SKIPPED', 'START_FAILURE', 'SUCCESS']
        first = True
        while not (status in final_status):
            status = client.task_instance_status(task_instance)
            logging.debug(status)
            if first:
                first = False
            else:
                time.sleep(3)
                del first
        task_instance.status = status
        # TODO
        # client.task_instance_info(task_instance)
        client.task_instance_output(task_instance)
        client.task_delete(task)
        return task_instance
