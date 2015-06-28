import urllib2
import json
import yaml

with open('wundergroundkey.yml', 'r') as txt:
	key = yaml.load(txt)

key = 'http://api.wunderground.com/api/'+ key['wunderground']

print key

f = urllib2.urlopen(key + '/geolookup/conditions/q/IA/Cedar_Rapids.json')
json_string = f.read()
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_f = parsed_json['current_observation']['temp_f']
print "Current temperature in %s is: %s" % (location, temp_f)
f.close()