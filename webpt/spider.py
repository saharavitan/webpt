import requests
from urllib.parse import urlparse
import threading
import time
from webpt.response_analysis import find
from webpt.any import isalive

requests.packages.urllib3.disable_warnings() # noqa


class Dict(dict):
    def __getattr__(self, item):
        pass


class Spider:
    def __init__(self, url=None):
        self.url = url
        self.level_deeps_ch = 1
        self.base_url = None
        self.links = []
        self.pass_links_dir = []
        self.links_dir = []
        self.msg_folder = ""
        self.headers = {"User-Agent": "Mozila/5",
                        "Accept": "application/json, text/javascript, */*; q=0.01"}
        self.non_list = ("#", "javascript:", "javascript :", "tel:", "mailto:", "'", "%",  "$", '\\', "data:image"
                         , "{{", "[""[[", "{", '"')
        self.cookies = {}
        self.src = None
        self.js_list = []

    def search(self, tag, att, src):
        tags = find(src).tag(tag, inline=True)

        for link in tags:
            link = link.attr(att)

            if ";" in str(link):
                link = link.split(";")[0]
            if ">" in str(link):
                link = link.split(">")[0]
            if " " in str(link):
                link = link.split(" ")[0]

            parsed = urlparse(link)
            base_from_link = parsed.netloc
            parsed = urlparse(self.url)
            base_from_url = parsed.netloc

            if link is not None:
                link = link.replace("www.", "")
                if link.startswith(" "):
                    link = link.replace(" ", '')
                if link.startswith("/www"):
                    link = self.url.split("/")[0] + link
                if link.startswith("http"):
                    if base_from_url == base_from_link or f"www.{base_from_url}" == base_from_link:
                        self.links.append(f"{link}")

                else:
                    if not link.startswith(self.non_list):
                        if link.startswith("/") and not link.startswith("//"):
                            link = f"{self.url}{link}"
                        elif not link.startswith("/"):
                            link = f"{self.url}/{link}"
                        elif not link.startswith("//"):
                            link = link.replace("//", "")
                            link = f"{self.url}/{link}"
                        if link.startswith("http"):
                            self.links.append(f"{link}")

    def make_links(self, _=None, src=None):
        if src is None:
            try:
                res = requests.get(_, headers=self.headers, cookies=self.cookies, verify=False)
                src = res.text
            except: # noqa
                src = ""

        dic = {"a": "href", "img": "src", "link": "href", "script": "src"}
        for tag, att in dic.items():
            self.search(tag, att, src)

    def check_protocol(self):
        if not self.url.startswith("http"):
            url_https = f"https://{self.url}:443"
            status_code = requests.get(url_https, verify=False).status_code
            self.url = "https"+self.url
            if status_code == 403:
                url_http = f"http://{self.url}:80"
                requests.get(url_http, verify=False)
                self.url = "http"+self.url

    def folders(self,):
        big_len = 0
        test = []

        for link in self.links:
            num_link_ls = 0
            link = str(link)
            link_tmp_re = str(self.url).replace('www.', '')
            if link.startswith("http://"):
                link = link.replace("http", "https")
            if "www." in link:
                link = link.replace(f"{self.url}", "")
            else:
                link = link.replace(link_tmp_re, "")

            link_ls = link.split("/")
            try:
                del link_ls[0]
            except: # noqa
                pass

            parsed = urlparse(self.url)
            base_url = parsed.netloc
            try:
                if link_ls[0] == '':
                    del link_ls[0]
                if link_ls[0] == base_url:
                    del link_ls[0]
            except: # noqa
                pass

            for file in link_ls:
                if "?" in file:
                    file = file.split("?")[0]
                if "#" in file:
                    file = file.split("#")[0]

                # Get Before
                if num_link_ls == 0:
                    before = ''  # First folder
                else:
                    before = link_ls[num_link_ls - 1]  # Take the last folder

                tmp = f"{before};{num_link_ls};{file}"
                if file != '' and tmp not in test:
                    test.append(f"{tmp}")

                num_link_ls += 1
            big_len += 1

        folder = test
        if folder:
            for ta in folder:
                ta_split = ta.split(";")
                try:
                    num = int(ta_split[1])
                except ValueError:
                    num = 0
                file = ta_split[2]
                self.msg_folder += f"{'  ' * num}> {file}\n"

    def __call__(self, *args, **kwargs):
        # Base URL
        base = str(self.url).split("/")
        self.base_url = base[2]
        if self.url.endswith("/"):
            self.url = self.url[:-1]

        # Get Source Code
        res = requests.get(self.url, headers=self.headers, cookies=self.cookies, verify=False)
        src = res.text

        # Make a links
        self.make_links(src=src)

        self.links = list(set(self.links))
        link_pass = []
        # Level Deep
        level_deeps = 0
        for i in range(self.level_deeps_ch):
            num = 1
            num_after_close = 1

            for _ in self.links:
                if _ in link_pass:
                    continue
                link_pass.append(_)
                num += 1
                t1 = threading.Thread(target=self.make_links, args=[_])
                t1.start()
                if num >= len(self.links) or num >= 800:
                    for stop_thread in range(1, len(self.links) + 1):
                        num_after_close += 1
                        t1.join()
                    time.sleep(1)
                    num = 0
                link_pass = list(set(link_pass))
                self.links = list(set(self.links))

            level_deeps += 1
        self.links = list(set(self.links))
        self.links.sort()
        self.folders()

        for l in self.links: # noqa
            if ".js" in l:
                self.js_list.append(l)
        request_dict = {"links": self.links, "gui": self.msg_folder, "js": self.js_list}
        get_var = Dict(request_dict)
        for key, value in get_var.items():
            setattr(get_var, key.lower(), value)
        return get_var


def spider(url):
    res = isalive(url)
    if res == "isAlive":
        return Spider(url)()
