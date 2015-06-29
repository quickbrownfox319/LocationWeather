import urllib2
import json
import yaml

#get key from file
with open('wundergroundkey.yml', 'r') as txt:
	key = yaml.load(txt)

key = key['wunderground']
zip_code = raw_input("Zip code: ")

f = urllib2.urlopen(
	'http://api.wunderground.com/api/%s/geolookup/forecast/conditions/q/%s.json' % (key,zip_code))
json_string = f.read()
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']

#next day's forecast
forecast_prefix = parsed_json['forecast']['txt_forecast']['forecastday'][2]
day = forecast_prefix['title']
forecast = forecast_prefix['fcttext']

print ("The weather in {} on {} will be: \n{}".format(location, day, forecast))
f.close()