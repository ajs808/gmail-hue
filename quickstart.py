from __future__ import print_function
import pickle
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from phue import Bridge
import config

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
b = Bridge(config.ip)
lights = b.get_light_objects('id')

def blinkRed():
    
    light = lights[3] #the light in my room
    light.transitiontime = 5

    oPower = light.on
    oBrightness = light.brightness
    oHue = light.hue
    oSaturation = light.saturation
    for i in range(0,3):
        light.on = True
        light.brightness = 254
        light.hue = 11
        light.saturation = 100

        time.sleep(0.5)

        light.on = oPower
        light.brightness = oBrightness
        light.hue = oHue
        light.saturation = oSaturation


def main():
    #refresh rate
    PERIOD = 60
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    while True:
        timeSinceEpoch = str(int(time.time()) - PERIOD -10)
        result = service.users().messages().list(userId='me', q='is:unread after:' + timeSinceEpoch).execute()
        messages = result.get('messages') 

        if not messages:
            print("No new messages")
        else:
            print("New messages found")
            blinkRed()
        time.sleep(PERIOD)

if __name__ == '__main__':
    main()
