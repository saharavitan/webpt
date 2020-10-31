import requests
import re
requests.packages.urllib3.disable_warnings() # noqa


class Find:
    def __init__(self, src=None):
        if src is not None:
            self.src = src.replace("\n", "").replace("\r", "").replace("\t", "")
        else:
            self.src = ""
        self.tag_list = None

    def tag(self, tag):
        self.tag_list = re.findall(f"<{tag} .*?</{tag}>", self.src)
        if not self.tag_list:
            self.tag_list += re.findall(f"<{tag} .*?>", self.src)
        return self.tag_list

    def attrs(self, full_tag, attribute): # noqa
        att_list = []
        match = re.search(r'{}=[\'"]?([^\'" >]+)'.format(attribute), full_tag)
        if match:
            att_list.append(match.group(1))
        if att_list:
            return att_list
        else:
            return None


def find(src=None):
    return Find(src)
