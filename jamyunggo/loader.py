from . import Jamyunggo
import importlib
import os
import pathlib


class Loader:
    def __init__(self):
        self.jamyunggo_list = []
        self.backend_list = {}
        pathlib.Path('cache').mkdir(parents=True, exist_ok=True)

    def load_backends(self):
        for py_file in os.listdir("jamyunggo/backends"):
            if py_file.endswith(".py") and not py_file.startswith("_"):
                module_name = py_file[:-3]
                module = importlib.import_module(
                    ".backends." + module_name, package="jamyunggo")

                self.backend_list[module_name] = module

    def load(self):
        self.load_backends()
        for py_file in os.listdir("pages"):
            if py_file.endswith(".py"):
                module_name = py_file[:-3]
                module = importlib.import_module("pages." + module_name)

                headers = module.HEADERS if hasattr(module, "HEADERS") else {}
                body_url_fn = module.BODY_URL_FN if hasattr(
                    module, "BODY_URL_FN") else None
                body_fn = module.BODY_FN if hasattr(module,
                                                    "BODY_FN") else None
                jamyunggo = Jamyunggo(
                    module_name=module_name,
                    backends=module.BACKENDS,
                    url=module.URL,
                    find_all_args=module.FIND_ALL_ARGS,
                    title_fn=module.TITLE_FN,
                    headers=headers,
                    body_url_fn=body_url_fn,
                    body_fn=body_fn)

                self.jamyunggo_list.append(jamyunggo)

    def run(self):
        for jamyunggo in self.jamyunggo_list:
            jamyunggo.run(self.backend_list)

        print(self.jamyunggo_list)
