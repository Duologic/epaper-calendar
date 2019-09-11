# coding: utf-8
import datetime
import calendar

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

EPD_WIDTH = 640
EPD_HEIGHT = 384


def draw_month():
    ROWS = 6
    COLS = 7
    TOP_ROW = 12
    BOX_WIDTH = EPD_WIDTH/COLS
    BOX_HEIGHT = (EPD_HEIGHT/ROWS) - (TOP_ROW/ROWS)

    font = ImageFont.truetype('/Users/duologic/Library/Fonts/DejaVu Sans Mono Bold for Powerline.ttf', 12)

    black_image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)
    black_draw = ImageDraw.Draw(black_image)

    red_image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)
    red_draw = ImageDraw.Draw(red_image)

    start = (0, TOP_ROW)
    end = (EPD_WIDTH, TOP_ROW)
    black_draw.line((start, end))

    row = 1
    while row < ROWS:
        start = (0, (row*BOX_HEIGHT)+TOP_ROW)
        end = (EPD_WIDTH, (row*BOX_HEIGHT)+TOP_ROW)
        black_draw.line((start, end))
        row += 1

    col = 1
    while col < COLS:
        start = (col*BOX_WIDTH, TOP_ROW)
        end = (col*BOX_WIDTH, EPD_HEIGHT)
        black_draw.line((start, end))
        col += 1

    c = calendar.TextCalendar()
    today = datetime.date.today()
    count = 0
    for day in c.itermonthdays(2019, 9):
        col = count - (COLS * (count // COLS))
        row = count // COLS
        if day > 0:
            black_draw.text((col*BOX_WIDTH+10, row*BOX_HEIGHT+10+TOP_ROW), '{}'.format(day), font=font)

            if day == today.day:
                red_draw.text((col*BOX_WIDTH+10,
                               row*BOX_HEIGHT+10+TOP_ROW),
                              '{}'.format(day),
                              font=font)
                red_draw.rectangle((col*BOX_WIDTH,
                                    row*BOX_HEIGHT+TOP_ROW,
                                    (col+1)*BOX_WIDTH,
                                    (row+1)*BOX_HEIGHT+TOP_ROW))
        count += 1

    return black_image, red_image
