# coding: utf-8

import os
import json
from fileutil import check_and_create

config_file = os.environ["HOME"] + "/.config/kdmongoviewer/conf.json"


def init_conf():
    check_and_create(config_file)
    with open(config_file, "r") as f:
        content = f.read()
        if content.strip() != "":
            conf = json.loads(content)
            return conf


def update_conf(host, port):
    check_and_create(config_file)
    with open(config_file, "w+") as f:
        conf = {}
        conf["host"] = host
        conf["port"] = port
        f.write(json.dumps(conf))
        f.flush()
