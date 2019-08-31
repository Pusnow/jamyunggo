"""
Jamyunggo Page
"""
import os
import pickle
import urllib.parse

import requests
from bs4 import BeautifulSoup

from config import config


class JamyunggoPage:
    """
    Main Jamyunggo class
    One jamyunggo for one URL
    """
    def __init__(self,
                 module_name,
                 backends,
                 ids,
                 url_fn,
                 title_value_fn,
                 notify_fn,
                 headers={},
                 name=None):
        self.module_name = module_name
        self.backends = backends
        self.ids = ids
        self.url_fn = url_fn
        self.title_value_fn = title_value_fn
        self.notify_fn = notify_fn
        self.headers = headers
        self.name = name

        self.nodes = None
        self.cached_last = {}
        self.body_urls = []

        self.session = requests.session()

        self.load_cache()

    def __repr__(self):
        return "<JamyunggoPage %s >" % self.module_name

    def run(self, backend_list):

        for id in self.ids:
            url = self.url_fn(id)

            if self.headers:
                main_html = self.session.get(url, headers=self.headers)
            else:
                main_html = self.session.get(url)

            main_text = main_html.text
            title, value = self.title_value_fn(main_text)
            if id not in self.cached_last:
                self.cached_last[id] = None
            if self.notify_fn(value, self.cached_last[id]):
                self.notify(title, value, url, backend_list)
            self.cached_last[id] = value

        self.save_cache()

    def save_cache(self):
        with open(
                os.path.join(config["CACHE_DIR"], self.module_name + ".cache"),
                "wb",
        ) as cache:
            pickle.dump(self.cached_last, cache)

    def load_cache(self):
        try:
            with open(
                    os.path.join(config["CACHE_DIR"],
                                 self.module_name + ".cache"), "rb") as cache:
                self.cached_last = pickle.load(cache)
        except FileNotFoundError:
            self.cached_last = {}

    def notify(self, title, value, url, backend_list):

        for backend in self.backends:
            if backend in backend_list:
                module = backend_list[backend]

                return module.notify(self.module_name,
                                     title,
                                     url=url,
                                     text="",
                                     name=self.name)

    def img_src_replace(self, body_url, body):
        for img in body.find_all("img"):
            img["src"] = urllib.parse.urljoin(body_url, img["src"])
        return body

    def get_text(self, body_url):
        if self.body_fn:
            if self.headers:
                body_html = self.session.get(body_url, headers=self.headers)
            else:
                body_html = self.session.get(body_url)
            body_text = body_html.text
            body_soup = BeautifulSoup(body_text, 'html.parser')
            return str(self.img_src_replace(body_url, self.body_fn(body_soup)))

        else:
            return None
