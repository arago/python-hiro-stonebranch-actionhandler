import logging
import time
import uuid

from arago.pyactionhandler.action import Action

from arago.hiro.actionhandler.plugin.stonebranch import TaskInstance, Task


class StonebranchAction(Action):
    clientRepository = {}
    # type: dict

    def __call__(self):
        task_instance = self.exec_task(self.parameters)

        self.output = task_instance.stdOut
        self.error_output = task_instance.stdErr
        self.system_rc = 0
        self.statusmsg = task_instance.status
        self.success = task_instance.success
        pass

    @staticmethod
    def exec_task(parameters: dict) -> TaskInstance:
        instance_name = parameters['instance']
        client = StonebranchAction.clientRepository[instance_name]
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
