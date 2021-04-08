import base64
import csv
import json
import os
import re
import time
from datetime import datetime
from pprint import pprint
from typing import Generator

import pandas as pd
import requests

from definitions import ROOT_DIR

from nova.utils import get_outward_codes


yyyymm = datetime.now().strftime('%Y%m')
DEFAULT_PARAMS = {}

BASE_URL = 'https://www.onthemarket.com/async/search/properties/'

HEADER = {
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

FIELDS = [
	'id',
	'images_count',
	'price_qualifier',
	'new_home_flag',
	'display_address',
	'cover_images_default',
	'cover_images_webp',
	'floorplans_count',
	'summary',
	'property_labels',
	'property_title',
	'property_link',
	'cover_image',
	'price',
	'floorplans',
	'for_sale',
	'agent_base_contact_url',
	'agent_contact_url',
	'agent_details_url',
	'agent_development',
	'agent_display_logo_url',
	'agent_id',
	'agent_name',
	'agent_telephone',
]


def _get_properties(
	outward_code: str,
	search_type: str='new-homes', 
	retirement='false',
	max_pages=42,
	sleep: float=0.2
	) -> Generator[dict, None, None]:

	"""
	Returns properties listed on onthemarket within the area.

	Yield
	------
	Generator
		Generator of dicts, where each dict contains information of one property.
	
	"""
	for page in range(1, max_pages+1):

		params = {
			'location-id': outward_code,
			'page': page,
			'search-type': search_type,
			'retirement': retirement,
		}

		response = requests.request('GET', BASE_URL, params=params, headers=HEADER, data={})
		time.sleep(sleep)

		try:
			json_data = response.json()
			properties = json_data['properties']

		except Exception as e:
			print(f'Could not download data for:\n >>> {url}', e, sep='\n\n')
			properties = []

		for _property in properties:
			yield _property


def _flatten_property(row: dict) -> tuple:
	"""
	Flatten the json and return a tuple.

	{
		'agent': {
			'base-contact-url': '/agents/contact/6292519/',
			'contact-url': '/agents/contact/6292519/?form-name=details-contact',
			'details-url': '/agents/branch/knight-frank-city-and-east-residential-development/',
			'development?': False,
			'display-logo': {
					'height': 43,
					'resized?': True,
					'url': 'https://media.onthemarket.com/agents/branches/37782/150609132133033/logo-100x65.jpg',
					'width': 100
			},
			'id': 37782,
			'name': 'Knight Frank - City & East, Residential Development',
			'telephone': '020 8022 6382'
		},
		'composite-eb-cover-image': {
			'default': 'https://media.onthemarket.com/properties/6292519/1337939268/composite.jpg',
			'webp': 'https://media.onthemarket.com/properties/6292519/1337939268/composite.webp'
		},
		'cover-image': 'https://media.onthemarket.com/properties/6292519/1337821444/image-0-480x320.jpg',
		'cover-images': {
			'default': 'https://media.onthemarket.com/properties/6292519/1337821444/image-0-480x320.jpg',
			'webp': 'https://media.onthemarket.com/properties/6292519/1337821444/image-0-480x320.webp'
		},
		'display_address': 'Unit 14 - Osborn Apartments, Osborn Street, London, E1',
		'floorplans-count': 1,
		'floorplans?': True,
		'for-sale?': True,
		'id': '6292519',
		'images-count': 7,
		'new-home-flag': True,
		'price': '£715,000',
		'price-qualifier': None,
		'property-labels': ['New build'],
		'property-link': '/details/6292519/',
		'property-title': '1 bedroom flat for sale',
		'summary': 'Stylish One bedroom apartments...'
	}
	"""
	result = {
		'id':						row.get('id', ''),
		'images_count':				row.get('images-count', ''),
		'price_qualifier':			row.get('price-qualifier', ''),
		'new_home_flag':			row.get('new-home-flag', ''),
		'display_address':			row.get('display_address', ''),
		'cover_images_default':		row.get('cover-images', {}).get('default', ''),
		'cover_images_webp':		row.get('cover-images', {}).get('webp', ''),
		'floorplans_count':			row.get('floorplans-count', ''),
		'summary':					row.get('summary', ''),
		'property_labels':			row.get('property-labels', ''),
		'property_title':			row.get('property-title', ''),
		'property_link':			row.get('property-link', ''),
		'cover_image':				row.get('cover-image', ''),
		'price':					row.get('price', ''),
		'floorplans':				row.get('floorplans?', ''),
		'for_sale':					row.get('for-sale?', ''),
		'agent_base_contact_url':	row.get('agent', {}).get('base-contact-url', ''),
		'agent_contact_url':		row.get('agent', {}).get('contact-url', ''),
		'agent_details_url':		row.get('agent', {}).get('details-url', ''),
		'agent_development':		row.get('agent', {}).get('development?', ''),
		'agent_display_logo_url':	row.get('agent', {}).get('display-logo', {}).get('url', ''),
		'agent_id':					row.get('agent', {}).get('id', ''),
		'agent_name':				row.get('agent', {}).get('name', ''),
		'agent_telephone':			row.get('agent', {}).get('telephone', ''),
	}

	return result


def add_outward_code_to_row(row, outward_code):
	row['outward_code'] = outward_code
	return row


NUMBERS_MAP = {x: i+1 for i, x in enumerate(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'])}

def extract_bedrooms(text: str, numbers_map: dict) -> int:
	r = """
		(one|two|three|four|five|six|seven|eight|nine|ten|\d+)
		[\s-]?
		bed
	"""
	items = re.findall(r, text, flags=re.VERBOSE | re.IGNORECASE)
	if not items:
		return 0

	bedrooms = items[0]

	if bedrooms in [str(x) for x in range(1, 11)]:
		return int(bedrooms)

	return numbers_map.get(bedrooms.lower(), 0)


def extract_price(text) -> int:
	text = text.replace(',', '').replace('£', '')
	if text and text != 'nan':
		return int(text)
	return 0

	
def main(
	outward_code: str,
	search_type: str='new-homes', 
	retirement='false', 
	max_pages=1,
	sleep: float=0.2
	) -> Generator[dict, None, None]:
	"""
	Parameters
	----------
	outward_code : str
		Postcode districts in UK from:
			https://en.wikipedia.org/wiki/List_of_postcode_districts_in_the_United_Kingdom

	search_type : str, optional
		Type of home, options are:
			commercial, for-sale, prices, to-rent, overseas, new-homes, farms-land, developments, agents, student

	retirement : str, optional
		'true' or 'false'

	max_pages : int, optional
		Maximum number of pages to get, 42 is the max.
	
	sleep : float, optional
		Amount of time to sleep between each request. Every page makes a new request.
	
	Yield
	------
	Generator
		Generator of dicts, where each dict contains information of one property.

	"""
	properties = _get_properties(
		outward_code,
		search_type=search_type,
		retirement=retirement,
		max_pages=max_pages,
		sleep=sleep
	)

	for row in properties:
		row = _flatten_property(row)
		row['outward_code'] = outward_code
		row['bedrooms'] = extract_bedrooms(row['summary'], numbers_map=NUMBERS_MAP)
		row['raw_price'] = row['price']
		row['price'] = extract_price(row['price'])

		yield row


if __name__ == '__main__':

	# ===========================================================
	#                       	Test
	# ===========================================================
	data = main(outward_code='e1', max_pages=1)
	for row in data:
		pprint(row)
		print('---------')
		# break

	# download()
	# process()
	# aggregate()
	# transform()



