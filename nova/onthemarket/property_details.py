import base64
import csv
import json
import logging
import os
import sys
import time
from datetime import datetime
from pprint import pprint
from random import random
from typing import Generator

import pandas as pd
import requests

from definitions import ROOT_DIR

from nova.onthemarket.schema import schema
from nova.utils import get_outward_codes


# ================================================================================
# 									To Do
# ================================================================================

#					- Complete extract_data_from_html function

# ================================================================================


yyyymm = datetime.now().strftime('%Y%m')

BASE_URL = 'https://www.onthemarket.com/'


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

		# Create filepath and check if it exists
		filename = url.rsplit('/', 1)[-1] + '.html'
		dst_fp = os.path.join(DIR_PATH_RAW, filename)

		if os.path.exists(dst_fp):

			if force == False:
				continue
			else:

		# Request html page and save
		response = _send_request(url)
		if response.status_code == 200:
			data = response.content
			_save_file(data, dst_fp)

			time.sleep(random())

		# break  # for testing


def extract_data_from_html(fp):
	pass



if __name__ == '__main__':
	
	# ===========================================================
	# 						Main pipeline
	# ===========================================================
	scrape_property_details(force=True)

