import web
import hashlib
from tinydb import TinyDB, Query, where

db = TinyDB('db.json')
render = web.template.render('templates/')

urls = ("/", "index",
        "/add/", "addTask",
        "/delete/*", "deleteTask",
        "/move/*", "moveTask")

app = web.application(urls, globals())

class index:
    def GET(self):
        section1 = db.search(where('section') == 1)
        section2 = db.search(where('section') == 2)
        section3 = db.search(where('section') == 3)
        return render.index(section1, section2, section3)

class addTask:
    form = web.form.Form(
            web.form.Textbox("title",  web.form.notnull, description="I need to..."),
            web.form.Textarea("description", web.form.notnull, description="Description"),
            web.form.Textbox("assignee", web.form.notnull, description="Person"),
            web.form.Button("Add To-Do")
            )
    def GET(self):
        f = self.form()
        return render.register(f)
    def POST(self):
        f= self.form()
        if not f.validates():
            return render.register(f)
        hash = hashlib.sha1(f.d.title.encode('utf-8') + f.d.description.encode('utf-8')).hexdigest()
        db.insert({'title':f.d.title, 'description':f.d.description, 'assignee':f.d.assignee, 'hash':hash, 'section':1})
        raise web.seeother('/')

class deleteTask:
    def GET(self):
        url_args = web.input()
        for i in db.all():
                print("Hash given from URL: " + url_args.hash + " Hash produced: " + i.get('hash') + " are matching")
                db.remove(where('hash') == url_args.hash)
                raise web.seeother('/')
        print("Has not found hash: " + url_args.hash)
        raise web.seeother('/')

class moveTask:
    form = web.form.Form(
            web.form.Dropdown('sectionSelect', [(1, 'Section 1'), (2, 'Section 2'), (3, 'Section 3')]),
            web.form.Button('Move')
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
