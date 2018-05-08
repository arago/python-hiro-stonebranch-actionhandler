from configparser import ConfigParser

from arago.pyactionhandler.capability import Capability

from arago.hiro.actionhandler.plugin import ActionHandlerDaemon
from arago.hiro.actionhandler.plugin.stonebranch import StonebranchRestClient, StonebranchInstance
from arago.hiro.actionhandler.plugin.stonebranch.action import StonebranchExecUnixCommandAction


class StonebranchActionHandlerDaemon(ActionHandlerDaemon):
    @property
    def short_name(self) -> str:
        return 'stonebranch'

    @property
    def display_name(self) -> str:
        return 'Stonebranch'

    def load_credentials(self):
        credentials = ConfigParser()
        for section in credentials.sections():
            self.credentials[section] = StonebranchRestClient(StonebranchInstance(
                host=credentials.get(section, 'host'),
                username=credentials.get(section, 'username'),
                password=credentials.get(section, 'password'),
            ))

    @property
    def capabilities(self) -> dict:
        self.credentials = ConfigParser()
        self.credentials.sections()
        self.credentials.keys()
        client_repository = {}
        return {
            "ExecuteCommand": Capability(StonebranchExecUnixCommandAction, client_repository=client_repository)
        }

    @staticmethod
    def main() -> int:
        args = ActionHandlerDaemon.args()
        daemon = StonebranchActionHandlerDaemon(args['--pidfile'], debug=args['--debug'])
        daemon.control(args)
        return 0
