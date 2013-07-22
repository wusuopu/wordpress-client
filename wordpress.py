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

import my_xmlrpc


class WordPress(object):
    def __init__(self, url, username, password,
                 proxy_host=None, proxy_port=None):
        self.rpc = my_xmlrpc.RPCProxy(url, proxy_host=proxy_host,
                                      proxy_port=proxy_port)
        self.username = username
        self.password = password
        try:
            self.supported_methods = self.rpc('mt.supportedMethods')[0]
        except:
            raise Exception("获取函数列表出错！")
            self.supported_methods = []

    def __call__(self, method_name, *args, **kwargs):
        assert (method_name in self.supported_methods)
        try:
            if 'user_info_pos' in kwargs:
                args = list(args)
                args.insert(kwargs['user_info_pos'], self.password)
                args.insert(kwargs['user_info_pos'], self.username)
            return self.rpc(method_name, *args)
        except:
            return ['']

if __name__ == '__main__':
    wp = WordPress("http://127.0.0.1/wordpress/xmlrpc.php", 'admin', '1')
    #print wp.supported_methods
    print wp('blogger.getUserInfo', 0, user_info_pos=1)
    print wp('wp.getTags', 0, user_info_pos=1)
    # metaWeblog.getPost(postid, username, password)
    print wp('metaWeblog.getPost', 10, user_info_pos=1)
    #content = {}
    #content['title'] = u"来自my xml-rpc2"   # 标题
    #content['description'] = u"xml-rpc测试！！！！！！！！<b>sdff</b><p> </p><img src=''>"         # 正文

    #import datetime
    #content['dateCreated'] = datetime.datetime.now()

    #content['mt_allow_comments'] = 1    # 允许评论
    #content['mt_allow_pings'] = 1       # 允许trackbacks
    #content['mt_keywords'] = u"xml-rpc test, api测试"        # tags 不存在会自动创建
    ##content['mt_excerpt'] = ""          #
    ##content['mt_text_more'] = ""        #

    #content['categories'] = [U"新的分类", u'分类2']   # 分类  需要先手动创建分类
    #print wp("metaWeblog.newPost", 0, 'admin', '1', content, True)
