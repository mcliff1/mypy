import flickrapi

import logging
import os
import random
import requests

logger = logging.getLogger()

class Flickr:
    def __init__(self, key, secret):
        self.flickr = None
        self.auth(key, secret)

if __name__ == '__main__':
    flickr_key = os.environ['FLICKR_KEY']

