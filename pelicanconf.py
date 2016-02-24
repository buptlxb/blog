#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

SITEURL = u'http://gotit.applinzi.com'
AUTHOR = u'ictlxb'
SITENAME = u'BLxG'
THEME = 'tuxlite_tbs'

PATH = 'content'
STATIC_PATHS = ['assets']

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh-CN'

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
SOCIAL = (('Github', 'https://github.com/buptlxb'),
          (u'Weibo','http://weibo.com/ictlxb'),)

DEFAULT_PAGINATION = 5 

TAGCLOUD = True
TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100

DISQUS_SITENAME = 'blxg'


# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['sitemap']
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.7,
        "indexes": 0.5,
        "pages": 0.3,
    },
    "changefreqs": {
        "articles": "monthly",
        "indexes": "daily",
        "pages": "monthly",
    }
}
