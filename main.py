# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import web
import random
import time


# stop the autoreload mode of web.py
web.config.debug = False
urls = (
    '/', 'Index',
)
class Index:
    def __init__(self):
        self.ret = dict()
        self.ret["code"] = 0
        self.ret["data"] = ""
        self.res= open('res.html').read()
        self.res2= '</div></body></html>'
        print 'init'
       
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        x = web.input()
        if(len(x)>0 and x.has_key('data') and len(x['data'])>0 and x.has_key('type') and len(x['type'])>0):
            cmd = "python predicat.py %s %s " % (x['data'],x['type'] )
            result = os.popen(cmd.encode('utf8')).readlines()
            if(x['type']=='0'):
                return self.res +"<h3>给定开头</h3><h3>" + result[-1] + "</h3>" + self.res2
            else:
                return self.res +"<h3>藏头诗</h3><h3>" + result[-1] + "</h3>" + self.res2
        else:
            return self.res  + self.res2

        return self.res
if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
