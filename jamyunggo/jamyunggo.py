"""
Main Jamyunggo
"""
import requests
from bs4 import BeautifulSoup
import urllib.parse
import config


class Jamyunggo:
    """
    Main Jamyunggo class
    One jamyunggo for one URL
    """

    def __init__(self,
                 module_name,
                 backends,
                 url,
                 find_all_args,
                 title_fn,
                 body_url_fn,
                 headers={},
                 body_fn=None,
                 name=None,
                 param=None):
        self.module_name = module_name
        self.backends = backends
        self.url = url
        self.find_all_args = find_all_args
        self.title_fn = title_fn
        self.body_url_fn = body_url_fn
        self.body_fn = body_fn
        self.headers = headers
        self.name = name
        self.param = param

        self.nodes = None
        self.cached_last = ""
        self.body_urls = []

        self.session = requests.session()

        self.load_cache()

    def __repr__(self):
        return "<Jamyunggo %s >" % self.url

    def run(self, backend_list):

        if self.headers:
            main_html = self.session.get(self.url, headers=self.headers)
        else:
            main_html = self.session.get(self.url)
        main_text = main_html.text
        main_soup = BeautifulSoup(main_text, 'html.parser')

        self.nodes = []
        for node in main_soup.find_all(**self.find_all_args):
            self.nodes.append(node)

        self.body_urls = []
        for node in self.nodes:
            self.body_urls.append(self.body_url_fn(node))

        if not self.body_urls:
            return


        if self.param:
            try:
                cached_last_int = int(self.cached_last)
            except:
                cached_last_int = 0
            for url, node in zip(self.body_urls, self.nodes):
                query = urllib.parse.urlsplit(url).query
                params = urllib.parse.parse_qsl(query)

                if self.param not in params:
                    raise
            
                id = int(params[self.param])

                if cached_last_int >= id:
                    break
                self.notify(node, backend_list)
                cached_last_int = id
            self.cached_last = str(cached_last_int)
        else:
            cached_last = self.cached_last
            for url, node in zip(self.body_urls, self.nodes):
                if url == self.cached_last:
                    break
                self.notify(node, backend_list)
                cached_last = url
            self.cached_last = cached_last

        self.save_cache()

    def save_cache(self):
        with open(
                "cache/" + self.module_name + ".cache", "w",
                encoding="utf8") as cache:
            cache.write(self.cached_last)

    def load_cache(self):
        try:
            with open(
                    "cache/" + self.module_name + ".cache",
                    "r",
                    encoding="utf8") as cache:
                self.cached_last = cache.read()
        except FileNotFoundError:
            self.cached_last = ""

    def notify(self, node, backend_list):
        for backend in self.backends:
            if backend in backend_list:
                module = backend_list[backend]
                title = self.title_fn(node)
                body_url = self.body_url_fn(node)

                if body_url:
                    url = urllib.parse.urljoin(self.url, body_url)
                    text = self.get_text(url)
                else:
                    url = None
                    text = ""
                return module.notify(
                    self.module_name, title, url=url, text=text, name=name)

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
