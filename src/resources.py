import os
import json


class Resources(object):

    def __init__(self, path="resources"):
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
