# Import web.py, the Microframework I am using, hashlib and time for hashing the 'tasks' and tinydb as database
import web
import hashlib
import time
from tinydb import TinyDB, Query, where

# Declarations for modules
db = TinyDB('db.json')
render = web.template.render('templates/', base='layout')

# Declare file structure of the application
urls = ("/", "index",
        "/add/", "addTask",
        "/delete/*", "deleteTask",
        "/move/*", "moveTask")

app = web.application(urls, globals())
# web.config.debug = True

# Gets called when site is first opened
class index:
    """Returns tasks from db"""
    def GET(self):
        section1 = db.search(where('section') == 1)
        section2 = db.search(where('section') == 2)
        section3 = db.search(where('section') == 3)
        return render.index(section1, section2, section3)

class addTask:
    form = web.form.Form(
            web.form.Textbox("title",  web.form.notnull, description="Title", class_="validate"),
            web.form.Textarea("description", web.form.notnull, description="Description" , class_="materialize-textarea"),
            web.form.Textbox("assignee", web.form.notnull, description="Assignee" , class_="validate"),
            web.form.Button("Add To-Do", class_="btn waves-effect waves-light")
            )

    def GET(self):
        f = self.form()
        return render.register(f)

    def POST(self):
        f= self.form()
        if not f.validates():
            return render.register(f)   # TODO: Return Error Message
        # sha1 is used, because it is fast and this is not security oriented
        
        hash = hashlib.sha1(f.d.title.encode('utf-8') +                         # Using the information here to make each UID unique
                            f.d.description.encode('utf-8') + 
                            f.d.assignee.encode('utf-8') + 
                            str(time.time()).encode('utf-8')                    # The hash is 100% unique, because Unix-Time gets factored in
                           ).hexdigest()
        # Save task to db
        db.insert({'title':f.d.title, 'description':f.d.description, 'assignee':f.d.assignee, 'hash':hash, 'section':1})
        raise web.seeother('/')

        
class deleteTask:
    def GET(self):
        url_args = web.input()
        
        # This requires every hash to be unique, that is not the case if two task with the same content 
        # created at exactly the same time. This is a small scale application, so that shouldn't be the case
        # If it is the case, then both entries get removed on deletion
        
        db.remove(where('hash') == url_args.hash)
        raise web.seeother('/')

class moveTask:
    form = web.form.Form(
            web.form.Dropdown('sectionSelect', [(1, 'TO-DO'), (2, 'WIP'), (3, 'Done')], description=None),
            web.form.Button('Move', class_="btn waves-effect waves-light")
            )

    def GET(self):
        f = self.form()
        return render.move(f)

    def POST(self):
        f = self.form()
        url_args = web.input()
        if not f.validates():
            return render.move(f)
        db.update({'section':int(f.d.sectionSelect)}, where('hash') == url_args.hash)
        raise web.seeother('/')

if __name__ == "__main__":
    app.run()
