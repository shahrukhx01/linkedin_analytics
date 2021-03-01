import logging
import yaml
from exceptions.exception import InvalidConfigurationException
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch as es
import json


def read_config(config_path):
    if not config_path:
        config_path = 'config/scraper_config.yaml'

    with open(r'{}'.format(config_path)) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        scraper_config = yaml.load(file, Loader=yaml.FullLoader)
    
    return scraper_config

def get_logger():
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(name='LinkedIn Jobs Scraper')

def write_to_file(data, file_path):
    with open(file_path,'a+') as f:
        f.write('{}\n'.format(data))

def read_from_file(file_path):
    with open(file_path,'r') as f:
        return [job_id.rstrip('\n') for job_id in f.readlines()] ## preprocess job_ids


def rel_time_to_absolute_datetime(relative_time_str):
    N = int(relative_time_str.split(' ')[0])
    date_n_days_ago = None
    if 'day' in relative_time_str:
        date_n_days_ago = datetime.now() - timedelta(days=N)
    elif 'week' in relative_time_str:
        date_n_days_ago = datetime.now() - timedelta(weeks=N)
    elif 'month' in relative_time_str:
        date_n_days_ago = datetime.now() - timedelta(months=N)

    return str(date_n_days_ago).split(' ')[0]

def write_to_es(index_name, data):
   es.index(index=index_name, id=data['job_id'],     body=json.loads(data))

