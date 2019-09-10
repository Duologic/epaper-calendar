# coding: utf-8
import time
import datetime
import calendar

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import pickle
import os.path
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

ROWS = 6
COLS = 7
EPD_WIDTH = 640
EPD_HEIGHT = 384
TOP_ROW = 12
BOX_WIDTH = EPD_WIDTH/COLS
BOX_HEIGHT = (EPD_HEIGHT/ROWS) - (TOP_ROW/ROWS)

image = Image.new('RGBA', (EPD_WIDTH, EPD_HEIGHT), 'white')
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('/Users/duologic/Library/Fonts/DejaVu Sans Mono Bold for Powerline.ttf', 12)

start = (0, TOP_ROW)
end = (EPD_WIDTH, TOP_ROW)
draw.line((start, end), 'black')

row = 1
while row<ROWS:
    start = (0, (row*BOX_HEIGHT)+TOP_ROW)
    end = (EPD_WIDTH, (row*BOX_HEIGHT)+TOP_ROW)
    draw.line((start, end), 'black')
    row += 1

col = 1
while col<COLS:
    start = (col*BOX_WIDTH, TOP_ROW)
    end = (col*BOX_WIDTH, EPD_HEIGHT)
    draw.line((start, end), 'black')
    col += 1

c = calendar.TextCalendar()
today = datetime.date.today()
count = 0
for day in c.itermonthdays(2019, 9):
    col = count - (COLS * (count // COLS))
    row = count // COLS
    if day>0:
        if day == today.day:
            draw.text((col*BOX_WIDTH+10, row*BOX_HEIGHT+10+TOP_ROW), '{}'.format(day), fill='red', font=font)
            draw.rectangle((col*BOX_WIDTH, row*BOX_HEIGHT+TOP_ROW, (col+1)*BOX_WIDTH, (row+1)*BOX_HEIGHT+TOP_ROW), outline='red')
        else:
            draw.text((col*BOX_WIDTH+10, row*BOX_HEIGHT+10+TOP_ROW), '{}'.format(day), fill='black', font=font)
    count += 1


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        while True:
            device = requests.post('https://accounts.google.com/o/oauth2/device/code',
                        params={'client_id': flow.client_config['client_id'],
                                'scope': SCOPES[0]},
                        headers={'Content-Type': 'application/x-www-form-urlencoded'})
            if device.status_code == 200:
                device = device.json()
                break
            else:
                time.sleep(2)

        print('Go to {} and enter {}'.format(device['verification_url'], device['user_code']))

        while True:
            try:
                flow.oauth2session._client.grant_type = 'http://oauth.net/grant_type/device/1.0'
                flow.fetch_token(code=device['device_code'])
                creds = flow.credentials
                break
            except:
                time.sleep(2)

    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

image.save('a.bmp')
