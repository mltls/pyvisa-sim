import yaml
import logging


class Binary(yaml.YAMLObject):
    yaml_tag = '!Binary'

    def __init__(self, binary):
        self.binary = binary

    def __repr__(self):
        return "binary: %s" % self.binary

    def strip(self, delim):
        return self

    def to_bin(self):
        logging.debug('to_bin called')
        return bytes(self.binary.encode('ascii'))
