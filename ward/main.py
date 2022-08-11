# -*- encoding: utf-8 -*-
import json
import logging
import os
import os.path
import pathlib
import threading
from datetime import datetime
from logging.handlers import RotatingFileHandler

import rumps
from keri.app import booting
from keri.app import directing

logger = logging.getLogger('ward_log')


class Ward(rumps.App):
    HeadDirPath = ""
    tcp = 5721
    admin = 5621

    def __init__(self, name, *args, **kwargs):
        super(Ward, self).__init__("Ward")
        self.status = rumps.MenuItem(f'Listening on... {self.admin}')
        self.menu.add(self.status)

        ward_home = os.path.join(pathlib.Path.home(), ".ward")
        if not os.path.exists(ward_home):
            os.mkdir(ward_home)

        self.HeadDirPath = ward_home

        logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(os.path.join(ward_home, 'ward.log'), maxBytes=2000, backupCount=10)
        logger.addHandler(handler)

        logger.debug(f'Starting ward {datetime.now()}')

        self.start()

    def start(self):
        with open(os.path.join(pathlib.Path(__file__).parent.resolve(), 'config.json')) as f:
            data = json.load(f)

            # logger.debug(f'Loaded config {data} from {self._path}')

            if data is not None:
                self.admin = int(data['API_PORT'])
                self.tcp = int(data['TCP_PORT'])

                self.status.title = f'Listening on... {self.admin}'

        servery = booting.Servery(port=self.admin)
        booting.setup(servery=servery,
                      controller="E59KmDbpjK0tRf9Rmc7OlueZVz7LB94DdD3cjQVvPcng",
                      configFile='demo-witness-oobis',
                      configDir=self.HeadDirPath,
                      insecure=True,
                      tcp=self.tcp,
                      adminHttpPort=self.admin,
                      headDirPath=self.HeadDirPath)

        th = threading.Thread(target=self.dispatch, args=([servery]))
        th.start()

    @staticmethod
    def dispatch(servery):
        directing.runController(doers=[servery], expire=0.0)


def main():
    app = Ward("Ward")
    app.icon = "icon.png"
    app.run()


if __name__ == '__main__':
    main()
