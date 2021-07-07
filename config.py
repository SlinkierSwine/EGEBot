import os
import logging
from dotenv import load_dotenv

from data.parse_json_texts import parse

load_dotenv()
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )

BASEDIR = os.path.abspath(os.path.dirname(__file__))
API_TOKEN = os.getenv('API_TOKEN')
DATABASE_PATH = os.path.join(BASEDIR, 'data', 'db', 'db.db')

MENU_TEXTS = parse(os.path.join(BASEDIR, 'data', 'texts.json'))
if MENU_TEXTS:
    REVIEWS_TEXT = MENU_TEXTS['menu']['reviews']['text']
    REVIEWS_PARSE_MODE = MENU_TEXTS['menu']['reviews']['parse_mode']

    FAQ_TEXT = MENU_TEXTS['menu']['faq']['text']
    FAQ_PARSE_MODE = MENU_TEXTS['menu']['faq']['parse_mode']

    VACANCIES_TEXT = MENU_TEXTS['menu']['vacancies']['text']
    VACANCIES_PARSE_MODE = MENU_TEXTS['menu']['vacancies']['parse_mode']
else:
    REVIEWS_TEXT = FAQ_TEXT = VACANCIES_TEXT = ''
    REVIEWS_PARSE_MODE = FAQ_PARSE_MODE = VACANCIES_PARSE_MODE = None

ADMINS = map(int, os.getenv('ADMINS').split(';'))
