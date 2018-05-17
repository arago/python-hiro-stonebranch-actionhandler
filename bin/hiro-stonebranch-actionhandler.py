#!/usr/bin/env python3
import sys

from arago.hiro.actionhandler.plugin.stonebranch.StonebranchActionHandlerDaemon import StonebranchActionHandlerDaemon

if __name__ == "__main__":
    status = StonebranchActionHandlerDaemon.main()
    sys.exit(status)
