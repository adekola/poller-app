""""
Models for the poller-app

this file contains models for : 
-    Response: to represent responses of users to a question raised by teh creator of the poll
-    Question: represents a question raised by the creator of a poll
"""

from google.appengine.ext import db

class Poller(db.Model):
  '''
  Class to represent the perosn who raises a question
  '''
  email = db.EmailProperty(required=True)
  password = db.StringProperty(required=True)
  fullname = db.StringProperty(required=True)

class Question(db.Model):
  '''
    A question created by the admin of the poll
    ...has the following fields: 
    - question_id : autogen id of the question..appengine will create this id automatically
    - date_posted: for the date the question was created by the poll admin
    - time_posted: for the time the question was created by the poll admin
    - reply_to: for the phone number users shld send their responses to i.e. teh long code
  '''
  reply_to = db.PhoneNumberProperty(required=True)
  date_posted  = db.DateProperty()
  time_posted = db.TimeProperty() 
  question = db.StringProperty()
  poller = db.ReferenceProperty(Poller, collection_name='questions')

class Response(db.Model):
  sender_phone = db.PhoneNumberProperty(required=True)
  question_id = db.ReferenceProperty(Question, collection_name='responses')
  response_body = db.StringProperty(required = True)
  time_sent = db.TimeProperty(auto_now = True)
  date_sent = db.DateProperty(auto_now = True)    
    

    
    #use the GAE Users API to auth pollers to the system. they'll be able to log in with their Google accounts to create questions and view responses 

