import importlib
import os
import pathlib
from datetime import datetime

from config import config

from . import Jamyunggo


class Loader:
    def __init__(self):
        self.jamyunggo_list = []
        self.backend_list = {}
        pathlib.Path(config["CACHE_DIR"]).mkdir(parents=True, exist_ok=True)

    def load_backends(self):

        for py_file in os.listdir("jamyunggo/backends"):
            if py_file.endswith(".py") and not py_file.startswith("_"):
                module_name = py_file[:-3]

                module = importlib.import_module(".backends." + module_name,
                                                 package="jamyunggo")
                if module.NAME in config:
                    self.backend_list[module_name] = module

    def load(self):
        self.load_backends()
        self.jamyunggo_list = []

        dirs = []
        for repo in config["PAGES"]:
            if os.path.isdir(repo):
                dirs = [(repo, a) for a in os.listdir(repo)]
        for super_dir, py_file in dirs:
            if py_file.endswith(".py"):
                if super_dir and super_dir[-1] == "/":
                    super_dir = super_dir[:-1]
                super_dir = super_dir.replace("/", ".")
                module_name = py_file[:-3]
                module = importlib.import_module(super_dir + "." + module_name)

                jamyunggo = Jamyunggo(module_name=module_name,
                                      module=module,
                                      backend_list=self.backend_list)

                self.jamyunggo_list.append(jamyunggo)

    def run(self):
        for jamyunggo in self.jamyunggo_list:
            jamyunggo.run()

        print("[%s] Done" % datetime.now())
