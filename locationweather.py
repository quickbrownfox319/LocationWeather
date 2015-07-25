import httplib2
import os
import urllib2
import json
import yaml
import re

import requests

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

#Google calendar API auth
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.yml'
APPLICATION_NAME = 'Google Calendar API Quickstart'

###
#Google Calendar API oauth2
def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials


###
#wunderground API
def get_weather(zip_code):

    with open('api_keys.yml', 'r') as txt:
        key = yaml.load(txt)

    key = key['wunderground']

    f = urllib2.urlopen(
        'http://api.wunderground.com/api/%s/geolookup/forecast/conditions/q/%s.json' % (key,zip_code))
    json_string = f.read()
    parsed_json = json.loads(json_string)
    location = parsed_json['location']['city']

    #next day's forecast
    forecast_prefix = parsed_json['forecast']['txt_forecast']['forecastday'][2]
    day = forecast_prefix['title']
    forecast = forecast_prefix['fcttext']

    forecast_msg = ("The weather in {} on {} will be: \n{}".format(location, day, forecast))
    f.close()
    return forecast_msg

###
#pushbullet api
def push(title, msg):
    with open('api_keys.yml', 'r') as txt:
        key = yaml.load(txt)

    key = key['pushbullet']

    try:
        url = 'https://api.pushbullet.com/v2/pushes'
        headers = {'Authorization': 'Bearer {}'.format(key), 'Content-Type': 'application/json'}
        payload = {'type':'note', 'title':title, 'body':msg}
        r = requests.post(url, data=json.dumps(payload), headers=headers)

        #push event and weather via pushbullet
        #push = pb.push_note(title, msg)

    except Exception, detail:
        print "Error, ", detail, "\n"


def main():
    """
    Retrieve today's event's weather using Google Calendar API and Wunderground API
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    #get today's date & time
    now = datetime.datetime.today()
    tomorrow = now + datetime.timedelta(days=7)
    print "Upcoming Events \n"

    #set event search for today and tomorrow
    # 'Z' indicates UTC time
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now.isoformat() + 'Z', 
        timeMax=tomorrow.isoformat() + 'Z', maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print 'No upcoming events found.\n'
    for event in events:

        #try and pull zip code, else default zip code
        try:
            location = event['location']
            print "Location: ", location

            #regex interpretation: zero or more instances of 5 consecutive numbers for
            #first half of zip code, and '-' and 4 more consecutive digits for second half of zip
            #one or more times
            zip_code = re.search(r'.*(\d{5}(\-\d{4})?)', location)
            zip_code = zip_code.groups()[0]

        except (KeyError, AttributeError):
            print "Site has no location, but here's NJ's weather\n"
            zip_code = "08807" #default zip

        start_time = event['start'].get('dateTime', event['start'].get('date'))
        forecast = get_weather(zip_code)
        event = event['summary']

        #debug
        print "start_time: " + start_time
        print "event: " + event
        print "forecast: " + forecast

        #push with pushbullet!
        push("Weather at: " + event, forecast)


if __name__ == '__main__':
    main()