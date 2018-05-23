from arago.hiro.actionhandler.plugin.stonebranch.rest_client import RestClient


class Task:
    def __init__(self, client: RestClient, name: str, parameters: map):
        self.client = client
        # type: RestClient
        self.name = name
        # type: str
        self.id = None
        # type: str

        if 'agent' in parameters:
            self.agent = parameters['agent']
        else:
            self.agent = None

        if 'agent_cluster' in parameters:
            self.agent_cluster = parameters['agent_cluster']
        else:
            self.agent_cluster = None

        if 'agent_cluster_broadcast' in parameters:
            self.agent_cluster_broadcast = parameters['agent_cluster_broadcast']
        else:
            self.agent_cluster_broadcast = None

        if 'Command' in parameters:
            self.command = parameters['Command']
        elif 'command' in parameters:
            self.command = parameters['command']
        else:
            self.command = None

        if 'arguments' in parameters:
            self.arguments = parameters['arguments']
        else:
            self.arguments = None

        if 'working_directory' in parameters:
            self.working_directory = parameters['working_directory']
        else:
            self.working_directory = None

        if 'success_exit_codes' in parameters:
            self.success_exit_codes = parameters['success_exit_codes']
        else:
            self.success_exit_codes = '0'
