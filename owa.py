#!/usr/bin/env python

from gi.repository import Gtk, WebKit, Gdk, GdkPixbuf
from urlparse import urlparse
import simplejson as json
import os, sys, urllib2, argparse

class App:

	def __init__(self):
		parser = argparse.ArgumentParser(description="Open Web App Runner")
		parser.add_argument("url", help="URL for the App without protocol")
		parser.add_argument("murl", nargs="?", help="Relative route for the manifest file (usually something like '/appname.webapp')")
		parser.add_argument("--width", dest="width", default=900, help="Default window width")
		parser.add_argument("--height", dest="height", default=500, help="Default window width")
		parser.add_argument("--fullscreen", dest="fullscreen", action="store_true", help="Start fullscreened")
		parser.add_argument("--custom", dest="fullscreen", action="store_true", help="Set custom decoration")
		args = parser.parse_args()
		self.url = urlparse(args.url)
		if(self.url.scheme == ""):
			self.url = urlparse("http://" + args.url)
		self.murl = args.murl
		
		self.window = Gtk.Window()
		self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.window.set_default_size(int(args.width), int(args.height))
		self.window.set_resizable(True)
		if(args.fullscreen):
			self.window.fullscreen()

		self.view = WebKit.WebView()
		self.view.open(self.url.geturl())
	        self.viewsettings = self.view.get_settings()
		self.viewsettings.set_property('enable-default-context-menu', False)
		self.viewsettings.set_property('enable-file-access-from-file-uris', True)
		self.view.connect('title-changed', self.title_changed)
		
		if(self.murl):
			self.manifest = self.appLoad(self.murl)
			if(self.manifest):
				self.window.set_title(self.manifest["name"]+ " - " + self.manifest["description"])
				self.window.set_icon_list(self.iconsLoad())

		self.window.add(self.view)
		self.window.show_all()
		self.window.connect('destroy', lambda w: Gtk.main_quit())
	
	def appLoad(self, url):
		manifest = None
		try:
			response = urllib2.urlopen(self.url.scheme + "://" + self.url.netloc + self.murl)
			manifest = json.loads(response.read())
		except:
			print "MANIFEST COULD NOT BE LOADED (" + self.url.scheme + "://" + self.url.netloc + self.murl + ")"
		return manifest
		
	def iconsLoad(self):
		iconlist = [];
		for icon in self.manifest["icons"].values():
			content = None
			try:
				response = urllib2.urlopen(self.url.scheme + "://" + self.url.netloc + icon)
				content = response.read()
				fname='/tmp/owaicon.png'
        			with open(fname,'w') as f:
					f.write(content)
        			image = GdkPixbuf.Pixbuf.new_from_file(fname)
				iconlist.append(image)
			except:
				print "IMAGE COULD NOT BE LOADED (" + self.url.scheme + "://" + self.url.netloc + icon + ")"
		return iconlist
	
	def title_changed(self, widget, frame, title):
		self.window.set_title(title)
		
def main():
	app = App()
	Gtk.main()

if __name__ == "__main__":
	main()
