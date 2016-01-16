#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Khue Vu'
SITENAME = u'Fundamentals'
SITEURL = ''
THEME = 'theme'
PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

#DISQUS_SITENAME = "khuevu-techblog"
GOOGLE_ANALYTICS = "UA-34233563-1"

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/khuevu'),
        ('github', 'http://github.com/khuevu'),
        ('linkedin', 'http://linkedin.ch/in/khuevu'),
        ('envelope', 'mailto:khuevu@gmail.com'),)

DEFAULT_PAGINATION = 20
MD_EXTENSIONS = ['extra']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
