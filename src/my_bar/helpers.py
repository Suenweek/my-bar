import os
import json
import importlib


def get_config():
    return importlib.import_module("my_bar.config")


class Resources(object):

    def __init__(self, path):
        self.path = path
        self.items = {}

    def __getitem__(self, item):
        if item not in self.items:
            self.items[item] = self.load(item)
        return self.items[item]

    def load(self, item):
        path = os.path.join(self.path, "{}.json".format(item))
        with open(path) as f:
            return json.load(f)
