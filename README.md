## About WebPT 

WebPT is a library for analyzing and crawling websites, the library is designed to be used by Pentesters and developers to make their code easier.


## Installation

```
git clone https://github.com/saharavitan/webpt.git
```

```
python -m pip install webpt
```

Requires Python **3.8+**


## Dependencies:

WebPT depends on the `re`, `requests`, `urllib`, `threading` and `time` python modules.

These dependencies can be installed using the requirements file:

- Installation on Windows:
```
python -m pip install -r requirements.txt
```
- Installation on Linux
```
pip install -r requirements.txt
```

## Vulnerability Functions

* For PoC write webpt.clickjacking(url).poc

Functions    | Description   |  Params
------------- |-------------  | -------------
all | Check for all vulnerabilities | url
clickjacking | Check for ClickJacking| url
wordpress | Tests 7 different vulnerabilities for wordpress | url
cookie_not_secure | Checks for cookies that are not set as Secure | url
xss_protection | Checks for XSS-Protection header | url
sri | Checks for SRI vulnerabilities in the code | url
htaccess | Check if htaccess file is readable | url
comments | Get all comment from source code and check by regex | url, regex
ip_disclosure | Checks for internal IP addresses in the source code  | url
fortinet | Tests 3 different vulnerabilities for Fortinet  | url / ip
cisco    |    Tests 2 different vulnerabilities for Cisco  | url / ip

## Make Request Attributes

Attributes    | Description
------------- |-------------
request | Create a request

## Find Functions - HTML Analysis

Functions    | Description   |  Params
------------- |------------- | -------------
tag | Exports all found objects, some tag must be written in the function | tag
attr | Exports the value of the attribute from the tag | Attributes
element | Get all Attributes and value to Dictionary | Element```<input type="text" id="2" value="example" placeholder="hello">```
send_form | Receives all forms and sends them with the option to change values ​​to parameters  |  param_name, new_value
mails | Get mails from source | Nothing


## Request Analysis Attributes

Attributes    | Description
------------- |-------------
method | Type of method
protocol | Type of protocol (GET, POST...)
url            | Get url
data           | Returns the data from the request within a dictionary
cookies            | Returns the data from the cookies within a dictionary 
headers            | Returns the data from the headers within a dictionary
params            | Returns the data from the params within a dictionary
path            | The path of the url
status_code            | The status code of the response
response            | The content of the response
redirect        |  To which address the server will redirect

## Spider Attributes

* The spider is a tool that is used to automatically discover new resources (URLs) on a particular Site.

Attributes    | Description
------------- |-------------
links | Exports all links found to the list
gui | Graphic display of the site
js | Exports all JS link to list

## Other Functions

Functions    | Description   | Params 
------------- |------------- |-------------
myip | Get your IP | -
call_attr | Make your own attributes to dictionary | dictionary

### Examples

## Using WebPT as a module in your python scripts

**MakeRequest Example**

```python
request = webpt.make_request(url, method='POST', data="param1=val1&param2=val2").request
```

```python
request = webpt.make_request(url).request
```


**Vuln Example**

```python
res = webpt.vuln.clickjacking(url)
```
* Poc can be exported using the following command:

```python
res = webpt.vuln.wordpress(url)
```
```python
res = webpt.vuln.all(url)
```
```python
res = webpt.vuln.comments("https://example.com").find("password")
```

**Subdomain Example**
```python
links = webpt.subdomains("example.com")
```

**Spider Example**

```python
get_links = webpt.spider("https://example.com").links
```

```python 
print(webpt.spider("https://example.com").gui)
```

**HTML Analysis - Response Analysis Example**
```python
src = requests.get(f'https://www.example.co.il/').text
tags = webpt.find(src).tag("form")
for tag in tags:
    webpt.send_form(tag.element).change("sadasda", "sahar")
```
```python
tags = webpt.find(source).tag("a")
for tag in tags:
    res = tag.attr("href")
```
```python
tags = webpt.find(source).tag("a").list
for tag in tags:
    webpt.element(tags[0])
```
```python
mails = webpt.find(source).mails()
```
**PortScanner Example**

```python
ports = webpt.scanport(url/ip)
```
```python
ports = webpt.scanport(url/ip, from, to)
```
**Request Analysis Example**

```python
request = """POST /api/scope.php HTTP/1.1
Host: example.com
Connection: close
Content-Length: 69
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: https://example.com
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://example.com/
Accept-Encoding: gzip, deflate
Accept-Language: he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: __cfduid=d77a6a7e8c8303932379a959c941da11a1604046519; PHPSESSID=fpehjl7lamt1akovf990bd2gfl

csrf=3dff02bd9e7f4d014ff7218d2f3a80dc&target=https%3A%2F%2Fexample.co.il"""

req = webpt.request_analysis(request)

method = req.method
protocol = req.protocol
url = req.url
data = req.data
headers = req.headers
params = req.params
path = req.path
status_code = req.status_code
response = req.response
redirect = req.redirect
```

**Other Functions**

```python
IP = webpt.myip()
```
```python
full_name = webpt.call_attr({"first": "Sahar", "last": "Avitan"})
print(full_name.first)
print(full_name.last)

Results:
Sahar
Avitan
```

## Author

* [SaharAvitan](https://twitter.com/avitansahar)

## Version
**Current version is 2.1.6**

## What's new

* From the new webpt update you can scan subdomains with the highest results
(Example code above) - ```.subdomains()```

* In the new update you can search for vulnerabilities automatically with a webpt.
12 vulnerabilities have been added, more to come soon.
(Example code above) - ```.vuln```

* Forms that exist on the site can be sent with a change of parameter / value.
(Example code above) - ```.send_form()```

* Element can be analyzed according to Attributes and value, Return in Dict. (Example code above) - ```.element()```

* What's my IP? (Example code above) - ```.myip()```

* In the new update you can encrypt and decrypt the following types:
```md5, sha1, sha256, sha512```.
To decrypt these hash (```md5, sha1, sha256, sha512```) you have to perform Brute Force that we wrote specifically.
(Example code above) - ```.hash()```

* You can insert a dictionary for a function called ```.call_attr()```, Once we call the function we can put "." at the end,
And add a key in the dictionary.

* Parts of the code have been ```repaired``` and ```improved```

* License updated to ```Apache License```

* you will be able to find the full documentation at this link soon : https://web-pt.com