AUTHOR = 'Nima Moradi'
SITENAME = 'Nima Moradi Personal blog'
SITEURL = 'ni-moradi.com'

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Article summary length on main index page
SUMMARY_MAX_LENGTH = 100
DEFAULT_PAGINATION = 10
GITHUB_URL = 'https://github.com/nimamoradi'

# Social widget
SOCIAL = (
    ('twitter', 'https://twitter.com/ni_moradi'),
    ('linkedin', 'https://www.linkedin.com/in/nima-moradi/'),
    ('github', 'https://github.com/nimamoradi'),
    ('gitlab', 'https://gitlab.com/ni_moradi'),
    ('instagram', 'https://instagram.com/ni_moradi'),
)


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
THEME = 'themes/Peli-Kiera'
PLUGIN_PATHS = ['plugins']
PLUGINS = ['readtime', 'neighbors']