import logging
import re
import requests

from arago.hiro.actionhandler.plugin.stonebranch.rest_client import RestClient
from arago.hiro.actionhandler.plugin.stonebranch.stonebranch_instance import StonebranchInstance
from arago.hiro.actionhandler.plugin.stonebranch.task import Task
from arago.hiro.actionhandler.plugin.stonebranch.task_instance import TaskInstance
from arago.hiro.actionhandler.plugin.stonebranch.task_instance_state import TaskInstanceState


class StonebranchRestClient(RestClient):

    def __init__(self, instance: StonebranchInstance):
        self.session = requests.Session()
        self.instance = instance
        self.session.auth = (instance.username, instance.password)
        self.logger = logging.getLogger(__name__)
        pass

    # https://www.stonebranch.com/confluence/display/UC64/Linux+Unix+Task+Web+Services#LinuxUnixTaskWebServices-CreateaLinux%2FUnixTask
    def task_create(self, task: Task) -> requests.models.Response:
        self.logger.info('Creating new task')

        json = {
            'type': 'taskUnix',
            'name': task.name,
            'command': task.command,
            'exitCodes': task.success_exit_codes,
        }
        if not (task.agent is None):
            json['agent'] = task.agent
        if not (task.agent_cluster is None):
            json['agentCluster'] = task.agent_cluster
        if not (task.agent_cluster_broadcast is None):
            json['broadcastCluster'] = task.agent_cluster_broadcast
        if not (task.arguments is None):
            json['parameters'] = task.arguments
        if not (task.working_directory is None):
            json['runtimeDir'] = task.working_directory

        response = self.session.post(
            url='https://%s/resources/task' % self.instance.authority,
            json=json,
        )
        if response.status_code == 200:
            match = re.match(pattern='Successfully created the (.+) task with id (.+).', string=response.text)
            task.id = match.group(2)
        else:
            self.logger.warning('Creating task failed')
        return response

    # https://www.stonebranch.com/confluence/display/UC64/Task+Web+Services#TaskWebServices-LaunchaTask
    def task_launch(self, task: Task) -> TaskInstance:
        self.logger.info('Launching new task instance')
        instance = TaskInstance(task)
        instance.state = TaskInstanceState.LAUNCH_PENDING
        self.logger.debug('Task launch pending')
        response = self.session.post(
            url='https://%s/resources/task/ops-task-launch' % self.instance.authority,
            json={'name': task.name, },
            headers={'Accept': 'application/json'},
        )
        if response.status_code == 200:
            response_json = response.json()
            if response_json['success']:
                instance.state = TaskInstanceState.LAUNCH_SUCCESS
                instance.id = response_json['sysId']
                self.logger.debug('Task launch success')
            else:
                instance.message = response_json['info']
                instance.state = TaskInstanceState.LAUNCH_FAILED
                self.logger.warning('Task launch failed')

            if response_json['errors'] != '':
                instance.message = response_json['errors']
        else:
            instance.state = TaskInstanceState.LAUNCH_FAILED
            self.logger.warning('Task launch failed')

        return instance

    # https://www.stonebranch.com/confluence/display/UC64/Task+Instance+Web+Services#TaskInstanceWebServices-TaskInstanceStatusTypes
    def task_instance_status(self, instance: TaskInstance):
        self.logger.info('Querying task instance status')
        response = self.session.post(
            url='https://%s/resources/taskinstance/list' % self.instance.authority,
            json={'sysId': instance.id, },
            headers={'Accept': 'application/json'},
        )
        if response.status_code == 200:
            response_json = response.json()
            return response_json[0]['status']
        else:
            self.logger.warning('Querying task instance status failed')
            return 'UNKNOWN'

    def task_instance_info(self, instance: TaskInstance):
        """Non functional since there is no documented REST end point for it yet"""
        self.logger.info('Querying task instance info')
        response = self.session.get(
            url='https://%s/resources/taskinstance/status' % self.instance.authority,
            params={'id': instance.id},
        )
        if response.status_code == 200:
            response_json = response.json()
            pass
        pass

    # https://www.stonebranch.com/confluence/display/UC64/Task+Instance+Web+Services#TaskInstanceWebServices-RetrieveTaskInstanceOutput
    def task_instance_output(self, instance: TaskInstance):
        self.logger.info('Querying task instance output')
        response = self.session.get(
            url='https://%s/resources/taskinstance/retrieveoutput' % self.instance.authority,
            params={'taskinstanceid': instance.id},
            headers={'Accept': 'application/json'},
        )
        if response.status_code == 200:
            response_json = response.json()
            std_out_idx = -1
            std_err_idx = -1
            for idx in range(len(response_json)):
                output = response_json[idx]
                if output['attemptCount'] != 1:
                    continue
                if output['outputType'] == 'STDOUT':
                    std_out_idx = idx
                if output['outputType'] == 'STDERR':
                    std_err_idx = idx
                pass

            instance.stdOut = response_json[std_out_idx]['outputData']
            instance.stdErr = response_json[std_err_idx]['outputData']
        else:
            self.logger.warning('Querying task instance output failed')

    # https://www.stonebranch.com/confluence/display/UC64/Task+Web+Services#TaskWebServices-DeleteaTask
    def task_delete(self, task: Task):
        self.logger.info('Deleting task')
        response = self.session.delete(
            url='https://%s/resources/task' % self.instance.authority,
            params={'taskid': task.id},
        )
        if response.status_code != 200:
            self.logger.warning('Deleting task failed')
