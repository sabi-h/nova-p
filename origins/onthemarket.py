import base64
import time

import pandas as pd
import requests

from utils import url_to_filename, filename_to_url, url_to_fp, fp_to_url


"""
Get list of all stations in london, loop through them.
"""

def london_stations():
	return pd.read_csv('../data/misc/london-stations.csv')


BASE_URL = 'https://www.onthemarket.com/async/search/properties/?search-type=new-homes&location-id={location}&retirement=false&page={page}'
BASE_FP = '../data/onthemarket/raw/{}.json'
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
	locations = london_stations()

	for location in locations:
		
		properties = True
		page = 1
		fp = BASE_FP.format()

		while properties:
			request_data = {
				'location': location,
				'page': page
			}

			url = BASE_URL.format(**request_data)

			try:
				response = requests.request('GET', BASE_URL, headers=HEADERS, data={})
				json_data = response.json()
				
				with open(fp, 'w') as f:
					pass
					
				if len(response['properties']) == 0:
					properties = False

				properties = False
			except Exception as e:
				pass

			page += 1

			time.sleep(1)


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
	# test_request()
	main()
	# data = london_stations()['Station code'].unique()
	# print(data)
	

























