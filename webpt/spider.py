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
    def __init__(self, url=None, headers=None, level_deeps=2):
        self.url = str(url)
        self.protocol = None
        self.base_url = None
        self.links = [url]
        self.level_deeps = level_deeps
        self.pass_links_dir = []
        self.links_dir = []
        self.msg_folder = ""
        self.headers = {"Connection": "close",
                        "Cache-Control": "max-age=0",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7"}
        if isinstance(headers, dict):
            self.headers.update(headers)
        self.non_list = ("#", "javascript:", "javascript :", "tel:", "mailto:", "'", "%", "$", '\\', "data:image"
                         , "{{", "[""[[", "{", '"')
        self.src = None
        self.js_list = []

    def check_and_add(self, link):
        if "logout" in link or "log-out" in link or "log_out" in link:
            return
        parsed = urlparse(self.url)
        base_from_url = parsed.netloc
        parsed = urlparse(link)
        base_from_link = parsed.netloc
        if base_from_url == base_from_link or f"www.{base_from_url}" == base_from_link or base_from_url.replace(
                "www.",
                "") == base_from_link:
            try:
                link = requests.get(link, headers=self.headers, allow_redirects=True, verify=False).url
                self.links.append(link)
            except requests.exceptions.SSLError:
                pass

    def search(self, tag, att, src, links_from):
        tags = find(src).tag(tag, inline=True)

        for link in tags:
            link = link.attr(att)
            if ";" in str(link):
                link = link.split(";")[0]
            if ">" in str(link):
                link = link.split(">")[0]
            if " " in str(link):
                link = link.split(" ")[0]

            parsed = urlparse(self.url)
            base_from_url = parsed.netloc
            parsed = urlparse(link)
            base_from_link = parsed.netloc

            if link is not None:
                if not link.startswith(self.non_list):
                    if link.startswith("http"):
                        self.check_and_add(link)
                        continue
                    else:
                        if link.startswith("/www.") or link.startswith(f"/{base_from_url}"):
                            link = self.protocol + ":/" + link
                            self.check_and_add(link)
                            continue
                        elif link.startswith("//www") or link.startswith(f"//{base_from_url}"):
                            link = self.protocol + ":" + link
                            self.check_and_add(link)
                            continue
                        elif link.startswith("./") or  link.startswith("../") or link.startswith("/../"):
                            if not links_from.endswith("/") and link.startswith("/"):
                                link = links_from + link
                                self.check_and_add(link)
                            elif links_from.endswith("/") and not link.startswith("/"):
                                link = links_from + link
                                self.check_and_add(link)
                            elif link.startswith("/") and links_from.endswith("/"):
                                link = links_from[:-1] + link
                                self.check_and_add(link)
                            continue
                        elif link.startswith("/"):
                            link = self.protocol + "://" + self.base_url + link
                            self.check_and_add(link)
                            continue
                        else:
                            tmp = links_from.split("/")
                            if not links_from.endswith("/"):
                                links_from = "/".join(tmp[0:-1]) + "/"

                            link = links_from + link
                            self.check_and_add(link)
                            continue

    def make_links(self, links_from=None, src=None):
        if src is None:
            try:
                res = requests.get(links_from, headers=self.headers, allow_redirects=True, verify=False)
                src = res.text
            except: # noqa
                src = ""

        dic = {"a": "href", "img": "src", "link": "href", "script": "src"}
        for tag, att in dic.items():
            self.search(tag, att, src, links_from)

    def check_protocol(self):
        if not self.url.startswith("http"):
            url = self.url
            try:
                res = requests.get("http://" + url, headers=self.headers, allow_redirects=True, verify=False).url
            except requests.exceptions.ConnectionError:
                res = requests.get("https://" + url, headers=self.headers, allow_redirects=True, verify=False).url
            except requests.exceptions.MissingSchema:
                raise requests.exceptions.MissingSchema("Protocol is missing")
            self.url = res.split("://")[0] + "://" + url
        self.protocol = self.url.split("://")[0]

    def folders(self):
        big_len = 0
        test = []

        for link in self.links:
            num_link_ls = 0
            link = str(link)
            link_tmp_re = str(f"{self.protocol}://{self.base_url}/").replace('www.', '')
            if link.startswith("http://"):
                link = link.replace("http", "https")
            if "www." in link:
                link = link.replace(f"{self.protocol}://{self.base_url}/", "")
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
        self.check_protocol()
        base = str(self.url).split("/")
        self.base_url = base[2]
        # Get Source Code
        res = requests.get(self.url, headers=self.headers, allow_redirects=True, verify=False)
        src = res.text

        # Make a links
        self.make_links(self.url, src=src)
        self.links = list(set(self.links))

        link_pass = []
        for i in range(self.level_deeps):
            time.sleep(1)
            num = 1
            num_after_close = 1
            for _ in self.links:
                if _ in link_pass:
                    continue
                link_pass.append(_)
                num += 1
                t1 = threading.Thread(target=self.make_links, args=[_])
                t1.start()
                if num >= 600 or num >= len(self.links):
                    for stop_thread in range(1, len(self.links) + 1):
                        num_after_close += 1
                        t1.join()
                    time.sleep(1)
                    num = 0
                link_pass = list(set(link_pass))
                self.links = list(set(self.links))
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


def spider(url, headers=None, level_deeps=2):
    res = isalive(url, headers)
    if res == "isAlive":
        return Spider(url, headers, level_deeps)()
