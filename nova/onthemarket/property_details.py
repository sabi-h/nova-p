import base64
import csv
import json
import logging
import os
from random import random
import sys
import time

from datetime import datetime
from pprint import pprint
from typing import Generator

import pandas as pd
import requests

from definitions import ROOT_DIR
from origins.utils import (
	get_filepath,
	get_outward_codes,
	get_url,
	process_df_columns,
	get_files
)
from origins.onthemarket.schema import schema


# ================================================================================
# 									To Do
# ================================================================================

"""				Complete extract_data_from_html function
"""
# ================================================================================



# ================================================================================
# 									Logging
# ================================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s:')

file_handler = logging.FileHandler(os.path.join(ROOT_DIR, 'logs/onthemarket_property_details.log'))
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
# ================================================================================


yyyymm = datetime.now().strftime('%Y%m')

BASE_URL = 'https://www.onthemarket.com/'

DIR_PATH_RAW = os.path.join(ROOT_DIR, f'data/onthemarket/property_details/raw/{yyyymm}')
DIR_PATH_PROCESSED = os.path.join(ROOT_DIR, f'data/onthemarket/property_details/processed/{yyyymm}')
DIR_PATH_AGGREGATED = os.path.join(ROOT_DIR, f'data/onthemarket/property_details/aggregated/')

# Create directories if they do not exist
for _dir in [DIR_PATH_RAW, DIR_PATH_PROCESSED, DIR_PATH_AGGREGATED]:
	if not os.path.exists(_dir):
		os.makedirs(_dir)


def _save_file(data, fp):
	"""
	Saves response from request to filepath.
	"""
	with open(fp, 'wb') as f:
		f.write(data)


def _get_urls(filename):
	fp = os.path.join(ROOT_DIR, f'data/onthemarket/property_tiles/aggregated/{filename}.csv')
	url_suffixes = pd.read_csv(fp, usecols=['property-link'])['property-link'].to_list()
	for url_suffix in url_suffixes:
		yield BASE_URL.strip('/') + '/' + url_suffix.strip('/')


def _send_request(url):
	payload = {}
	headers = {
		'authority': 'www.onthemarket.com',
		'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
		'accept': 'application/json',
		'sec-ch-ua-mobile': '?0',
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
		'content-type': 'application/json; charset=utf-8',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'cors',
		'sec-fetch-dest': 'empty',
		'referer': 'https://www.onthemarket.com/new-homes/property/london/?view=grid',
		'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
	}
	return requests.request('GET', url, headers=headers, data=payload)


def scrape_property_details(force=False):
	"""
	Parameters
	----------
		force : bool, default False
			If you want to override files then set it to True

	"""
	urls = _get_urls(yyyymm)
	for url in urls:
		logger.info(f'url: -> {url}')

		# Create filepath and check if it exists
		filename = url.rsplit('/', 1)[-1] + '.html'
		dst_fp = os.path.join(DIR_PATH_RAW, filename)

		if os.path.exists(dst_fp):
			logger.info(f'file exists -> {dst_fp}')

			if force == False:
				continue
			else:
				logger.info(f'overriding existing file -> {dst_fp}')

		# Request Html page and save
		response = _send_request(url)
		if response.status_code == 200:
			data = response.content
			_save_file(data, dst_fp)

			logger.info(f'file saved -> {dst_fp}')
			time.sleep(random())

		# break  # for testing



def extract_data_from_html(fp):
	pass



if __name__ == '__main__':
	
	# ===========================================================
	# 						Main pipeline
	# ===========================================================
	scrape_property_details(force=True)
	extract_from_html(fp='')

