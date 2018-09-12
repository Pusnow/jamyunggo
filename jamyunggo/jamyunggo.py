"""
Main Jamyunggo
"""
import requests
from bs4 import BeautifulSoup
import msgpack
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
                 body_fn=None):
        self.module_name = module_name
        self.backends = backends
        self.url = url
        self.find_all_args = find_all_args
        self.title_fn = title_fn
        self.body_url_fn = body_url_fn
        self.body_fn = body_fn
        self.headers = headers

        self.nodes = None
        self.cached_urls = []
        self.urls = []

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

        self.urls = []
        for node in self.nodes:
            self.urls.append(self.body_url_fn(node))

        if self.cached_urls:
            first = self.cached_urls[0]
        else:
            first = None

        for title, node in zip(self.urls, self.nodes):
            if title == first:
                break
            self.notify(node, backend_list)

        self.save_cache()

    def save_cache(self):
        with open("cache/" + self.module_name + ".cache", "wb") as cache:
            cache.write(msgpack.packb(self.urls, use_bin_type=True))

    def load_cache(self):

        if config.REMOTE_CACHE:
            try:
                cached_result = requests.get(config.HOME_URL + "/" +
                                             self.module_name + ".cache")
                if cached_result.status_code == 200:
                    content = cached_result.content
                    self.cached_urls = msgpack.unpackb(content, raw=False)
                else:
                    print("Cache Error non 200 code")
            except SystemExit:
                raise SystemExit
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                print("Cache Load Error!")

            with open("cache/" + self.module_name + ".cache", "wb") as cache:
                cache.write(msgpack.packb(self.cached_urls, use_bin_type=True))
        else:
            try:
                with open("cache/" + self.module_name + ".cache",
                          "rb") as cache:
                    self.cached_urls = msgpack.unpackb(cache.read(), raw=False)
            except FileNotFoundError:
                self.cached_urls = []

    def notify(self, node, backend_list):
        for backend in self.backends:
            if backend in backend_list:
                module = backend_list[backend]
                title = self.title_fn(node)

                url = urllib.parse.urljoin(self.url, self.body_url_fn(node))
                text = self.get_text(url)
                return module.notify(
                    self.module_name, title, url=url, text=text)

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