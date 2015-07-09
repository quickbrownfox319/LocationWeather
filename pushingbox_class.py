#pushingbox class
#credit to GuigiAbloc
#http://blog.guiguiabloc.fr/index.php/2012/02/22/pushingbox-vos-notifications-in-the-cloud/

import urllib, urllib2
class pushingbox():
	url = ""
	def __init__(self, key):
		url = 'http://api.pushingbox.com/pushingbox'
		values = {'devid' : key}
		try:
			data = urllib.urlencode(values)
			print data
			req = urllib2.Request(url, data)
			print req
			#400 error with urllib2.urlopen...somewhere...
			sendrequest = urllib2.urlopen(req)
			print sendrequest
		except Exception, detail:
			print "Error, ", detail, "\n"