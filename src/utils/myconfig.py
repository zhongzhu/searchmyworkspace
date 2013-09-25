import ConfigParser
import json

class MyConfig(object):
    def __init__(self):
        self.configParser = ConfigParser.ConfigParser()
        self.configParser.read('config.ini')

    def get(self, section, key):
        return self.configParser.get(section, key)

    def getList(self, section, key):
        l = self.get(section, key)
        return json.loads(l)
