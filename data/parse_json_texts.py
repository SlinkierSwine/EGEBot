import json
import logging

from aiogram.types import ParseMode


def parse(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            d = json.load(f)
        for i in d['menu'].keys():
            if d['menu'][i]['parse_mode'] and d['menu'][i]['parse_mode'].lower == 'markdown':
                d['menu'][i]['parse_mode'] = ParseMode.MARKDOWN
            elif d['menu'][i]['parse_mode'] and d['menu'][i]['parse_mode'].lower == 'html':
                d['menu'][i]['parse_mode'] = ParseMode.HTML
        return d
    except Exception as e:
        logging.error(e)
        return None
