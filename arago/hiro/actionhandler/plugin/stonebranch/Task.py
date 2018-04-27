from arago.hiro.actionhandler.plugin.stonebranch import RestClient


class Task:
    def __init__(self, client: RestClient, name: str, parameters: map):
        self.client: RestClient = client
        self.name = name
        self.id: str = None

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

        if 'command' in parameters:
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
