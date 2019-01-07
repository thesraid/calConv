#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
thesraid@gmail.com
https://bottlepy.org/docs/dev/tutorial.html
"""
import os
import calConv
from bottle import run, template, get, post, request # or route

@get('/upload') 
def login():
    return '''
        <form action="/upload" method="post" enctype="multipart/form-data">
            File: <input name="upload" type="file" />
            <input value="Upload" type="submit" />
        </form>
    '''

@post('/upload') # or @route('/login', method='POST')
def do_upload():
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.ics'):
        return "File extension not allowed."
    save_path = "/tmp/"
   
    file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    upload.save(file_path)

    calConv.main(save_path + "/" + upload.filename, "/var/www/html/beards/cal/cal.csv")   

    return '''<a href = "http://bleedingeardrums.com/cal/cal.csv">Download CSV</a>'''

run(host='bleedingeardrums.com', port=8080, debug=True)

