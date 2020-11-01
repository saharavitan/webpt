# Authors : Sahar Avitan & Eden Zaraf

import re
import requests
requests.packages.urllib3.disable_warnings() # noqa


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
    def __init__(self, tag, element):
        self.tag = tag
        self.element = element

    def __str__(self):
        return self.element

    def attr(self, attribute): # noqa
        att_list = []
        match = re.search(r'{}=[\'"]?([^\'" >]+)'.format(attribute), self.element)
        if match:
            att_list.append(match.group(1))
        if att_list:
            return att_list
        else:
            return None


class Tags:
    def __init__(self, tag, src):
        self.num = 0
        self.tag = tag
        self.tag_list = []
        tmp_tag_list = re.findall(f"<{tag} .*?</{tag}>", src)
        if not tmp_tag_list:
            tmp_tag_list += re.findall(f"<{tag} .*?>", src)
        else:
            for i in tmp_tag_list:
                self.tag_list.append(Tag(tag, i))

    def __str__(self):
        return self.tag_list

    def __iter__(self):
        return self

    def __next__(self):
        num = self.num
        self.num += 1
        if len(self.tag_list) > num:
            return self.tag_list[num]
        raise StopIteration


def find(source=None):
    return Find(source)
