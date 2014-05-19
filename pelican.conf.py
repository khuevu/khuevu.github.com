#!/usr/bin/env python
# -*- coding: utf-8 -*- #

SITENAME = u"Water Spinach"
AUTHOR = u"Vu Minh Khue"
AUTHOR_EMAIL = "khuevu@gmail.com"
SITEURL = 'http://khuevu.com'
TIMEZONE = 'Asia/Singapore'
LOCALE = ('en_US')

FEED_DOMAIN = 'http://feeds.khuevu.com'
FEED_ALL_RSS = 'feeds/all.rss.xml'
FEED_ALL_ATOM = 'feeds/all.atom.xml'

USE_FOLDER_AS_CATEGORY = True
DEFAULT_CATEGORY = 'Programming'

MD_EXTENSIONS = ['codehilite(css_class=highlight)','extra']

# code blocks with line numbers
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

LINKS =  (
    ('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
    ('Python.org', 'http://python.org'),
    ('Jinja2', 'http://jinja.pocoo.org'),
         )

SOCIAL = (('twitter', 'http://twitter.com/khuevu'),
                    ('github', 'http://github.com/khuevu'),)

DEFAULT_DATE = 'fs'

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'

EXTRA_PATH_METADATA = {
        'extra/robots.txt': {'path': 'robots.txt'}
    }

STATIC_PATHS = ['images', 'extra/robots.txt']

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
TAGS_URL = 'tags.html'
TAGS_SAVE_AS = 'tags.html'
ARCHIVES_SAVE_AS = 'archive.html'
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'


DATE_FORMAT = {
        'en': '%a, %d %b %Y'
        }

DEFAULT_PAGINATION = 10
DEFAULT_ORPHANS = 1


TWITTER_USERNAME = 'khuevu'
DISQUS_SITENAME = "waterspinach"
GITHUB_URL = "https://github.com/khuevu"

GOOGLE_ANALYTICS = "UA-34233563-1"

TAG_CLOUD_STEPS = 4
TAG_CLOUD_MAX_ITEMS = 100

THEME = 'themes/responsive'

TYPOGRIFY = True
# for Development
RELATIVE_URLS = True

PLUGIN_PATH='/Users/khuevu/Projects/pelican-plugins'
PLUGINS = ['representative_image']
