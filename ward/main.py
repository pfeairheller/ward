# -*- encoding: utf-8 -*-
import json
import os
import os.path
import pathlib
import threading

import rumps
from keri import help
from keri.app import booting
from keri.app import directing

logger = help.ogler.getLogger()


class Ward(rumps.App):
    HeadDirPath = ""
    tcp = 5721
    admin = 5621

    def __init__(self, name, *args, **kwargs):
        super(Ward, self).__init__("Ward")
        self._path = pathlib.Path(__file__).parent.resolve()
        self.HeadDirPath = self._path.absolute()
        status = rumps.MenuItem(title=f'Listening on... {self.admin}')
        self.menu.add(status)
        self.start(sender=None)

    def start(self, sender):
        p = pathlib.Path(__file__).parent.resolve()
        f = open(os.path.join(p, 'config.json'))
        data = json.load(f)

        if data is not None:
            self.admin = int(data['API_PORT'])
            self.tcp = int(data['TCP_PORT'])

        logger.debug(f"HeadDirPath {self.HeadDirPath}\n")

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
