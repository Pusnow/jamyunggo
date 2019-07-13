import json
import os

config_path = os.environ['JAMYUNGGO_CONFIG']
with open(config_path, "r") as f:
    config = json.load(f)
