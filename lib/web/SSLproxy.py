# urllib2 opener to connection through a proxy using the CONNECT method, (useful for SSL)
# tested with python 2.4

"""Code from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/456195 modified by comments on the same page."""

import urllib2
import urllib
import httplib
import socket


class ProxyHTTPConnection(httplib.HTTPConnection):

    _ports = {'http' : 80, 'https' : 443}


    def request(self, method, url, body=None, headers={}):
        #request is called before connect, so can interpret url and get
        #real host/port to be used to make CONNECT request to proxy
        proto, rest = urllib.splittype(url)
        if proto is None:
            raise ValueError, "unknown URL type: %s" % url
        #get host
        host, rest = urllib.splithost(rest)
        #try to get port
        host, port = urllib.splitport(host)
        #if port is not defined try to get from proto
        if port is None:
            try:
                port = self._ports[proto]
            except KeyError:
                raise ValueError, "unknown protocol for: %s" % url
        self._real_host = host
        self._real_port = port
        httplib.HTTPConnection.request(self, method, url, body, headers)


    def connect(self):
        httplib.HTTPConnection.connect(self)
        #send proxy CONNECT request
        self.send("CONNECT %s:%d HTTP/1.0\r\n\r\n" % (self._real_host, self._real_port))
        #expect a HTTP/1.0 200 Connection established
        response = self.response_class(self.sock, strict=self.strict, method=self._method)
        (version, code, message) = response._read_status()
        #probably here we can handle auth requests...
        if code != 200:
            #proxy returned and error, abort connection, and raise exception
            self.close()
            raise socket.error, "Proxy connection failed: %d %s" % (code, message.strip())
        #eat up header block from proxy....
        while True:
            #should not use directly fp probablu
            line = response.fp.readline()
            if line == '\r\n': break


class ProxyHTTPSConnection(ProxyHTTPConnection):

    default_port = 443

    def __init__(self, host, port = None, key_file = None, cert_file = None, strict = None):
        ProxyHTTPConnection.__init__(self, host, port)
        self.key_file = key_file
        self.cert_file = cert_file

    def connect(self):
        ProxyHTTPConnection.connect(self)
        #make the sock ssl-aware
        ssl = socket.ssl(self.sock, self.key_file, self.cert_file)
        self.sock = httplib.FakeSocket(self.sock, ssl)

class ConnectHTTPHandler(urllib2.HTTPHandler):
    """Code from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/456195 from comment Norm Petterson, 2006/05/04"""
    def __init__(self, proxy=None, debuglevel=0):
        self.proxy = proxy
        urllib2.HTTPHandler.__init__(self, debuglevel)

    def do_open(self, http_class, req):
        if self.proxy is not None:
            req.set_proxy(self.proxy, 'http')
        return urllib2.HTTPHandler.do_open(self, ProxyHTTPConnection, req)

class ConnectHTTPSHandler(urllib2.HTTPSHandler):
    """Code from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/456195 from comment Norm Petterson, 2006/05/04"""

    def __init__(self, proxy=None, debuglevel=0):
        self.proxy = proxy
        urllib2.HTTPSHandler.__init__(self, debuglevel)

    def do_open(self, http_class, req):
        if self.proxy is not None:
            req.set_proxy(self.proxy, 'https')
        return urllib2.HTTPSHandler.do_open(self, ProxyHTTPSConnection, req)

class ConnectHTTPSOverHTTPHandler(urllib2.HTTPHandler):
    """ Try to include code from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/456195 from comment yin sun, 2006/06/16 """
    def __init__(self, proxy=None, debuglevel=0):
        self.proxy = proxy
        urllib2.HTTPSHandler.__init__(self, debuglevel)

    def do_open(self, http_class, req):
        if self.proxy is not None:
            req.set_proxy(self.proxy, 'https')
        return urllib2.HTTPHandler.do_open(self, ProxyHTTPSConnection, req)

if __name__ == '__main__':

    import sys

    opener = urllib2.build_opener(ConnectHTTPHandler, ConnectHTTPSHandler)
    urllib2.install_opener(opener)
    req = urllib2.Request(url='https://192.168.1.1')
    req.set_proxy('192.168.1.254:3128', 'https')
    f = urllib2.urlopen(req)
    print f.read()
