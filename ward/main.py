# -*- encoding: utf-8 -*-
import json
import logging
import os
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
        self.menu.add(self.status)

        version = open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'version')), "r")
        v = version.read()
        version.close()

        self.version = rumps.MenuItem(f'Version: {v}')
        self.menu.add(self.version)
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

        wits = {
            "dt": "2022-01-20T12:57:59.823350+00:00",
            "iurls": [
                "http://49.12.190.139:5623/oobi",   # staging
                "http://139.99.193.43:5623/oobi",   # staging
                "http://20.3.144.86:5623/oobi",     # staging
                "http://13.245.160.59:5623/oobi",   # staging
                "http://47.242.47.124:5623/oobi",   # staging
                "http://65.21.253.212:5623/oobi",   # production Pool 1 BDkq35LUU63xnFmfhljYYRY0ymkCg7goyeCxN30tsvmS
                "http://8.210.213.186:5623/oobi",   # production Pool 1 BLmvLSt1mDShWS67aJNP4gBVBhtOc3YEu8SytqVSsyfw
                "http://51.79.54.121:5623/oobi",    # production Pool 1 BHxz8CDS_mNxAhAxQe1qxdEIzS625HoYgEMgqjZH_g2X
                "http://102.37.159.99:5623/oobi",   # production Pool 1 BTXmViKBsWrnXfs7v_00vTdSIh5w_9uDdrz2K7cuRS9s
                "http://54.233.109.129:5623/oobi",  # production Pool 1 BFl6k3UznzmEVuMpBOtUUiR2RO2NZkR3mKrZkNRaZedo
                "http://5.161.69.25:5623/oobi",     # production Pool 2 BNfDO63ZpGc3xiFb0-jIOUnbr_bA-ixMva5cZb3s4BHB
                "http://51.161.130.60:5623/oobi",   # production Pool 2 BDwydI_FJJ-tvAtCl1tIu_VQqYTI3Q0JyHDhO1v2hZBt
                "http://20.78.61.227:5623/oobi",    # production Pool 2 BewGSU2XtGOf28Drz-TJJzHxG-UgYPZSx8WjVT3HbkgM
                "http://13.244.119.106:5623/oobi",  # production Pool 2 BM4Ef3zlUzIAIx-VC8mXziIbtj-ZltM8Aor6TZzmTldj
                "http://8.208.27.153:5623/oobi"     # production Pool 2 BLo6wQR73-eH5v90at_Wt8Ep_0xfz05qBjM3_B1UtKbC

            ]
        }
        with open(os.path.join(pathlib.Path.home(), ".keri", "cf", "witnesses.json"), "w") as f:

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
