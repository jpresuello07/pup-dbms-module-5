import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json

from google.appengine.api import users


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class useraccount(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    first_name = ndb.StringProperty(indexed=True)
    last_name = ndb.StringProperty(indexed=True)
    phone_number = ndb.StringProperty(indexed=True)
    created_date = ndb.DateTimeProperty(auto_now_add=True)

class createthesis(ndb.Model):
    year = ndb.StringProperty(indexed=True)
    title1 = ndb.StringProperty(indexed=True)
    abstract = ndb.StringProperty(indexed=True)
    adviser = ndb.StringProperty(indexed=True)
    section = ndb.StringProperty(indexed=True)
    author = ndb.KeyProperty(kind = 'useraccount',indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        loggedin_user = users.get_current_user()

        if loggedin_user:
            user_key=ndb.Key('useraccount',loggedin_user.user_id())
            user=user_key.get()
            if user:
                logout_url = users.create_logout_url('/login')
                template = JINJA_ENVIRONMENT.get_template('main.html')
                template_values = {
                	'logout_url':logout_url
                }
                self.response.write(template.render(template_values))
            else:
                template = JINJA_ENVIRONMENT.get_template('reg_form.html')
                self.response.write(template.render())
        else:
            login_url = users.create_login_url('/home')
            template = JINJA_ENVIRONMENT.get_template('login.html')
            template_values = {
            	'login_url':login_url
            }
            self.response.write(template.render(template_values))

class ThesisHandler(webapp2.RequestHandler):
    def get(self):  
        thesis1 = createthesis.query().order(-createthesis.date)
        thesis_list = []

        for t in thesis1:
            user = useraccount.query(useraccount.key == t.author)
            author_name=[]
            for u in user:
                author_name.append({
                    'first_name': u.first_name,
                    'last_name': u.last_name
                    })
            thesis_list.append({
                'year': t.year,
                'title1': t.title1,
                'abstract': t.abstract,
                'adviser': t.adviser,
                'section': t.section,
                'author': author_name,
                })

        response = {
            'result': 'OK',
            'data': thesis_list
        }                           
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        thesis1 = createthesis()

        user_key=ndb.Key('useraccount',users.get_current_user().user_id())

        thesis1.author = user_key
        thesis1.year = self.request.get('year')
        thesis1.title1 = self.request.get('title1')
        thesis1.abstract = self.request.get('abstract')
        thesis1.adviser = self.request.get('adviser')
        thesis1.section = self.request.get('section')
        thesis1.put()

        self.response.headers['Content-Type'] = 'application/json'
        response = {
        'result': 'OK',
        'data': {
            'id': thesis1.key.urlsafe(),
            'year': thesis1.year,
            'title1': thesis1.title1,
            'abstract': thesis1.abstract,
            'adviser': thesis1.adviser,
            'section': thesis1.section,
            'author':user_key.get().first_name + '  ' + user_key.get().last_name
            }
        }
        self.response.out.write(json.dumps(response))

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        login_url = users.create_login_url('/home')
        template = JINJA_ENVIRONMENT.get_template('login.html')
        template_values = {
        	'login_url':login_url
        }

        self.response.write(template.render(template_values))

class RegistrationHandler(webapp2.RequestHandler):
    def get(self):
        loggedin_user = users.get_current_user()

        if loggedin_user:
            user_key=ndb.Key('useraccount',loggedin_user.user_id())
            user=user_key.get()
            if user:
                self.redirect('/home')
            else:
                template = JINJA_ENVIRONMENT.get_template('reg_form.html')
                self.response.write(template.render())
        else:
            self.redirect(users.create_login_url('/register'))

    def post(self):
        loggedin_user = users.get_current_user()
        user1 = useraccount(id=loggedin_user.user_id())

        user1.email = loggedin_user.email()
        user1.first_name = self.request.get('first_name')
        user1.last_name=self.request.get('last_name')
        user1.phone_number=self.request.get('phone_number')
        user1.put()

        self.response.headers['Content-Type'] = 'application/json'
        response = {
        'result': 'OK',
        'data': {
            'email': user1.email,
            'first_name': user1.first_name,
            'last_name': user1.last_name,
            'phone_number': user1.phone_number,
            }
        }
        self.response.out.write(json.dumps(response))

        self.redirect('/home')

app = webapp2.WSGIApplication([
    ('/api/thesis', ThesisHandler),
    ('/login', LoginHandler),
    ('/home', MainPageHandler),
    ('/register',RegistrationHandler),
    ('/', MainPageHandler)
], debug=True)