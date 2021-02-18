import base64
from datetime import datetime
import json
import os
import time

import pandas as pd
import requests

from utils import (
	get_filename,
	get_filepath,
	get_outward_codes,
	get_url,
)


yyyymm = datetime.now().strftime('%Y%m')


"""
- Loop through each station in london
- while there are properties of page < 100
- send request and store response in json format

"""

BASE_URL = 'https://www.onthemarket.com/async/search/properties/?search-type={search_type}&retirement=false&location-id={location_id}&page={page}'
DIR_PATH = f'../data/onthemarket/raw/{yyyymm}'
if not os.path.exists(DIR_PATH):
	os.makedirs(DIR_PATH)


HEADERS = {
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

def _save_response(json_data, fp):
	"""
	Saves response from request to filepath.
	"""
	with open(fp, 'w') as f:
		json.dump(json_data, f, indent=4)


def download_data():
	print('='*100, 'Starting Scraper...', '='*100, sep='\n', end='\n\n')
	
	outward_codes = get_outward_codes()

	for location in outward_codes:
		print('='*20, f'location: {location}', '='*20)

		for page in range(1, 42):

			url = get_url(BASE_URL, 'new-homes', location, page)
			filename = get_filename('new-homes', location, page)
			print(url, filename, sep='\n')
			
			fp = get_filepath(DIR_PATH, filename)
			if os.path.exists(fp):
				print(f'fp exists: {fp}', '\n\n')
				continue

			response = requests.request('GET', url, headers=HEADERS, data={})

			if response.status_code == 200:
				json_data = response.json()
				if json_data['properties']:
					_save_response(json_data, fp)
				else:
					print('No properties found...')
					break

			print('Success...', '\n\n')
			time.sleep(1)

		print('\n', '*'*50, '\n\n')


def test_request():
	import requests

	url = "https://www.onthemarket.com/async/search/properties/?search-type=new-homes&location-id=WIJ&retirement=false&view=grid"

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

	response = requests.request("GET", url, headers=headers, data=payload)

	return response.json()


if __name__ == '__main__':
	download_data()
	
	pass
























