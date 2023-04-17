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
DEFAULT_PAGINATION = 8
GITHUB_URL = 'https://github.com/nimamoradi'

# Social widget
SOCIAL = (
    ('twitter', 'https://twitter.com/ni_moradi'),
    ('linkedin', 'https://www.linkedin.com/in/nima-moradi/'),
    ('github', 'https://github.com/nimamoradi'),
    ('gitlab', 'https://gitlab.com/ni_moradi'),
    ('stackoverflow', 'https://stackoverflow.com/users/6138345/nima-moradi'),
    ('medium', 'https://medium.com/@ni.moradi96'),
    ('instagram', 'https://instagram.com/ni_moradi'),
)

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
THEME = 'themes/Papyrus'
THEME_STATIC_PATHS = ['static']
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['readtime', 'search', 'neighbors', 'pelican-toc']

# TEMPLATE_PAGES = {'home.html': 'index.html',}

SUBTITLE = 'Nima Moradi'
SUBTEXT = '''
<b>Bachelor of Science in Computer engineering - Ferdowsi University
</b>
<br>
Mashhad - Iran
<br>
2015 - 2020
<br>
<br>
<b>
Master Degree in Computer Science - Bishop's University
</b>
<br>
Sherbrooke - Canada
<br>
<br>

I have a keen interest in the fields of Deep Learning, Natural Language Processing, Software Development, and Android App Development. In particular, I am fascinated by the potential of these technologies to solve complex problems and create innovative solutions. I am always eager to learn more and stay up-to-date with the latest advancements in these fields.
<br>
<pre>
Country: Canada
Email: me[at]ni-moradi[dot]com, ni.moradi96[at]gmail[dot]com
</pre>
<br>
'''

DISPLAY_PAGES_ON_MENU = True
DIRECT_TEMPLATES = (('index', 'search', 'tags', 'categories', 'archives',))
PAGINATED_TEMPLATES = {'index': None, 'tag': None, 'category': None, 'author': None, 'archives': 24, }

# Site search plugin
SEARCH_MODE = "output"
SEARCH_HTML_SELECTOR = "main"
# Table of Content Plugin
TOC = {
    'TOC_HEADERS': '^h[1-3]',  # What headers should be included in
    # the generated toc
    # Expected format is a regular expression
    'TOC_RUN': 'true',  # Default value for toc generation,
    # if it does not evaluate
    # to 'true' no toc will be generated
    'TOC_INCLUDE_TITLE': 'false',  # If 'true' include title in toc
}

# Article share widgets
SHARE = (
    ("twitter", "https://twitter.com/intent/tweet/?text=Features&amp;url="),
    ("linkedin", "https://www.linkedin.com/sharing/share-offsite/?url="),
    ("reddit", "https://reddit.com/submit?url="),
    ("facebook", "https://facebook.com/sharer/sharer.php?u="),
    ("whatsapp", "https://api.whatsapp.com/send?text=Features - "),
    ("telegram", "https://telegram.me/share/url?text=Features&amp;url="),
)
EXTRA_PATH_METADATA = {
    'extra/favicon.jpg': {'path': 'favicon.jpg'},  # and this
    'extra/CNAME': {'path': 'CNAME'},
    'extra/LICENSE': {'path': 'LICENSE'}
}