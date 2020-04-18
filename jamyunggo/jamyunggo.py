"""
Main Jamyunggo
"""
import os
import pickle
import urllib.parse
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from config import config


class Jamyunggo:
    """
    Main Jamyunggo class
    One jamyunggo for one URL
    """
    def __init__(self, module_name, module, backend_list):
        self.module_name = module_name
        self.module = module
        self.backend_list = backend_list
        self.session = requests.session()
        self.load_cache()

    def __repr__(self):
        return "<Jamyunggo %s >" % self.module_name

    def run(self):
        headers = self.module.HEADERS if hasattr(self.module,
                                                 "HEADERS") else {}
        self.module.LOAD(self.cached_last)

        force = self.module.FORCE if hasattr(self.module, "FORCE") else False
        verify = not force
        for url in self.module.URLS:
            if headers:
                main_html = self.session.get(url,
                                             headers=headers,
                                             verify=verify)
            else:
                main_html = self.session.get(url, verify=verify)

            main_text = main_html.text
            main_soup = BeautifulSoup(main_text, 'html.parser')

            scope = self.module.SCOPE if hasattr(self.module, "SCOPE") else {}

            nodes = []
            for scope_node in main_soup.find_all(**scope):
                for node in self.module.LIST(scope_node):
                    nodes.append(node)

            for node in nodes:
                title = self.module.NODE_TITLE(node)
                name = self.module.NAME
                node_url = self.module.NODE_URL(node, url)
                if node_url:
                    node_url = urllib.parse.urljoin(url, node_url)
                backends = self.module.BACKENDS
                need_notify = self.module.NODE_NOTIFY(node, url)

                if need_notify:
                    self.notify(name, title, node_url, backends)

        self.cached_last = self.module.STORE()
        self.save_cache()

    def save_cache(self):
        with open(
                os.path.join(config["CACHE_DIR"],
                             self.module_name + ".pickle"), "wb") as cache:
            pickle.dump(self.cached_last, cache)

    def load_cache(self):
        try:
            with open(
                    os.path.join(config["CACHE_DIR"],
                                 self.module_name + ".pickle"), "rb") as cache:
                self.cached_last = pickle.load(cache)
        except FileNotFoundError:
            self.cached_last = None

    def notify(self, name, title, url, backends):

        for backend in backends:
            if backend in self.backend_list:
                module = self.backend_list[backend]
                print("[%s] Nofify[%s]:  [%s] %s" %
                      (datetime.now(), self.module_name, name, title))

                return module.notify(self.module_name,
                                     title,
                                     url=url,
                                     name=name)

    def img_src_replace(self, body_url, body):
        for img in body.find_all("img"):
            img["src"] = urllib.parse.urljoin(body_url, img["src"])
        return body
