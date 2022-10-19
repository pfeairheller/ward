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
    admin = 5621

    def __init__(self, name, *args, **kwargs):
        super(Ward, self).__init__("Ward")
        self.status = rumps.MenuItem(f'Listening on... {self.admin}')
        self.menu.add(self.status)

        self.start()

    def start(self):
        config_path = os.path.join(pathlib.Path(__file__).parent.resolve(), 'config.json')
        if os.path.exists(config_path):
            with open(config_path) as f:
                data = json.load(f)

                # logger.debug(f'Loaded config {data} from {self._path}')

                if data is not None:
                    self.admin = int(data['API_PORT'])
                    self.status.title = f'Listening on... {self.admin}'

        kp = os.path.join(pathlib.Path.home(), ".keri", "cf")
        if not os.path.exists(kp):
            os.makedirs(kp)

        with open(os.path.join(pathlib.Path.home(), ".keri", "cf", "witnesses.json"), "w") as f:
            json.dump({
                "dt": "2022-01-20T12:57:59.823350+00:00",
                "iurls": [
                    "http://49.12.190.139:5623/oobi",
                    "http://139.99.193.43:5623/oobi",
                    "http://20.3.144.86:5623/oobi",
                    "http://13.245.160.59:5623/oobi",
                    "http://47.242.47.124:5623/oobi"
                ]
            }, f, indent=2)

        print(f'Listening on... {self.admin}')
        servery = booting.Servery(port=self.admin)
        booting.setup(servery=servery,
                      controller="E59KmDbpjK0tRf9Rmc7OlueZVz7LB94DdD3cjQVvPcng",
                      configFile='witnesses.json',
                      insecure=True)

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
