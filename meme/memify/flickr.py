"""
Flicker Class
"""

import logging
import os
import random
import requests

import flickrapi


LOGGER = logging.getLogger()

class Flickr:
    """
    class to wrap flicker Interface
    """
    def __init__(self, key, secret):
        LOGGER.debug('__init()__:begin')
        self.flickr = None
        self.auth(key, secret)


    def auth(self, secret):
        """
        better do something
        """
        pass

if __name__ == '__main__':
    flickr_key = os.environ['FLICKR_KEY']
