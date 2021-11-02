import os

from flask import Flask
from flask_assets import Environment, Bundle
from webassets.filter import register_filter

from lso import consts
from lso import filters
from lso.sass_dart import SassDart
from lso.views.api import bp as api
from lso.views.guide import bp as guide
from lso.views.site import bp as site
from lso.views.tools import bp as tools
from lso.views.vyakarana import bp as vyakarana

app = Flask(__name__)


# Config
# ------

app.config["MAILING_LIST_URL"] = consts.MAILING_LIST_URL


# Static assets
# -------------

register_filter(SassDart)
assets = Environment(app)
css = Bundle("css/style.css", "css/style-reset.css", output="gen/style.css")
assets.register("css_legacy_all", css)

# CSS
css = Bundle(
    "css/style.scss",
    filters="sass-dart",
    depends="css/*.scss",
    output="gen/style-all.css",
)
assets.register("css_all", css)

css = Bundle(
    "css/print.scss",
    filters="sass-dart",
    output="gen/print.css",
)
assets.register("css_print", css)


js = Bundle("scripts/sanscript.js", "scripts/main.js", output="gen/main.js")
assets.register("js_all", js)

# Sass configuration
_py_dir = os.path.dirname(__file__)
_project_dir = os.path.dirname(_py_dir)
app.config["SASS_BIN"] = os.path.join(_project_dir, "node_modules", ".bin", "sass")
app.config["SASS_LINE_COMMENTS"] = False


# Views and filters
# -----------------

# Can't use `api` for some reason
app.register_blueprint(api)
app.register_blueprint(guide)
app.register_blueprint(vyakarana)
app.register_blueprint(site)
app.register_blueprint(tools)

app.jinja_env.filters.update(
    {
        "sml": filters.sml,
        "d": filters.devanagari,
        "i": filters.roman,
        "t": filters.transliterate_generic,
        "sa2": filters.sa2,
    }
)
