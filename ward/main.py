# -*- encoding: utf-8 -*-
import json
import logging
import os
import os.path
import pathlib
import threading
from logging import handlers

import rumps
from keri.app import booting
from keri.app import directing

logger = logging.getLogger('ward_log')
logger.setLevel(logging.DEBUG)


class Ward(rumps.App):
    admin = 5621

    def __init__(self, name, *args, **kwargs):
        super(Ward, self).__init__("Ward")
        kp = os.path.join(pathlib.Path.home(), ".keri")
        if not os.path.exists(kp):
            os.makedirs(kp)

        with open(os.path.join(kp, "ward.log"), "w+") as loggy:
            log_handler = handlers.RotatingFileHandler(loggy.name,
                                                       maxBytes=2000000,
                                                       backupCount=10)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            log_handler.setFormatter(formatter)

        log_handler.setLevel(logging.DEBUG)
        logger.addHandler(log_handler)

        m = f'Listening on... {self.admin}'
        self.status = rumps.MenuItem(f'')
        self.set_status(msg=m)
        self.start()

    def set_status(self, msg):
        logger.debug(msg)
        self.status.title = msg

    def dispatch_exception(self, args):
        self.set_status('Stopped')
        logger.error(f'{args.exc_value}')
        logger.debug("restarting")
        rumps.notification(title='Error', subtitle='Stopped', message=f'{args.exc_value}')
        self.start()

    def start(self):
        config_path = os.path.join(pathlib.Path(__file__).parent.resolve(), 'config.json')
        if os.path.exists(config_path):
            with open(config_path) as f:
                data = json.load(f)

                if data is not None:
                    self.admin = int(data['API_PORT'])
                    self.status.title = f'Listening on... {self.admin}'

        kpc = os.path.join(pathlib.Path.home(), ".keri", "cf")
        if not os.path.exists(kpc):
            os.makedirs(kpc)

        with open(os.path.join(pathlib.Path.home(), ".keri", "cf", "witnesses.json"), "w") as f:
            wits = {
                "dt": "2022-01-20T12:57:59.823350+00:00",
                "iurls": [
                    "http://49.12.190.139:5623/oobi",   # staging
                    "http://139.99.193.43:5623/oobi",   # staging
                    "http://20.3.144.86:5623/oobi",     # staging
                    "http://13.245.160.59:5623/oobi",   # staging
                    "http://47.242.47.124:5623/oobi",   # staging
                    "http://65.21.253.212:5623/oobi",   # production
                    "http://5.161.69.25:5623/oobi"      # production
                    "http://51.79.54.121:5623/oobi",    # production
                    "http://51.161.130.60:5623/oobi",   # production
                    "http://20.78.61.227:5623/oobi",    # production
                    "http://102.37.159.99:5623/oobi",   # production
                    "http://54.233.109.129:5623/oobi",  # production
                    "http://13.244.119.106:5623/oobi",  # production
                    "http://8.208.27.153:5623/oobi",    # production
                    "http://8.210.213.186:5623/oobi",   # production
                ]
            }

            logger.debug(f'writing witnesses {wits}')
            json.dump(wits, f, indent=2)

        servery = booting.Servery(port=self.admin)
        booting.setup(servery=servery,
                      controller="E59KmDbpjK0tRf9Rmc7OlueZVz7LB94DdD3cjQVvPcng",
                      configFile='witnesses.json',
                      insecure=True)

        threading.excepthook = self.dispatch_exception

        th = threading.Thread(target=self.dispatch, args=([servery]))
        th.start()
        th.join(0.1)

    @staticmethod
    def dispatch(servery):
        directing.runController(doers=[servery], expire=0.0)


def main():
    app = Ward("Ward")
    app.icon = "icon.png"
    app.run()


if __name__ == '__main__':
    main()
