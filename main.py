# coding: utf-8
import datetime
import os.path
import pyqrcode

from auth import GoogleCalendar
from draw_calendar import draw_month

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


EPD_WIDTH = 640
EPD_HEIGHT = 384
epd_enabled = False

if epd_enabled:
    from waveshare_epd import epd7in5bc
    epd = epd7in5bc.EPD()
    epd.init()
    epd.Clear()

b = GoogleCalendar()
if not b.is_authenticated:
    device = b.get_device_code()

    qr = pyqrcode.create(device['verification_url'])
    qr.png('qr.png', scale=5)
    qr_image = Image.open('qr.png')

    black_image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)
    red_image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)
    black_image.paste(qr_image, (int((EPD_WIDTH-qr_image.width)/2), 12))

    black_draw = ImageDraw.Draw(black_image)

    line_spacing = 6
    start = qr_image.height+line_spacing

    def draw_text(msg, size, top):
        if os.path.exists('/usr/share/fonts/truetype/ttf-bitstream-vera/Vera.ttf'):
            font = ImageFont.truetype('/usr/share/fonts/truetype/ttf-bitstream-vera/Vera.ttf', size)
        else:
            font = ImageFont.truetype('/Library/Fonts/Arial.ttf', size)

        w, h = black_draw.textsize(msg, font=font)
        black_draw.text(((EPD_WIDTH-w)/2, top), msg, font=font)
        return top + h + line_spacing

    msg = 'Scan the QR code or go to this url:'
    next_top = draw_text(msg, 12, start)

    msg = device['verification_url']
    next_top = draw_text(msg, 20, next_top)

    msg = 'Enter this code to give this device permission:'
    next_top = draw_text(msg, 12, next_top)

    msg = device['user_code']
    next_top = draw_text(msg, 20, next_top)

    if epd_enabled:
        epd.display(epd.getbuffer(black_image), epd.getbuffer(red_image))
    else:
        black_image.show()

    print("waiting for token")
    b.wait_fetch_token()

if b.is_authenticated:
    today = datetime.date.today()
    events = b.get_events(today.year, today.month)
    b, r = draw_month(today.year, today.month, events, today.day)
    if epd_enabled:
        epd.display(epd.getbuffer(b), epd.getbuffer(r))
    else:
        b = b.convert('RGBA')
        r = r.convert('RGBA')
        for y in range(r.size[1]):
            for x in range(r.size[0]):
                # Replace black by red
                if r.getpixel((x, y)) == (0, 0, 0, 255):
                    r.putpixel((x, y), (255, 0, 0, 255))
                # Replace white by transparent
                if r.getpixel((x, y)) == (255, 255, 255, 255):
                    r.putpixel((x, y), (0, 0, 0, 0))
        img = Image.alpha_composite(b, r)
        img.show()
