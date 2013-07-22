#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Copyright (C) 
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; If not, see <http://www.gnu.org/licenses/>.
# 
# 2013 - Long Changjin <admin@longchangjin.cn>

import xmlrpclib
import pycurl
import StringIO
import urllib


class RPCProxy(object):
    def __init__(self, uri, encoding=None, allow_none=0,
                 proxy_host=None, proxy_port=None):
        super(RPCProxy, self).__init__()
        # get the url
        if urllib.splittype(uri)[0] not in ("http", "https"):
            raise IOError("unsupported XML-RPC protocol")
        self.__url = uri
        self.__encoding = encoding
        self.__allow_none = allow_none
        self.__proxy_host = proxy_host
        self.__proxy_port = proxy_port

    def __repr__(self):
        return ("<RCPProxy for %s%s>" % (self.__host, self.__handler))

    __str__ = __repr__

    def __call__(self, method_name, *args):
        request = xmlrpclib.dumps(args, method_name, encoding=self.__encoding,
                                  allow_none=self.__allow_none)
        crl = pycurl.Curl()
        # set proxy
        if self.__proxy_host:
            crl.setopt(pycurl.PROXY, self.__proxy_host)
        if self.__proxy_port:
            crl.setopt(pycurl.PROXYPORT, self.__proxy_port)

        crl.setopt(pycurl.HTTPPROXYTUNNEL, 1)
        crl.setopt(pycurl.USERAGENT, "LC RPCProxy")

        crl.setopt(pycurl.SSL_VERIFYPEER, 0)
        crl.setopt(pycurl.SSL_VERIFYHOST, 0)

        crl.setopt(pycurl.CONNECTTIMEOUT, 60)
        crl.setopt(pycurl.TIMEOUT, 300)

        crl.fp = StringIO.StringIO()
        crl.setopt(pycurl.POSTFIELDS,  request)
        crl.setopt(pycurl.URL, self.__url)
        crl.setopt(crl.WRITEFUNCTION, crl.fp.write)
        crl.perform()
        data = xmlrpclib.loads(crl.fp.getvalue())[0]
        crl.fp.close()
        crl.close()
        return data
