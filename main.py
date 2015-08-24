import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
from HTMLParser import HTMLParser
import jinja2
import os
import logging
import json
import urllib


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

class Thesis(ndb.Model):
    
    created_by = ndb.StringProperty(indexed=True)
    email = ndb.StringProperty(indexed=True)
    year = ndb.IntegerProperty(indexed=True)
    title = ndb.StringProperty(indexed=True)
    abstract = ndb.StringProperty(indexed=True)
    adviser = ndb.StringProperty(indexed=True)
    section = ndb.IntegerProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
  

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
       
        user = users.get_current_user()

        if user:

            url = users.create_logout_url(self.request.uri)
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            }
        
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))

        
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'LOG IN'
            status = 'Log in to your account'
            user = ' ' 

            template_values = {
                'user': user,
                'status': status,
                'url': url,
                'url_linktext': url_linktext,
            }
            
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render())
            
    def post(self):
       
        thesis = Thesis()
       
        thesis.created_by = users.get_current_user().user_id()
        thesis.email = users.get_current_user().email()
        thesis.year = int(self.request.get('year'))
        thesis.title = self.request.get('title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = int(self.request.get('section'))
        thesis.key = thesis.put()
        thesis.put()
        self.redirect('/')

class APIThesisHandler(webapp2.RequestHandler):
    def get(self):
        thesiss = Thesis.query().order(-Thesis.date).fetch()
        thesis_list = []

        for thesis in thesiss:
            thesis_list.append({
                'created_by': thesis.created_by,
                'email' : thesis.email,
                'id': thesis.key.id(),
                'year' : thesis.year,
                'title' : thesis.title,
                'abstract' : thesis.abstract,
                'adviser' : thesis.adviser,
                'section' : thesis.section
                });
            
        response = {
             'result' : 'OK',
             'data' : thesis_list
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        thesis = Thesis()
       
        thesis.created_by = users.get_current_user().user_id()
        thesis.email = users.get_current_user().email()
        thesis.year = int(self.request.get('year'))
        thesis.title = self.request.get('title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = int(self.request.get('section'))
        thesis.key = thesis.put()
        thesis.put()

        self.response.headers['Content-Type'] = 'application/json'
        response = {
        'result' : 'OK',
        'data':{
                'created_by': thesis.created_by,
                'email' : thesis.email,              
                'id': thesis.key.id(),
                'year' : thesis.year,
                'title' : thesis.title,
                'abstract' : thesis.abstract,
                'adviser' : thesis.adviser,
                'section' : thesis.section
        }
        }
        self.response.out.write(json.dumps(response))

class DeleteEntry(webapp2.RequestHandler):
    def get(self, thesis_id):
        thesis = Thesis.get_by_id(int(thesis_id))
        thesis.key.delete()
        self.redirect('/')

class EditEntry(webapp2.RequestHandler):
    def get(self, thesis_id):
        thesis = Thesis.get_by_id(int(thesis_id))
        template_data = {
            'thesis': thesis
        }
        user = users.get_current_user()

        if user:

            url = users.create_logout_url(self.request.uri)
            url_linktext = 'LOG OUT'
            status = 'Hello, '
            template_values = {
            'user': user,
            'status': status,
            'url': url,
            'url_linktext': url_linktext,
            }
        
        template = JINJA_ENVIRONMENT.get_template('login.html')
        self.response.write(template.render(template_values))
        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_data))

    def post(self, thesis_id):
        
        thesis = Thesis.get_by_id(int(thesis_id))
        thesis.created_by = users.get_current_user().user_id()
        thesis.email = users.get_current_user().email()
        thesis.year = int(self.request.get('year'))
        thesis.title = self.request.get('title')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.section = int(self.request.get('section'))
        thesis.put()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/edit_thesis/(.*)', EditEntry),
    ('/delete_thesis/(.*)', DeleteEntry),
    ('/api/thesis', APIThesisHandler),
    ('/', MainPageHandler)
], debug=True)