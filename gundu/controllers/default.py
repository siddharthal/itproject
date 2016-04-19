# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
@auth.requires_login()
def c_team():
    form = SQLFORM(db.teams)#.process(next=URL('index'))
    if form.process().accepted:
    	response.flash = "team created"
        q=db(db.teams.id>0).select(orderby=~db.teams.created_on)
        r=db(db.tble.id>0).select(db.tble.id)
        if q[0].id not in r:
            db.tble.insert(teams=q[0].id,person=auth.user_id)
    elif form.errors:
        response.flash = "Errors"
    else:
        response.flash = "Please fill the form"
    return locals()
@auth.requires_login()
def chooseteam():
    if session.var is 1:
        response.flash="team choosen"
        session.var=0
    elif session.var is 2:
        response.flash="already in the team"
        session.var=0
    else:
        response.flash="choose a team"
    teams=db(db.teams.id>0).select()
    return locals()
def show():
    i = db.teams(request.args(0,cast=int)) or redirect(URL('index'))
    p=db((db.tble.person==auth.user_id) & (db.tble.teams==i.id) ).count()
    if p is 0:
        db.tble.insert(person=auth.user_id,teams=i.id)
        session.var=1
    else:
        session.var=2
    redirect(URL('chooseteam'))
    return locals()
def myteams():
    p=db(db.teams.created_by==auth.user_id).select()
    if session.flag is 0:
        response.flash="min 5 members required"
    if session.flag is 1:
        if session.v is 1:
            response.flash="moderator choosen"
            session.v=0
        if session.v is 2:
            response.flash="already choosen"
            session.v=0
    return locals()
def details():
    i = db.teams(request.args(0,cast=int)) or redirect(URL('index'))
    session.req=i.id
    array=db(db.tble.teams==i.id).select()
    session.c=db(db.tble.teams==i.id).count()
    return locals()
def details1():
    i = db.tble(request.args(0,cast=int)) or redirect(URL('index'))
    if session.c>=5:
        m=db(db.teams.id==session.req).select()
        if m[0].moderator is None:
            db(db.teams.id==session.req).update(moderator=i.person)
            session.v=1
        else:
            session.v=2
        session.flag=1
    else:
        session.flag=0
    redirect(URL('myteams'))
    return locals()
def home():
    return locals()
def mail():
    i = db.teams(request.args(0,cast=int)) or redirect(URL('index'))
    pro=db(db.teams.id==i.id).select()
    ma=db(db.mail1.teams==i.id).select(orderby=~db.mail1.created_on)
    if (pro[0].moderator==auth.user_id):
        flag=1
    else:
        flag=0
    session.popo=i.id
    return locals()
def sendmail():
    i = db.teams(request.args(0,cast=int)) or redirect(URL('index'))
    form=SQLFORM(db.mail1)#.process()
    if form.process().accepted:
    	response.flash = "mail sent"
        my=db(db.mail1).select(orderby=~db.mail1.created_on)
        dhoni=db(db.teams.id==session.popo).select()
        if (dhoni[0].moderator==my[0].created_by):
            db(db.mail1.id==my[0].id).update(moderator=1,teams=session.popo)
        else:
            db(db.mail1.id==my[0].id).update(moderator=0,teams=session.popo)
    elif form.errors:
        response.flash = "pls check subject and body"
    return locals()
def teamin():
    q=db(db.tble.person==auth.user_id).select()
    return locals()
def mail2():
    i = db.tble(request.args(0,cast=int)) or redirect(URL('index'))
    pro=db(db.teams.id==i.teams).select()
    ma=db(db.mail1.teams==i.teams).select(orderby=~db.mail1.created_on)
    if (pro[0].moderator==auth.user_id):
        flag=1
    else:
        flag=0
    session.popo=i.teams
    return locals()
def memo():
    p=db(db.teams.moderator==auth.user_id).select()
    return locals()
def fullmail():
    i = db.mail1(request.args(0,cast=int)) or redirect(URL('index'))
    return locals()
def c_agenda():
    i = db.teams(request.args(0,cast=int)) or redirect(URL('index'))
    if(i.moderator!=auth.user_id):
        redirect(URL('index'))
    form=SQLFORM(db.agenda)#.process()
    if form.process().accepted:
    	response.flash = "agenda created"
        q=db(db.agenda.id>0).select(orderby=~db.agenda.created_on)
        db(db.agenda.id==q[0].id).update(teams=i.id)
    elif form.errors:
        response.flash = "Errors"
    else:
        response.flash = "Please fill the form"
    return locals()
def agenda():
    i = db.teams(request.args(0,cast=int)) or redirect(URL('index'))
    yuvi=db(db.agenda.teams==i.id).select()
    session.pastore=i.moderator
    return locals()
def full():
    i = db.agenda(request.args(0,cast=int)) or redirect(URL('index'))
    form=SQLFORM(db.topic)
    pandya=db(db.topic.agenda==i.id).select()
    session.pro=i.id
    if form.process().accepted:
    	response.flash = "topic added"
        q=db(db.topic.id>0).select(orderby=~db.topic.created_on)
        db(db.topic.id==q[0].id).update(agenda=i.id)
        redirect(URL('full',args=i.id))
    elif form.errors:
        response.flash = "Errors"
    return locals()
def topic():
    session.flow=1
    redirect((URL('full',args=session.pro)))
    return locals()
