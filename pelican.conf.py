#!/usr/bin/env python
# -*- coding: utf-8 -*- #

SITENAME = u"Water Spinach"
AUTHOR = u"Vu Minh Khue"
AUTHOR_EMAIL = "khuevu@gmail.com"
SITEURL = '/'

TIMEZONE = 'Asia/Singapore'

DEFAULT_LANG='en'

# Blogroll
LINKS =  (
    ('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
    ('Python.org', 'http://python.org'),
    ('Jinja2', 'http://jinja.pocoo.org'),
         )

# URL
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
PAGE_URL = 'pages/{slug}.html'
PAGE_SAVE_AS = 'pages/{slug}.html'
AUTHOR_URL = 'about.html'
AUTHOR_SAVE_AS = 'about.html'
CATEGORY_URL = 'category/{name}.html'
CATEGORY_SAVE_AS = 'category/{name}.html'
TAG_URL = 'tag/{name}.html'
TAG_SAVE_AS = 'tag/{name}.html'
TAGS_SAVE_AS = 'tags.html'
ARCHIVES_SAVE_AS = 'archive.html'
#STATIC
STATIC_PATHS = ['images']
# Social widget
SOCIAL = (
          ('You can add links in your config file', '#'),
         )

DATE_FORMAT = {
        'en': '%a, %d %b %Y'
        }


# PAGINATION
DEFAULT_PAGINATION = 10 
DEFAULT_ORPHANS = 1

#SOCIAL PLUGIN
TWITTER_USERNAME = 'khuevu'
DISQUS_SITENAME = "waterspinach"
GOOGLE_ANALYTICS = "UA-34233563-1"
GITHUB_URL = "https://github.com/khuevu"

PLUGINS = ['pelican.plugins.gravatar']

MD_EXTENSIONS = ['codehilite', 'extra']
