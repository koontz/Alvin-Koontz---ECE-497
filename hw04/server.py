#!/usr/bin/env python
import web 
from static import view
from static import config
from static.view import render

urls = (
	'/', 'index'
)

class index:
	def GET(self):
		return render.base()

if __name__ == "__main__":
	app=web.application(urls,globals())
	app.internalerror = web.debugerror
	app.run()
