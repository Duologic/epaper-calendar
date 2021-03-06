# coding: utf-8
import os.path
import calendar

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

EPD_WIDTH = 640
EPD_HEIGHT = 384


def draw_month(year, month, events, select):
    weekdays = []
    for day in calendar.weekheader(10).split(' '):
        if day.strip():
            weekdays.append(day.strip())

    ROWS = 5
    COLS = len(weekdays)
    FONT_SIZE = 10
    LINES = 2
    TOP_ROW = FONT_SIZE*LINES + 2*LINES
    BOX_WIDTH = EPD_WIDTH/COLS
    BOX_HEIGHT = (EPD_HEIGHT/ROWS) - (TOP_ROW/ROWS)

    if os.path.exists('/usr/share/fonts/TTF/Vera.ttf'):
        font = ImageFont.truetype('/usr/share/fonts/TTF/VeraBd.ttf', FONT_SIZE)
    else:
        font = ImageFont.truetype('/Library/Fonts/Arial.ttf', FONT_SIZE)

    black_image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)
    black_draw = ImageDraw.Draw(black_image)

    red_image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)
    red_draw = ImageDraw.Draw(red_image)

    line = 0
    w, h = black_draw.textsize('{} {} '.format(calendar.month_name[month], year), font=font)
    start = ((EPD_WIDTH-w)/2, FONT_SIZE*line)
    red_draw.text(start, '{} {} '.format(calendar.month_name[month], year), font=font)

    line = 1
    col = 0
    for day in weekdays:
        start = (col*BOX_WIDTH+2, FONT_SIZE*line)
        black_draw.text(start, '{} '.format(day), font=font)
        col += 1

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
    count = 0
    text_padding = 2
    for day in c.itermonthdays(year, month):
        col = count - (COLS * (count // COLS))
        row = count // COLS
        if day > 0:
            black_draw.text((col*BOX_WIDTH+text_padding,
                             row*BOX_HEIGHT+text_padding+TOP_ROW),
                            '{}'.format(day), font=font)

            if day == select:
                red_draw.text((col*BOX_WIDTH+text_padding,
                               row*BOX_HEIGHT+text_padding+TOP_ROW),
                              '{}'.format(day),
                              font=font)
                red_draw.rectangle((col*BOX_WIDTH,
                                    row*BOX_HEIGHT+TOP_ROW,
                                    (col+1)*BOX_WIDTH,
                                    (row+1)*BOX_HEIGHT+TOP_ROW))

            if day in events:
                line = 1
                for event in events[day]:
                    if day == select:
                        red_draw.text((col*BOX_WIDTH+text_padding,
                                       row*BOX_HEIGHT+text_padding+TOP_ROW+font.size*line),
                                      '{} '.format(event[1][0:16]), font=font)
                    else:
                        black_draw.text((col*BOX_WIDTH+text_padding,
                                         row*BOX_HEIGHT+text_padding+TOP_ROW+font.size*line),
                                        '{} '.format(event[1][0:16]), font=font)
                    line += 1
                    if line == 4:
                        if day == select:
                            red_draw.text((col*BOX_WIDTH+text_padding,
                                           row*BOX_HEIGHT+text_padding+TOP_ROW+font.size*line),
                                          'more...', font=font)
                        else:
                            black_draw.text((col*BOX_WIDTH+text_padding,
                                             row*BOX_HEIGHT+text_padding+TOP_ROW+font.size*line),
                                            'more...', font=font)
                        break

        count += 1

    return black_image, red_image
