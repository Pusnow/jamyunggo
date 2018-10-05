from . import Jamyunggo
import importlib
import os
import pathlib


class Loader:
    def __init__(self):
        self.jamyunggo_list = []
        self.backend_list = {}

        self.jamyunggo_module = []
        self.backend_module = []
        pathlib.Path('cache').mkdir(parents=True, exist_ok=True)

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
                    module = importlib.import_module(
                        ".backends." + module_name, package="jamyunggo")
                self.backend_module.append(module)
                self.backend_list[module_name] = module

    def load(self):
        self.load_backends()
        module_names = {
            module.__name__: module
            for module in self.jamyunggo_module
        }
        self.jamyunggo_module = []
        self.jamyunggo_list = []

        dirs = [("pages", a) for a in os.listdir("pages")]

        if os.path.isdir("privates"):
            dirs += [("privates", a) for a in os.listdir("privates")]

        for super_dir, py_file in dirs:
            if py_file.endswith(".py"):
                module_name = py_file[:-3]
                module_path = "jamyunggo.backends." + module_name
                if module_path in module_names:
                    module = importlib.reload(module_names[module_path])
                else:
                    module = importlib.import_module(super_dir + "." +
                                                     module_name)
                self.jamyunggo_module.append(module)
                headers = module.HEADERS if hasattr(module, "HEADERS") else {}
                body_url_fn = module.BODY_URL_FN if hasattr(
                    module, "BODY_URL_FN") else None
                body_fn = module.BODY_FN if hasattr(module,
                                                    "BODY_FN") else None
                param_fn = module.PARAM if hasattr(module, "PARAM_FN") else None
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
                    param_fn=param_fn)

                self.jamyunggo_list.append(jamyunggo)

    def run(self):
        for jamyunggo in self.jamyunggo_list:
            jamyunggo.run(self.backend_list)

        print(self.jamyunggo_list)
