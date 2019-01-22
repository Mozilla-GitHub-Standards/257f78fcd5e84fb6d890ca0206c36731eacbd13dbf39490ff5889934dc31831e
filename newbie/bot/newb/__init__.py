from flask import Flask, request, render_template, redirect, url_for, session, make_response, Response, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils import create_database, database_exists

import slackclient

from apscheduler.schedulers.background import BackgroundScheduler

import holidays

import logging.config
# auth
from flask_cors import CORS as cors
from flask_environ import get, collect, word_for_true
from authlib.flask.client import OAuth
from functools import wraps
from newb import auth, config, settings

# endauth


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('newbie')
scheduler = BackgroundScheduler()




# current_host = 'https://nhobot.ngrok.io'
# current_host = 'https://newbie-stage.mozilla-slack.app'
current_host = None

app = Flask(__name__, static_url_path='/static')
app.secret_key = settings.MONGODB_SECRET
sdu = settings.SQLALCHEMY_DATABASE_URI + settings.SQLALCHEMY_DATABASE_USER \
      + ':' + settings.SQLALCHEMY_DATABASE_USER_PASSWORD + '@' + settings.SQLALCHEMY_DATABASE_HOST + '/' \
      + settings.SQLALCHEMY_DATABASE_DB
app.config['SQLALCHEMY_DATABASE_URI'] = sdu
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/newbie'
app.debug = True
app.use_reloader = False
app.jinja_env.cache = {}
cors(app)
app.logger.info(f'SQLALCHEMY_DATABASE_URI {app.config["SQLALCHEMY_DATABASE_URI"]}')
db_url = app.config["SQLALCHEMY_DATABASE_URI"]
if not database_exists(db_url):
    create_database(db_url)
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET
client_uri = settings.CLIENT_URI
client_audience = settings.CLIENT_AUDIENCE

slack_verification_token = settings.SLACK_VERIFICATION_TOKEN

slack_client = slackclient.SlackClient(settings.SLACK_BOT_TOKEN)

all_timezones = settings.all_timezones
us_holidays = holidays.US()
ca_holidays = holidays.CA()


# auth
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=settings.AUTH_ID,
    client_secret=settings.AUTH_SECRET,
    api_base_url='https://' + settings.AUTH_HOST,
    access_token_url='https://' + settings.AUTH_HOST + '/oauth/token',
    authorize_url='https://' + settings.AUTH_HOST + '/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)

app.config.update(collect(
    get('DEBUG', default=True, convert=word_for_true),
    get('HOST', default='localhost'),
    get('PORT', default=5000, convert=int),
    get('AUTH_ID', default=settings.AUTH_ID),
    get('AUTH_SECRET', default=settings.AUTH_SECRET),
    get('AUTH_HOST', default=settings.AUTH_HOST),
    get('AUTH_SCOPE', default='openid email profile'),
    get('AUTH_AUDIENCE', default=settings.AUTH_AUDIENCE),
    get('AUTH_SECRET_KEY', default=settings.AUTH_SECRET_KEY)))

AUTH_AUDIENCE = settings.AUTH_AUDIENCE
if AUTH_AUDIENCE is '':
    AUTH_AUDIENCE = 'https://' + app.config.get('HOST') + '/userinfo'

# This will be the callback URL Auth0 returns the authenticate to.
# app.config['AUTH_URL'] = 'https://{}:{}/callback/auth'.format(app.config.get('HOST'), app.config.get('PORT'))
# app.config['AUTH_URL'] = 'http://{}:{}/callback/auth'.format(app.config.get('HOST'), 8000)
# app.config['AUTH_URL'] = 'https://nhobot.ngrok.io/callback/auth'
app.config['AUTH_URL'] = 'https://newbie-stage.mozilla-slack.app/callback/auth'


oidc_config = config.OIDCConfig()
authentication = auth.OpenIDConnect(
    oidc_config
)
oidc = authentication.auth(app)
# endauth