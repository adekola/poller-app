import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from util.sessions import Session
from model import Poller
from google.appengine.ext import db



class index(webapp.RequestHandler):
    
    def get(self):
        #check for sessions here to det which template to render
        
       data = {}
       #check if there's a username entry in the session
       self.session = Session()
    
       data['user'] =  self.session.get('username', None)
       data['noinfo'] = False
      
       render(self, "index.html", data)
       
    def post(self):
        data={}
        render(self, "index.html", data)
        
class editprofile(webapp.RequestHandler):
    
    def get(self):
        #check for sessions here to det which template to render
        
       data = {}
       #check if there's a username entry in the session
       self.session = Session()
    
       data['user'] =  self.session.get('username', None)
       user  = self.session.get('username', None)
       if user:
           que = db.Query(Poller)
           que.filter('email', user)
           res  = que.fetch(limit=1)
           current_user = res[0]
           data['email'] = current_user.email
           data['fullname'] = current_user.fullname
           data['password'] = current_user.password
           
           render(self,"profile.html",data)
        
       else:
            render(self, "index.html",data)
       
    def post(self):
        data={}
        em = self.request.get('em') 
        pw = self.request.get('pw')
        pwa = self.request.get('pwa')
        fn = self.request.get('fn')
        
        if pw == pwa:
            que = db.Query(Poller)
            que.filter('email',em)
            res = que.fetch(limit=1)
            
            poller = res[0] #get the first (and only)  dude in the match
            poller.fullname = fn
            poller.password = pw
            poller.put()
            data['updatesuccess'] = True
            render(self,"profile.html",data)
        else:
            data['pwmismatch'] = True
            data['error_msg'] = "The passwords you are trying to change do not match"
            render(self,"profile.html", data)
        
class createQuestion(webapp.RequestHandler):
    
    def get(self):
       data = {}
       #check if there's a username entry in the session
       self.session = Session()
    
       data['user'] =  self.session.get('username', None)
       render(self, "create_question.html",data)

    def post(self):
        self.response.out.write()
        
class getResponses(webapp.RequestHandler):
    
    def get(self):
       data = {}
       #check if there's a username entry in the session
       self.session = Session()
    
       data['user'] =  self.session.get('username', None)
       render(self, "view_responses.html",data)

    def post(self):
        #get input from the forms, using the name = value from the input fields
        self.request.headers
        
        
class about(webapp.RequestHandler):
    def get(self):
        
       data = {}
       #check if there's a username entry in the session
       self.session = Session()
    
       data['user'] =  self.session.get('username', None)
       
       render(self,"about.html",data)  
        
        

    
class login(webapp.RequestHandler):
    def get(self):
        render(self, "login.html")
        
    def post(self):
        data = {}
        em = self.request.get('em')
        pw = self.request.get('pw')
    
        self.session = Session()
        #destroy former session data
        self.session.delete_item('username')
       
        
        if em =="" and pw == "":
            data['noCredos']  = True
            #self.session = Session()
            #data['user'] =  self.session.get('username', None)
            data['error_msg'] = "pls fill in your email and password"
            render(self,"login.html",data) 
        
        else:
            que = db.Query(Poller)
            que.filter('email', em)
            que.filter('password', pw)
        
            results = que.fetch(limit=1)
        
            if len(results) > 0:
                self.session['username'] = em #set session
                data['user'] = em
                render(self,"create_question.html",data)
            else:
                data['usernotfound'] = True
                data['error_msg'] = "incorrect password or email; pls try again"
                render(self,"login.html",data)
         
        
class logout(webapp.RequestHandler):
    def get(self):
        self.session = Session()
        self.session.delete_item('username')
        render(self,"logout.html")
        
    def post(self):
        render()

        
class register(webapp.RequestHandler):
    def get(self):
        data = {}
        data['user']  = None
        data['noinfo'] = False
        render(self, "index.html", data)
        
    def post(self):
        data = {}
        em = self.request.get('em') 
        pw = self.request.get('pw')
        pwa = self.request.get('pwa')
        fn = self.request.get('fn')
        
        if em == '' or pw == '' or pwa == '' or fn == '':
            data['noinfo']  =True
            data['error_msg'] = "all fields must be supplied for registration"
            render(self,"index.html", data)
         
        else:
            #check if user already exists
            que =  db.Query(Poller)
            que.filter('email', em)
            results = que.fetch(limit=1)
        
            if len(results) > 0:
                data['userexists'] = True
                data['error_msg'] = "An account with that email already exists"
                render(self, "index.html", data)
            
        
            else:
                if pw == pwa:
                    poller = Poller(email= em, password = pw, fullname=fn)
                    poller.put()
                    self.session = Session()
                    self.session['username'] = em
                    data['user'] = em
                    render(self,"create_question.html",data)
                else:
                    data['pwmismatch'] = True
                    data['error_msg'] = "The passwords you entered do not match"
                    render(self,"index.html", data)


def render(handler, template_file = "base.html", data = {}):
    temp = os.path.join(
    os.path.dirname(__file__),
    'templates/' + template_file)
    if not os.path.isfile(temp):
      return False

  # Make a copy of the dictionary and add the path and session
    newval = dict(data)
    newval['path'] = handler.request.path
    handler.session = Session()
    if 'username' in handler.session:
      newval['username'] = handler.session['username']

#love this part
    outStr = template.render(temp, newval)
    handler.response.out.write(outStr)
    return True
    


def main():
  application = webapp.WSGIApplication([('/',index), ('/createquestion', createQuestion),
                                       ('/getresponses', getResponses),('/logout', logout), 
                                       ('/editprofile', editprofile), ('/index',index), ('/login', login), ('/about', about), ('/register', register)], debug=True)
  wsgiref.handlers.CGIHandler().run(application)
  
if __name__ == "__main__":
  main()
