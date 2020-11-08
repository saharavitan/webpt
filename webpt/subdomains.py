import re
import requests
from webpt import find
from urllib.parse import urlparse
import threading
import urllib.request
import time
requests.packages.urllib3.disable_warnings() # noqa


class SubDomains:
    def __init__(self, url):
        self.url = url
        self.domains = []
        self.all_links = []
        self.subdomains = []
        self.sub_len = None

    def extract_href(self, src):
        tags = find(src).tag("a")

        for link in tags:
            link = link.attr("href")
            self.all_links.append(str(link))

    def baidu(self, src): # noqa
        ret = []
        links = re.findall(
            '<a target="_blank" href="https?://www(.*)" class="c-showurl" style="text-decoration:none;">', src)
        for link in links:
            url = f"http://www{link}"
            ret.append(url)

        return ret

    def make_links(self, src, name):
        if "http://www.baidu.com" in src:
            ret = self.baidu(src)
            self.all_links += ret

        tags = find(src).tag("a")
        for link in tags:
            link = link.attr("href")
            if f"{name}" not in str(link):
                self.all_links.append(str(link))

    def check(self, url, page_no, name):

        payload = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "close",
            "Cookie": "BAIDUID=BE59E2290E0A4804AA8AE1E43C266B76:FG=1",
            "Upgrade-Insecure-Requests": "1"
        }

        try:
            for i in range(1, 30, 10):
                url_new = f'{url}{page_no}{i}'
                self.make_links(requests.get(url_new, headers=payload, verify=False).text, name)
        except Exception as err: # noqa
            pass

    def pool(self, link, domain):
        if not link.startswith("http"):
            link = "http://"+link
        try:
            res = requests.get(link, verify=False)
            src = res.text
            found = list(set(re.findall(r'https?://[\w.-]+.{}'.format(domain), src)))
            for _ in found:
                if not str(_).startswith("u00") or not str(_).startswith("22") or "@" not in str(_):
                    if "." in str(_) and f".{domain}" in str(_):
                        self.subdomains.append(f"{_}")
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.InvalidURL:
            pass

    def sender(self, domain):
        num = 1
        num_after_close = 1

        for link in self.all_links:
            num += 1
            t1 = threading.Thread(target=self.pool, args=[link, domain])
            t1.start()
            if num >= 600:
                for stop_thread in range(1, 1000 + 1):
                    num_after_close += 1
                    t1.join()
                time.sleep(1)
                num = 0

    def make_links_from_google(self, src):
        tags = find(src).tag("a")
        for link in tags:
            link = link.attr("href")
            if str(link).startswith("/url?q="):
                if "&ved" in link:
                    link = str(link)
                    link = link.split("&sa")
                    link = link[0]
                    link = urllib.parse.unquote(link)
                    self.all_links.append(str(link).replace("/url?q=", ""))
                else:
                    link = urllib.parse.unquote(link)
                    self.all_links.append(str(link).replace("/url?q=", ""))

    def check_google(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G920A) AppleWebKit (KHTML, like Gecko) Chrome Mobil"
                          "e Safari (compatible; AdsBot-Google-Mobile; +http://www.google.com/mobile/adsbot.html)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "close",
            "Cookie": "BAIDUID=BE59E2290E0A4804AA8AE1E43C266B76:FG=1",
            "Upgrade-Insecure-Requests": "1"
        }
        try:
            for i in range(1, 22, 10):
                url_new = f"{url}&start={i}"
                res = requests.get(url_new, headers=headers, verify=False)
                src = res.text
                if len(src) < 4000:
                    break
                if len(src) > 26000:
                    self.make_links_from_google(src)
                else:
                    break
        except Exception as err: # noqa
            pass

    def engine(self):
        self.subdomains.append(self.url)
        index_dict = {"yahoo": '&b=', 'bing': "&go=Submit&first=", "baidu": "&pn=", "ask": "&page="}

        urls_link = [f'https://{self.url}',
                     f'https://www.google.com/search?q=inurl:+"{self.url}"',
                     f'https://www.bing.com/search?q=".{self.url}"',
                     f'https://www.bing.com/search?q={self.url}',
                     f'https://www.ask.com/web?q={self.url}'
                     f'https://www.bing.com/search?q=pastebin.com+"{self.url}"',
                     f'https://www.bing.com/search?q=facebook.com+"{self.url}"',
                     f'https://www.bing.com/search?q=twitter.com+"{self.url}"',
                     f'https://search.yahoo.com/search?p={self.url}',
                     f'https://search.yahoo.com/search?p=".{self.url}"',
                     f'https://search.yahoo.com/search?p=pastebin.com+".{self.url}"',
                     f'https://search.yahoo.com/search?p=facebook.com+"{self.url}"',
                     f'https://www.baidu.com/s?wd="{self.url}"&oq="{self.url}"']

        links = requests.get(f"https://api.web-pt.com/sub.php?url={self.url}").text.replace('"', "")\
            .replace("[", "").replace("]", "").split(",")
        self.subdomains += links

        url_list = [f"https://crt.sh/?q=%25.{self.url}",
                    f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={self.url}"]
        for url_from_list in url_list:
            src = requests.get(url_from_list).text
            found = list(set(re.findall(r'[\w-]+.{}'.format(self.url), src)))
            links = []
            for link in found:
                if self.url in link:
                    links.append(link.replace("BR>", "").replace("TD>", "").replace("q=", "")
                                 .replace("null", "www."+self.url))
            self.subdomains += links

        # dnsdumpster
        obj = requests.get("https://dnsdumpster.com/")
        token_src = obj.text
        token_header = obj.headers['Set-Cookie']
        csrf = re.findall("csrftoken=(.*); expires", token_header)[0]
        token = re.findall('name="csrfmiddlewaretoken" value="(.*)"', token_src)[0]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML"
                          ", like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "Referer": "https://dnsdumpster.com/"}
        src = requests.post("https://dnsdumpster.com/", headers=headers,
                            data={"csrfmiddlewaretoken": token, "targetip": self.url}, cookies={"csrftoken": csrf}).text
        found = list(set(re.findall(r'[\w-]+.{}'.format(self.url), src)))
        links = []
        for link in found:
            if self.url in link:
                links.append(link.replace("BR>", "").replace("q=", "").replace("map/", "")
                             .replace("xls/", "").replace("graph/", ""))
        self.subdomains += links

        for target in urls_link:
            if target == urls_link[0]:
                try:
                    self.extract_href(requests.get(target, verify=False).text)
                except requests.exceptions.MissingSchema:
                    raise requests.exceptions.MissingSchema("Invalid Url")
                except requests.exceptions.ConnectionError:
                    raise requests.exceptions.ConnectionError("Invalid Url")
                except requests.exceptions.InvalidURL:
                    raise requests.exceptions.InvalidURL("Invalid Url")
            else:
                if "google.com" in target:
                    self.check_google(target)
                else:
                    try:
                        index_name = target.split('//')[1].replace("www.", "").replace("search.", "").split('.')[0]
                        self.check(target, index_dict[index_name], index_name)
                    except requests.exceptions.MissingSchema:
                        pass

        self.all_links = list(set(self.all_links))
        self.sender(self.url)
        self.subdomains = list(set(self.subdomains))
        self.sub_len = len(self.subdomains)

        for sub in self.subdomains:
            if "https://"+sub in self.subdomains or "http://"+sub in self.subdomains:
                self.subdomains.remove(sub)
            elif sub.startswith("http://") and sub.replace("http://", "https://") in self.subdomains:
                self.subdomains.remove(sub)

        return sorted(self.subdomains)


def subdomains(url):
    return SubDomains(url).engine()
