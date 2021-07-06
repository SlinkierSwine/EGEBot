import os
import logging
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )

BASEDIR = os.path.abspath(os.path.dirname(__file__))
API_TOKEN = os.getenv('API_TOKEN')
DATABASE_PATH = os.path.join(BASEDIR, 'data', 'db', 'db.db')

