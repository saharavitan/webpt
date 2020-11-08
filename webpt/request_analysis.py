import re
import requests
from webpt.any import isalive
requests.packages.urllib3.disable_warnings() # noqa


class Dict(dict):
    def __getattr__(self, item):
        pass


class Request_Analysis:
    def __init__(self, request=None):
        self.url = ""
        self.protocol = ""
        self.base_url = ""
        self.method = ""
        self.data = None
        self.tmp = ""
        self.path = ""
        self.params = {}
        self.request = request
        self.cookies = None
        self.headers = {}
        self.accept = None
        self.content_type = None
        self.status_code = None
        self.res = None
        self.redirect = None

    def get_protocol(self):
        url = self.tmp
        try:
            res = requests.get("http://"+url).url
        except requests.exceptions.MissingSchema:
            raise requests.exceptions.MissingSchema("Protocol is missing")
        self.protocol = res.split("://")[0]

    def get_response(self):
        data_split = self.request.split("\n")
        num = 0
        stop = False
        index = 0

        # GetMethod
        self.method = data_split[0].split(" ")[0]

        # GET index for data
        for line in data_split:
            if not stop:
                if line == "":
                    index = num + 1
                    stop = True
            num += 1

        # GET Data
        _data = ""
        for i in data_split[index:len(data_split)]:

            _data += f"{i} "
        self.data = _data

        # GET Params
        path = re.findall(f"{self.method} (.*) HTTP", data_split[0])[0]
        for param in data_split[1:index - 1]:
            param = param.replace("\n", "")
            param = param.split(":")
            if "Cookie" in param:
                self.cookies = {}
            if param[0] == "Host":
                self.base_url = param[1].replace(" ", "")
                self.path = path
                self.tmp = self.base_url + path
                self.get_protocol()
                self.url = self.protocol + "://" + self.tmp
            elif param[0] == "Cookie":
                tmp_cookies = param[1]
                tmp_cookies = tmp_cookies.split("; ")
                for c in tmp_cookies:
                    coo = c.split("=")
                    if len(coo) == 1:
                        coo.append("")
                    self.cookies.update({coo[0].replace(" ", ""): coo[1].replace(" ", "")})
            else:
                if len(param) == 1:
                    pass
                else:
                    # if param[0] == "Accept":
                    #     tmp =
                    if param[0] == "Content-Type":
                        self.content_type = param[1]
                    if param[1].startswith(" "):
                        param[1] = param[1][1:]
                    self.headers.update({param[0]: param[1]})

        if self.method == "GET":
            if "?" in self.path:
                tmp = self.path.split("?")[1]
                if tmp != "":
                    if "&" in tmp:
                        args = tmp.split("&")
                        for arg in args:
                            arg = arg.split("=")
                            if len(arg) == 1:
                                arg.append("")
                            self.params.update({arg[0].replace(" ", ""): arg[1].replace(" ", "")})
                    else:
                        arg = tmp.split("=")
                        if len(arg) == 1:
                            arg.append("")
                        self.params.update({arg[0].replace(" ", ""): arg[1].replace(" ", "")})
            else:
                self.params = None
        else:
            if "Content-Type" in self.headers:
                r = re.findall("</.*?>", self.data)
                if "&" in self.data:
                    params_temp = self.data.split("&")
                    for param in params_temp:
                        param = param.split("=")
                        self.params.update({param[0].replace(" ", ""): param[1].replace(" ", "")})
                elif r:
                    for i in r:
                        key = i.replace("</", "").replace(">", "")
                        val = re.findall(f"<{key}>(.*)</{key}>", self.data)[0]
                        if "<" not in val and ">" not in val:
                            self.params.update({key: val})
                elif "=" in self.data:
                    param = self.data.split("=")
                    self.params.update({param[0].replace(" ", ""): param[1].replace(" ", "")})
                else:
                    self.params = None
            else:
                self.params = None

    def get_info(self):
        if self.method == "GET":
            self.res = requests.get(self.url).text
            self.status_code = requests.get(self.url, headers=self.headers).status_code
            tmp = requests.get(self.url, headers=self.headers).headers
            try:
                if tmp["Location"]:
                    self.redirect = tmp["Location"]
            except KeyError:
                self.redirect = None

        elif self.method == "POST":
            self.res = requests.post(self.url, headers=self.headers, data=self.data).text
            self.status_code = requests.post(self.url, headers=self.headers, data=self.data).status_code
            tmp = requests.post(self.url, headers=self.headers, data=self.data).headers
            try:
                if tmp["Location"]:
                    self.redirect = tmp["Location"]
            except KeyError:
                self.redirect = None

        elif self.method == "PUT":
            self.res = requests.put(self.url, headers=self.headers, data=self.data).text
            self.status_code = requests.put(self.url, headers=self.headers, data=self.data).status_code
            tmp = requests.put(self.url, headers=self.headers, data=self.data).headers
            try:
                if tmp["Location"]:
                    self.redirect = tmp["Location"]
            except KeyError:
                self.redirect = None

    def __call__(self, *args, **kwargs):
        self.get_response()
        self.get_info()
        request_dict = {"method": self.method, "protocol": self.protocol, "url": self.url, "data": self.data,
                        "cookies": self.cookies, "headers": self.headers, "params": self.params, "path": self.path,
                        "status_code": self.status_code, "response": self.res, "redirect": self.redirect}
        get_var = Dict(request_dict)
        for key, value in get_var.items():
            setattr(get_var, key.lower(), value)
        return get_var


class Make_Request:
    def __init__(self, url, method="GET", data=None, cookie=None):
        self.url = url
        self.cookie = cookie
        self.method = str(method).upper()
        self.data = data
        self.request = """@method @path HTTP/1.1
Host: @base_url
@headers@cookie
@data"""

    def check_protocol(self):
        if not self.url.startswith("http"):
            try:
                res = requests.get("http://" + self.url).url
            except requests.exceptions.MissingSchema:
                raise requests.exceptions.MissingSchema("Protocol is missing")
            self.url = str(res.split("://")[0])+self.url

    def req(self):
        res = requests.get(self.url).request.headers
        msg_header = ""
        for key, val in res.items():
            msg_header += f"{key}: {val}\n"
        self.request = self.request.replace("@headers", msg_header)

        res = requests.get(self.url).cookies
        msg_header = ""
        for key, val in res.items():
            msg_header += f"{key}: {val}; "
        self.request = self.request.replace("@cookie", "Cookie: "+msg_header+"\n")

    def start(self):
        self.check_protocol()

        self.req()
        _new = self.url.split("/")
        self.request = self.request.replace("@base_url", _new[2])
        del _new[0:3]

        path = ""
        for i in _new:
            if i != "":
                path += "/" + i
        if path == "":
            path = "/"

        self.request = self.request.replace("@path", path).replace("@method", self.method)

        if self.method == "GET":
            self.request = self.request.replace("@data", "")
        else:
            if self.data is None:
                self.request = self.request.replace("@data", "")
            else:
                self.request = self.request.replace("@data", self.data)

    def __call__(self, *args, **kwargs):
        self.start()
        request_dict = {"request": self.request}
        get_var = Dict(request_dict)
        for key, value in get_var.items():
            setattr(get_var, key.lower(), value)
        return get_var


def request_analysis(request):
    return Request_Analysis(request)()


def make_request(url, method="GET", data=None):
    res = isalive(url)
    if res == "isAlive":
        return Make_Request(url, method, data)()
