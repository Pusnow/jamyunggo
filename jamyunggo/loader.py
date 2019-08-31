import importlib
import os
import pathlib

from config import config

from . import Jamyunggo, JamyunggoPage


class Loader:
    def __init__(self):
        self.jamyunggo_list = []
        self.backend_list = {}
        self.backend_module = []
        pathlib.Path(config["CACHE_DIR"]).mkdir(parents=True, exist_ok=True)

    def load_backends(self):

        module_names = {
            module.__name__: module
            for module in self.backend_module
        }

        self.backend_module = []
        for py_file in os.listdir("jamyunggo/backends"):
            if py_file.endswith(".py") and not py_file.startswith("_"):
                module_name = py_file[:-3]
                module_path = "jamyunggo.backends." + module_name

                if module_path in module_names:
                    module = importlib.reload(module_names[module_path])
                else:
                    module = importlib.import_module(".backends." +
                                                     module_name,
                                                     package="jamyunggo")
                self.backend_module.append(module)
                self.backend_list[module_name] = module

    def load(self):
        self.load_backends()
        self.jamyunggo_list = []

        dirs = []
        for repo in config["REPOS"]:
            if os.path.isdir(repo):
                dirs = [(repo, a) for a in os.listdir(repo)]

        for super_dir, py_file in dirs:
            if py_file.endswith(".py"):
                module_name = py_file[:-3]
                # module_path = "jamyunggo.backends." + module_name

                module = importlib.import_module(super_dir + "." + module_name)
                module_type = module.TYPE if hasattr(module,
                                                     "TYPE") else "list"
                headers = module.HEADERS if hasattr(module, "HEADERS") else {}

                if module_type == "list":
                    body_url_fn = module.BODY_URL_FN if hasattr(
                        module, "BODY_URL_FN") else None
                    body_fn = module.BODY_FN if hasattr(module,
                                                        "BODY_FN") else None
                    param_fn = module.PARAM_FN if hasattr(module,
                                                          "PARAM_FN") else None
                    blacklist = module.BLACKLIST if hasattr(
                        module, "BLACKLIST") else []
                    jamyunggo = Jamyunggo(
                        module_name=module_name,
                        backends=module.BACKENDS,
                        url=module.URL,
                        find_all_args=module.FIND_ALL_ARGS,
                        title_fn=module.TITLE_FN,
                        headers=headers,
                        body_url_fn=body_url_fn,
                        body_fn=body_fn,
                        name=module.NAME,
                        param_fn=param_fn,
                        blacklist=blacklist,
                    )
                elif module_type == "page":
                    jamyunggo = JamyunggoPage(
                        module_name=module_name,
                        backends=module.BACKENDS,
                        ids=module.IDS,
                        url_fn=module.URL_FN,
                        title_value_fn=module.TITLE_VALUE_FN,
                        notify_fn=module.NOTIFY_FN,
                        headers=headers,
                        name=module.NAME,
                    )

                self.jamyunggo_list.append(jamyunggo)

    def run(self):
        for jamyunggo in self.jamyunggo_list:
            jamyunggo.run(self.backend_list)

        print(self.jamyunggo_list)
