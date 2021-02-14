import base64
from datetime import datetime
import json
import os
import time

import pandas as pd
import requests

from utils import request_data_to_filename

yyyymm = datetime.now().strftime('%Y%m')

"""
- Loop through each station in london
- while there are properties of page < 100
- send request and store response in json format

"""

def london_stations():
	return pd.read_csv('../data/misc/london-stations.csv')


def london_outward_codes():
	return pd.read_csv('../data/misc/london-outward-codes.csv')['outward_code'].str.lower().to_list()


BASE_URL = 'https://www.onthemarket.com/async/search/properties/?search-type={search_type}&retirement=false&location-id={location_id}&page={page}'
BASE_FP = '../data/onthemarket/raw/{yyyymm}/{filename}.json'
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

def main():
	outward_codes = london_outward_codes()

	print('='*100, 'Starting Scraper...', '='*100, sep='\n', end='\n\n')

	for location in outward_codes:

		print(f'location: {location}')

		for page in range(1, 100):
			print(f'page: {page}')

			request_data = {
				'search_type': 'new-homes',
				'location_id': location,
				'page': page,
			}

			url = BASE_URL.format(**request_data)
			print(f'url: {url}')

			filename = request_data_to_filename(request_data)
			fp = BASE_FP.format(yyyymm=yyyymm, filename=filename)

			dirname = os.path.dirname(fp)
			if not os.path.exists(dirname):
				os.makedirs(dirname)

			if os.path.exists(fp):
				print(f'fp exists: {fp}')
				continue

			print(f'fp: {fp}', '\n')

			try:
				response = requests.request('GET', url, headers=HEADERS, data={})
				print(f'response: {response}')
				json_data = response.json()

			except Exception as e:
				print('ERROR:', e)

			if json_data['properties']:
				print('properties exist, writing to file...')
				with open(fp, 'w') as f:
					json.dump(json_data, f, indent=4)
			else:
				break

			time.sleep(1)
			print('\n\n')


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

	main()
	

	pass
























