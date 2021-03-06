import logging
import logging.config
import os
import signal
import sys
from configparser import ConfigParser, NoSectionError, NoOptionError

import gevent
from arago.common.daemon import daemon as Daemon
from arago.pyactionhandler.handler import SyncHandler
from arago.pyactionhandler.worker_collection import WorkerCollection
from docopt import docopt

from arago.hiro.actionhandler.plugin.docopt_builder import DocoptBuilder


class ActionHandlerDaemon(Daemon):

    def __init__(self, args=None):
        super().__init__(args['--pidfile'], debug=args['--debug'])
        self.args = args  # type: docopt
        self.logging_config = None
        self.handler_config = None
        self.credentials = {}
        self.handlers = []
        self.logger = logging.getLogger(__name__)

    def load_handler_config(self):
        self.handler_config = ConfigParser()
        if '--handler-config-file' in self.args:
            handler_config_filename = self.args['--handler-config-file']
        else:
            handler_config_filename = '/opt/autopilot/conf/external_actionhandlers/%s-actionhandler.conf' % self.short_name
        if os.path.isfile(handler_config_filename):
            self.handler_config.read(handler_config_filename)
        else:
            self.logger.warning("Missing or unreadable handler configuration file: %s" % handler_config_filename)

    def load_logging_config(self):
        if '--logging-config-file' in self.args:
            logging_config_filename = self.args['--logging-config-file']
        else:
            logging_config_filename = '/opt/autopilot/conf/external_actionhandlers/%s-actionhandler-log.conf' % self.short_name
        if os.path.isfile(logging_config_filename):
            logging.config.fileConfig(logging_config_filename, disable_existing_loggers=False)
        else:
            print("Missing or unreadable logging configuration file: %s" % logging_config_filename, file=sys.stderr)

    def load_credentials(self):
        pass

    def init_logging(self):
        if self.debug:
            root_logger = logging.getLogger('root')
            root_logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
            ch.setFormatter(formatter)
            root_logger.addHandler(ch)
            self.logger.info("Logging also to console")

    def pre_daemonize(self):
        self.load_logging_config()
        self.init_logging()

    def pre_drop_privileges(self):
        self.load_credentials()
        self.load_handler_config()

    def run(self):
        self.handlers = self.init_handlers()

        gevent.hub.signal(signal.SIGINT, self.exit_gracefully)
        gevent.hub.signal(signal.SIGTERM, self.exit_gracefully)
        self.logger.info("Starting handlers")
        greenlets = [
            handler.run() for handler in self.handlers
        ]
        self.logger.info("Starting handlers finished")
        gevent.idle()
        gevent.joinall(greenlets)
        self.logger.info("Exiting")
        sys.exit(0)

    def exit_gracefully(self):
        self.logger.info("Stopping handlers")
        for handler in self.handlers:
            handler.shutdown()
        self.logger.info("Stopping handlers finished")

    @property
    def zmq_auth(self) -> tuple:
        try:
            if self.handler_config.getboolean('Encryption', 'enabled'):
                return (
                    self.handler_config.get('Encryption', 'server-public-key', raw=True).encode('ascii'),
                    self.handler_config.get('Encryption', 'server-private-key', raw=True).encode('ascii')
                )
        except (NoSectionError, NoOptionError):
            pass

    @property
    def short_name(self) -> str:
        raise NotImplementedError

    @property
    def display_name(self) -> str:
        raise NotImplementedError

    @property
    def capabilities(self) -> dict:
        raise NotImplementedError

    def init_handlers(self) -> list:
        return [SyncHandler(
            WorkerCollection(
                self.capabilities,
                parallel_tasks=self.handler_config.getint('ActionHandler', 'ParallelTasks', fallback=5),
                parallel_tasks_per_worker=self.handler_config.getint('ActionHandler', 'ParallelTasksPerWorker',
                                                                     fallback=5),
                worker_max_idle=self.handler_config.getint('ActionHandler', 'WorkerMaxIdle', fallback=300)
            ),
            zmq_url=self.handler_config.get('ActionHandler', 'ZMQ_URL'),
            auth=self.zmq_auth
        )]

    def control(self, args) -> int:
        if args['start']:
            return self.start()
        elif args['stop']:
            return self.stop()
        elif args['restart']:
            return self.restart()

    @staticmethod
    def docopt_builder(builder=DocoptBuilder()) -> DocoptBuilder:
        builder.usages.append('{program_name} [options] (start|stop|restart)')
        builder.options.append('--debug\tdo not run as daemon and log to stderr')
        builder.options.append('--pidfile=PIDFILE\tSpecify pid file [default: /var/run/{short_name}.pid]')
        builder.options.append('--handler-config-file=FILE\tfoo [default: '
                               '/opt/autopilot/conf/external_actionhandlers/{short_name}-actionhandler.conf]')
        builder.options.append('--logging-config-file=FILE\tbar [default: '
                               '/opt/autopilot/conf/external_actionhandlers/{short_name}-actionhandler-log.conf]')
        builder.options.append('-h --help\tShow this help screen')
        return builder
