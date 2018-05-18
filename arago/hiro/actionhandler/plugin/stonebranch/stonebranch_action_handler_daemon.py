import logging
import os
from configparser import ConfigParser

from arago.pyactionhandler.capability import Capability

from arago.hiro.actionhandler.plugin.action_handler_daemon import ActionHandlerDaemon
from arago.hiro.actionhandler.plugin.stonebranch.action.stonebranch_exec_unix_command_action import \
    StonebranchExecUnixCommandAction
from arago.hiro.actionhandler.plugin.stonebranch.stonebranch_instance import StonebranchInstance
from arago.hiro.actionhandler.plugin.stonebranch.stonebranch_rest_client import StonebranchRestClient


class StonebranchActionHandlerDaemon(ActionHandlerDaemon):
    @property
    def short_name(self) -> str:
        return 'stonebranch'

    @property
    def display_name(self) -> str:
        return 'Stonebranch'

    def load_credentials(self):
        logger = logging.getLogger('root')
        credentials = ConfigParser()
        credentials_config_filename = '/opt/autopilot/conf/external_actionhandlers/%s-instances.conf' % self.short_name
        if os.path.isfile(credentials_config_filename):
            credentials.read(credentials_config_filename)
        else:
            logger.warning("Missing or unreadable instances configuration file: %s" % credentials_config_filename)

        for section in credentials.sections():
            self.credentials[section] = StonebranchRestClient(StonebranchInstance(
                host=credentials.get(section, 'host'),
                username=credentials.get(section, 'username'),
                password=credentials.get(section, 'password'),
            ))

    @property
    def capabilities(self) -> dict:
        return {
            "ExecuteCommand": Capability(StonebranchExecUnixCommandAction, client_repository=self.credentials)
        }

    @staticmethod
    def main() -> int:
        args = ActionHandlerDaemon.args()
        daemon = StonebranchActionHandlerDaemon(args)
        return daemon.control(args)
