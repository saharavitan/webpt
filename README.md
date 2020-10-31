## About WebPT 

WebPT is a library for analyzing and crawling websites, the library is designed to be used by Pentesters and developers to make their code easier.


## Installation

```
git clone https://github.com/saharavitan/webpt.git
```

```
python -m pip install webpt
```

## Recommended Python Version:

WebPT currently supports **Python 3**

* The recommended version for Python 3 is **>=3.6.x**

## Dependencies:

WebPT depends on the `re`, `requests`, `bs4`, `urllib`, `threading` and `time` python modules.

These dependencies can be installed using the requirements file:

- Installation on Windows:
```
c:\python38\python.exe -m pip install -r requirements.txt
```
- Installation on Linux
```
sudo pip install -r requirements.txt
```

## Make Request Attributes

Short Form    | Description
------------- |-------------
request | Create a request

## find Attributes

Short Form    | Description
------------- |-------------
tag | Exports all found objects, some tag must be written in the function
attrs | Exports the value of the attribute from the tag


## Request Analysis Attributes

Short Form    | Description
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

Short Form    | Description
------------- |-------------
links | Exports all links found to the list
gui | Graphic display of the site

### Examples



## Using WebPT as a module in your python scripts

**MakeRequest Example**

```python
import webpt 
request = webpt.make_request(url, method='POST', data="param1=val1&param2=val2").request
```

```python
import webpt 
request = webpt.make_request(url).request
```

**Spider Example**
 
```python
import webpt 
get_links = webpt.spider("https://example.com").links
```

```python
import webpt 
print(webpt.spider("https://example.com").gui)
```

**Response Analysis Example**

```python
import webpt 
tags = webpt.find(source).tag('script')
for tag in tags:
    res = find().attrs(test, "src")
```

**PortScanner Example**

```python
import webpt 
ports = webpt.scanport(url/ip)
```

**Request Analysis Example**

```python
import webpt 

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


## Author

* [SaharAvitan](https://twitter.com/avitansahar).

## Version
**Current version is 1.0**
