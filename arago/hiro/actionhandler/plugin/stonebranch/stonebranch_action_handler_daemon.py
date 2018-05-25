import logging
import os
import sys
from configparser import ConfigParser

from arago.pyactionhandler.capability import Capability

from arago.hiro.actionhandler.plugin.action_handler_daemon import ActionHandlerDaemon
from arago.hiro.actionhandler.plugin.docopt_builder import DocoptBuilder
from arago.hiro.actionhandler.plugin.stonebranch.action.stonebranch_exec_unix_command_action import \
    StonebranchExecUnixCommandAction
from arago.hiro.actionhandler.plugin.stonebranch.stonebranch_instance import StonebranchInstance
from arago.hiro.actionhandler.plugin.stonebranch.stonebranch_rest_client import StonebranchRestClient


class StonebranchActionHandlerDaemon(ActionHandlerDaemon):
    SHORT_NAME = 'stonebranch'
    DISPLAY_NAME = 'Stonebranch'
    logger = logging.getLogger('root')

    @property
    def short_name(self) -> str:
        return self.SHORT_NAME

    @property
    def display_name(self) -> str:
        return self.DISPLAY_NAME

    def load_credentials(self):
        credentials = ConfigParser()
        if '--instances-config-file' in self.args:
            credentials_config_filename = self.args['--instances-config-file']
        else:
            credentials_config_filename = '/opt/autopilot/conf/external_actionhandlers/%s-instances.conf' % self.short_name
        if os.path.isfile(credentials_config_filename):
            credentials.read(credentials_config_filename)
        else:
            self.logger.warning("Missing or unreadable instances configuration file: %s" % credentials_config_filename)

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
    def docopt_builder(builder=DocoptBuilder()) -> DocoptBuilder:
        builder = ActionHandlerDaemon.docopt_builder(builder)
        builder.options.append('--instances-config-file=FILE\tbaz [default: /opt/autopilot/conf/external_actionhandlers/{short_name}-actionhandler-log.conf]')
        return builder

    @staticmethod
    def main() -> int:
        args = StonebranchActionHandlerDaemon.docopt_builder().build(
            program_name=os.path.basename(sys.argv[0]),
            short_name=StonebranchActionHandlerDaemon.SHORT_NAME
        )
        daemon = StonebranchActionHandlerDaemon(args)
        return daemon.control(args)
