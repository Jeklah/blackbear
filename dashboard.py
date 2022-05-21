import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import regex as re
from dateutil import parser
import streamlit as st


rss = ['https://www.eveonline.com/rss/news',
       'https://newsfeed.eveonline.com/en-US/42/articles/page/1/20',
       'https://newsfeed.eveonline.com/en-US/43/articles/page/1/20',
       'https://newsfeed.eveonline.com/en-US/100/articles/page/1/20']


def date_time_parser(dt):
    return int(np.round((dt.now(dt.tz) - dt).total_seconds() / 60, 0))


def elapsed_time_str(mins):
    time_str = ''
    hours = int(mins / 60)
    days = np.round(mins / (60 * 24), 1)
    remaining_mins = int(mins - (hours * 60))

    if (days >= 1):
        time_str = f'{str(days)} days ago'
        if days == 1:
            time_str = 'a day ago'

    elif (days < 1) & (hours < 24) & (mins >= 60):
        time_str = f'{str(hours)} hours and {str(remaining_mins)} mins ago'
        if (hours == 1) & (remaining_mins > 1):
            time_str = f'an hour and {str(remaining_mins)} mins ago'
        if (hours == 1) & (remaining_mins == 1):
            time_str = 'an hour and a min ago'
        if (hours > 1) & (remaining_mins == 1):
            time_str = f'{str(hours)} hours and a min ago'
        if (hours > 1) & (remaining_mins == 0):
            time_str = f'{str(hours)} hours ago'
        if ((mins / 60) == 1) & (remaining_mins == 0):
            time_str = 'an hour ago'

    elif (days < 1) & (hours < 24) & (mins == 0):
        time_str = 'Just in'

    else:
        time_str = f'{str(mins)} minutes ago'
        if mins == 1:
            time_str = 'a minute ago'
    return time_str


def text_clean(desc):
    desc = desc.replace("&lt;", "<")
    desc = desc.replace("&gt;", ">")
    desc = desc.sub("<.*?>", "", desc)
    desc = desc.replace("#39;", "'")
    desc = desc.replace('&quot;', '"')
    desc = desc.replace('&nbsp;', '"')
    desc = desc.replace('#32;', ' ')
    return desc
