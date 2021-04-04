import base64
import csv
import json
import os
import time
from datetime import datetime
from pprint import pprint
from typing import Generator

import pandas as pd
import requests

from definitions import ROOT_DIR

from nova.data import outward_codes
from nova.utils import (
	get_filepath,
	get_files,
	get_last_file,
	get_outward_codes,
	get_url,
	process_df_columns
)


yyyymm = datetime.now().strftime('%Y%m')
DEFAULT_PARAMS = {}

BASE_URL = 'https://www.onthemarket.com/async/search/properties/?search-type={search_type}&retirement=false&location-id={location_id}&page={page}'

HEADER_URL = {
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


def get_properties(outward_code: str, params={}) -> list:
	"""
	Takes outward_code and returns pandas dataframe containing
	properties listed on onthemarket within the area.

	Parameters
	----------
	outward_code : str
		Postcode districts in UK from:
			https://en.wikipedia.org/wiki/List_of_postcode_districts_in_the_United_Kingdom

	Returns
	-------
	list
	    list of dicts, where each dict contains information of one property.

	"""
	for page in range(1, 42):

		url = get_url(BASE_URL, 'new-homes', outward_code, page)
		response = requests.request('GET', url, headers=HEADER_URL, data={})
		time.sleep(0.2)

		try:
			json_data = response.json()
			properties = json_data['properties']

		except Exception as e:
			print(f'Could not download data for:\n >>> {url}', e, sep='\n\n')
			properties = []

		for _property in properties:
			yield _property

		break	# For testing


def _process_property(property_row: dict) -> tuple:
	row = (
		property_row.get('id', ''),
		property_row.get('images-count', ''),
		property_row.get('price-qualifier', ''),
		property_row.get('new-home-flag', ''),
		property_row.get('display_address', ''),
		property_row.get('cover-images', {}).get('default', ''),
		property_row.get('cover-images', {}).get('webp', ''),
		property_row.get('floorplans-count', ''),
		property_row.get('summary', ''),
		property_row.get('property-labels', ''),
		property_row.get('property-title', ''),
		property_row.get('property-link', ''),
		property_row.get('cover-image', ''),
		property_row.get('price', ''),
		property_row.get('floorplans?', ''),
		property_row.get('for-sale?', ''),
		property_row.get('agent', {}).get('base-contact-url', ''),
		property_row.get('agent', {}).get('contact-url', ''),
		property_row.get('agent', {}).get('details-url', ''),
		property_row.get('agent', {}).get('development?', ''),
		property_row.get('agent', {}).get('display-logo', {}).get('url', ''),
		property_row.get('agent', {}).get('id', ''),
		property_row.get('agent', {}).get('name', ''),
		property_row.get('agent', {}).get('telephone', ''),
	)

	return result


def main():
	result_df = pd.DataFrame(columns=FIELDS)
	result_df = process_df_columns(result_df, FIELDS)
	
	properties = get_properties('e1')
	for p in properties:
		if not p:
			continue
		p = _process_property(p)
		pprint(p)


def _concat_dfs(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
	return pd.concat([df1, df2], ignore_index=True)


def aggregate():
	result_df = pd.DataFrame(columns=FIELDS)
	result_df = process_df_columns(result_df, FIELDS)

	files = get_files(DIR_PATH_PROCESSED)

	for fp_csv in files:

		df = _fp_to_df(fp_csv)
		df = process_df_columns(df, FIELDS)
		result_df = _concat_dfs(result_df, df)
	
	csv_fp = os.path.join(DIR_PATH_AGGREGATED, f'{yyyymm}.csv')


def transform():
	file = get_last_file(DIR_PATH_AGGREGATED)
	df = pd.read_csv(file)
	print(df.columns)



if __name__ == '__main__':
	
	# ===========================================================
	# 						Helper Functions
	# ===========================================================

	# files = get_files(DIR_PATH_RAW)
	# fp_json = next(files)
	# print(f'fp_json: {fp_json}')
	#


	# data = _read_file(fp_json)
	# assert isinstance(data, str)

	# data_json = _data_to_json(data)
	# assert isinstance(data_json, dict)

	# data_flattened = _flatten_json(data_json)
	# assert isinstance(data_flattened, list)

	# csv_fp = os.path.join(DIR_PATH_PROCESSED, os.path.basename(fp_json).rsplit('.', 1)[0] + '.csv')
	# _save_as_csv(data_flattened, csv_fp)
	


	# ===========================================================
	# 						Main pipeline
	# ===========================================================
	main()
	# download()
	# process()
	# aggregate()
	# transform()




