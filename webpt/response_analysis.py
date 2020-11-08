# Authors : Sahar Avitan & Eden Zaraf
import re
import requests


class Dict(dict):
    def __getattr__(self, item):
        pass


class Find:
    def __init__(self, source=None):
        if isinstance(source, str):
            self.src = source.replace("\n", "").replace("\r", "").replace("\t", "")
        else:
            raise TypeError("The source should be a string")

    def tag(self, tag):
        return Tags(tag, self.src)

    def emails(self):
        match = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', self.src) # noqa
        return match


class Tag:
    def __init__(self, tag, element): # noqa
        self.tag = tag
        self.element = element

    def __str__(self):
        return str(self.element)

    def attr(self, attribute): # noqa
        att_list = []
        m = re.compile(f'{attribute} ?= ?[\'"]?([^\'"]+)[^a-z]*=? ?')
        match = m.search(self.element)
        try:
            if match:
                if match.group(1):
                    att_list.append(match.group(1))
                if att_list:
                    return att_list[0]
        except: # noqa
            pass


    def text(self): # noqa
        text = re.findall(f'<.*>(.*?)<.*>', self.element)
        if text:
            return text[0]


class Attributes:
    def __init__(self, element): # noqa
        self.element = element
        self.tag = self.element.split(" ")[0].replace("<", "")
        self.elem_dic = {"tag": self.tag}

    def __call__(self, *args, **kwargs):
        attributes = re.findall(f' (.*?)=.', self.element)

        for attribute in attributes:
            if " " not in attribute:
                m = re.compile(f'{attribute} ?= ?[\'"]?([^\'"]+)[^a-z]*=? ?')
                match = m.search(self.element)

                if match:
                    if match.group(1):
                        self.elem_dic.update({attribute: match.group(1)})

        get_var = Dict(self.elem_dic)
        for key, value in get_var.items():
            setattr(get_var, key.lower(), value)
        return get_var


class Tags:
    def __init__(self, tag, src):
        self.num = 0
        self.tag = tag
        self.tag_list = []
        self.tags_str = []
        # if tag is not None:
        tmp_tag_list = re.findall(f"<{tag} ?.*?</{tag}>", src)

        if not tmp_tag_list:
            tmp_tag_list += re.findall(f"<{tag} ?.*?>", src)
            for i in tmp_tag_list:
                self.tags_str.append(i)
                self.tag_list.append(Tag(tag, i))
        else:
            for i in tmp_tag_list:
                self.tags_str.append(i)
                self.tag_list.append(Tag(tag, i))

    def list(self):
        return self.tags_str

    def __str__(self):
        return str(self.tag_list)

    def __iter__(self):
        return self

    def __next__(self):
        num = self.num
        self.num += 1
        if len(self.tag_list) > num:
            return self.tag_list[num]
        raise StopIteration


class Send_Form:
    def __init__(self, form):
        self.form = form
        self.method = None
        self.action = None
        self.data = {}
        self.dic = {}
        self.src = None
        self.url = None

    def get_tags(self):
        tag = find(self.form.lower()).tag("form")
        for t in tag:
            self.action = t.attr("action")
            self.method = t.attr("method")

        inputs = find(self.form).tag("input")
        textareas = find(self.form).tag("textarea")
        for inp in inputs:
            input_name = inp.attr("name")
            input_value = inp.attr("value")
            if input_value is None:
                input_value = ""
            self.data.update({input_name: input_value})
        for textar in textareas:
            textar_name = textar.attr("name")
            textar_value = textar.text()
            if textar_name is not None:
                if textar_value is None:
                    textar_value = ""
                self.data.update({textar_name: textar_value})

    def make_req(self):
        if self.method is None or self.method.lower() == "get":
            msg = "?"
            for key, val in self.data.items():
                msg += f"{key}={val}&"
            if msg.endswith("&"):
                msg = msg[:-1]

            url = f"{self.action}{msg}"
            self.src = requests.get(url).text
        elif self.method.lower() == "post":
            self.src = requests.post(self.action, data=self.data).text

    def change(self, param_name=None, new_value=None):
        self.get_tags()
        if param_name is not None and new_value is not None:
            self.data[param_name] = new_value
        self.make_req()

        self.dic.update({"text": self.src, "url": self.url, "data": self.data})
        get_var = Dict(self.dic)
        for key, value in get_var.items():
            setattr(get_var, key.lower(), value)
        return get_var


def find(source=None):
    return Find(source)


def send_form(form):
    return Send_Form(form)


def element(element): # noqa
    return Attributes(element)()
