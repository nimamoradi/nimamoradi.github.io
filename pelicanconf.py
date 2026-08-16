AUTHOR = 'Nima Moradi'
SITENAME = 'Nima Moradi | Software Engineer & AI Developer'
SITE_BRAND = 'Nima Moradi'
SITEURL = 'https://ni-moradi.com'

# Public endpoint used by the contact widget on every page.
CONTACT_FORM_ENDPOINT = 'https://formspree.io/f/xvzjllra'

PATH = 'content'
STATIC_PATHS = ['images', 'extra']

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
    ('linkedin', 'https://www.linkedin.com/in/nima-moradi/'),
    ('github', 'https://github.com/nimamoradi'),
    ('gitlab', 'https://gitlab.com/ni_moradi'),
    ('stackoverflow', 'https://stackoverflow.com/users/6138345/nima-moradi'),
    ('medium', 'https://medium.com/@ni.moradi96'),
)

# The public site has one HTTPS canonical origin. Relative canonical URLs caused
# Google to receive conflicting canonical signals from the sitemap and pages.
RELATIVE_URLS = False
THEME = 'site-theme'
THEME_STATIC_PATHS = ['static']
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['readtime', 'search', 'neighbors', 'pelican-toc', 'sitemap']

# TEMPLATE_PAGES = {'home.html': 'index.html',}

SITEMAP = {
    "format": "xml",
    # Taxonomy, search and pagination pages are useful for visitors but are thin
    # discovery pages. Keep the sitemap focused on the pages that should rank.
    "exclude": [
        r"^author[0-9]*\.html$",
        r"^category/",
        r"^tag/",
        r"^(archives|categories|tags|search|index[0-9]+)\.html$",
    ],
    "priorities": {
        "articles": 0.8,
        "indexes": 0.4,
        "pages": 0.7
    },
    "changefreqs": {
        "articles": "weekly",
        "indexes": "monthly",
        "pages": "monthly"
    }
}
SUBTITLE = 'Nima(Nick) Moradi'
SUBTEXT = '''
<details>
  <summary><b>About Me</b></summary>
  <p>
    <b>Master of Science in Computer Science - Bishop's University</b>
    <br>
    Sherbrooke - Canada
    <br><br>
    <b>Bachelor of Science in Computer Engineering - Ferdowsi University</b>
    <br>
    Mashhad - Iran
    <br><br>
    As a Software Developer, I am passionate about turning bold visions into reality through structured thinking and persistent effort. I build robust, scalable systems and thrive on the complex challenges found in high-impact projects, with a keen interest in Deep Learning, Natural Language Processing, and Mobile Development. I believe great software development is like a Dixieland jazz ensemble: a blend of individual skill, rigorous structure, and collaborative interplay. I'm always open to collaborating on forward-thinking projects with teams that value creativity and technical excellence.
    <br><br>
    Country: Canada
    <br>
    <a href="/pages/about-me.html">Read More</a>
  </p>
</details>

'''

DISPLAY_PAGES_ON_MENU = True
DIRECT_TEMPLATES = (('index', 'search', 'tags', 'categories', 'archives',))
PAGINATED_TEMPLATES = {'index': None, 'tag': None, 'category': None, 'author': None, 'archives': 24, }

# The older Pelican release in this project requires an author output path.
# Normalized author metadata now produces this single archive (not in sitemap).
AUTHOR_SAVE_AS = 'author.html'
AUTHOR_URL = 'author.html'

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
    'extra/favicon.jpg': {'path': './content/images/favicon.jpg'},  # and this
    'extra/CNAME': {'path': 'CNAME'},
    'extra/LICENSE': {'path': 'LICENSE'},
    'extra/robots.txt': {'path': 'robots.txt'},
}
