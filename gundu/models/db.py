# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.get('db.uri'), 
             pool_size = myconf.get('db.pool_size'),
             migrate_enabled = myconf.get('db.migrate'),
             check_reserved = ['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
db.define_table("teams",
Field("name",requires=IS_NOT_EMPTY(),unique=True),
Field("moderator","reference auth_user",readable=False,writable=False,default=None),
auth.signature
)
db.define_table("agenda",
Field("title",requires=IS_NOT_EMPTY(),unique=True),
Field("objective",requires=IS_NOT_EMPTY()),
Field("stime","datetime",requires=IS_NOT_EMPTY(),label="start time"),
Field("venue",requires=IS_NOT_EMPTY()),
Field("calledby",requires=IS_NOT_EMPTY()),
Field("invo",label="special invitees"),
Field("teams",readable=False,writable=False),
auth.signature
)
db.define_table("tble",
Field("teams","reference teams",unique=True),
Field("person","reference auth_user",default=auth.user_id),
)
db.define_table("topic",
Field("agenda","reference agenda",readable=False,writable=False),
Field("title","string",requires=IS_NOT_EMPTY()),
Field("Des","text",label="Description",requires=IS_NOT_EMPTY()),
Field("stime",label="Time alloted"),
auth.signature
)
db.define_table("minutes",
                Field("Reference","string",requires=IS_NOT_EMPTY()),
                Field("agenda","reference agenda"),
                Field("teams","reference teams"),
)
db.define_table("mail1",
                Field("subject","string",requires=IS_NOT_EMPTY()),
                Field("body","text",requires=IS_NOT_EMPTY()),
                Field("teams",readable=False,writable=False),
                Field("moderator",readable=False,writable=False),
                auth.signature
    )

from gluon.contrib.login_methods.rpx_account import RPXAccount
auth.settings.actions_disabled=['register','change_password','request_reset_password']
auth.settings.login_form = RPXAccount(request,
                                      api_key='0ac3875cfa8101c1fca35ca50ef725b3d9bd6808',
                                      domain='minutes',
                                      url = "http://localhost:8000/%s/default/user/login" % request.
                                      application)
