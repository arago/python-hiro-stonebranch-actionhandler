import logging
import time
import uuid

from arago.pyactionhandler.action import Action

from arago.hiro.actionhandler.plugin.stonebranch.stonebranch_rest_client import StonebranchRestClient
from arago.hiro.actionhandler.plugin.stonebranch.task import Task
from arago.hiro.actionhandler.plugin.stonebranch.task_instance import TaskInstance


class ActionResult:
    def __init__(self, task: Task) -> None:
        super().__init__()
        self.task = task  # type: Task
        self.message = None  # type: str
        self.instance = None  # type: TaskInstance


class StonebranchExecUnixCommandAction(Action):
    logger = logging.getLogger('StonebranchExecUnixCommandAction')

    def __init__(self, num, node, zmq_info, timeout, parameters, client_repository):
        super().__init__(num, node, zmq_info, timeout, parameters)
        self.client_repository = client_repository

    def __call__(self):
        instance_name = self.parameters['instance']
        client = self.client_repository[instance_name]
        action_result = self.exec_task(client, self.parameters)

        if action_result.message is not None:
            self.output = ''
            self.error_output = ''
            self.system_rc = 0
            self.statusmsg = action_result.message
            self.success = False
            return

        task_instance = action_result.instance
        self.output = task_instance.stdOut
        self.error_output = task_instance.stdErr
        self.system_rc = 0
        self.statusmsg = task_instance.status
        self.success = task_instance.success

    @staticmethod
    def exec_task(client: StonebranchRestClient, parameters: dict) -> ActionResult:
        logger = StonebranchExecUnixCommandAction.logger
        task = Task(client=client, name='HIRO action %s' % uuid.uuid1(), parameters=parameters)
        action_result = ActionResult(task)
        task_response = client.task_create(task)
        if task_response.status_code != 200:
            action_result.message = 'Task creation Failed'
        task_instance = client.task_launch(task)
        action_result.instance = task_instance
        status = 'UNKNOWN'
        final_status = ['FINISHED', 'CANCELLED', 'FAILED', 'SKIPPED', 'START_FAILURE', 'SUCCESS']
        first = True
        while not (status in final_status):
            status = client.task_instance_status(task_instance)
            logger.debug(status)
            if first:
                first = False
            else:
                time.sleep(3)
        task_instance.status = status
        # TODO
        # client.task_instance_info(task_instance)
        client.task_instance_output(task_instance)
        client.task_delete(task)
        return action_result
