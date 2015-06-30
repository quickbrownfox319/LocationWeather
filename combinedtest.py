import httplib2
import os
import urllib2
import json
import yaml

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

###
#Google Calendar API

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.yml'
APPLICATION_NAME = 'Google Calendar API Quickstart'


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
def get_weather(loc):
    with open('wundergroundkey.yml', 'r') as txt:
        key = yaml.load(txt)

    key = key['wunderground']
    zip_code = raw_input(loc)

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

#get zip code from location if there is one
#def getzip():


def main():
    """
    Retrieve today's event's weather using Google Calendar API and Wunderground API
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    #get today's date & time
    now = datetime.datetime.today()
    tomorrow = now + datetime.timedelta(days=2)
    print "Today's and tomorrow's events"

    #set event search for today and tomorrow
    # 'Z' indicates UTC time
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now.isoformat() + 'Z', 
        timeMax=tomorrow.isoformat() + 'Z', maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print 'No upcoming events found.'
    for event in events:

        try:
            location = event['location']
            #need to parse location for zip, maybe using regex
            #get_weather(location)
        except KeyError:
            print "Site has no location, but here's NJ's weather"
            location = "08807" #default zip

        start = event['start'].get('dateTime', event['start'].get('date'))
        print start
        print event['summary']
        print location + "\n"


if __name__ == '__main__':
    main()