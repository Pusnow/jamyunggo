"""
Init file for Jamyunggo
"""
from jamyunggo import Loader
import config
import time

loader = Loader()

if config.INTERVAL:
    while True:
        loader.load()
        loader.run()
        time.sleep(config.INTERVAL)

else:
    loader.load()
    loader.run()
