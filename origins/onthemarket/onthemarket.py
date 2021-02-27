import base64
import csv
import json
import logging
import os
import time

from datetime import datetime
from pprint import pprint
from typing import Generator

import pandas as pd
import requests

from definitions import ROOT_DIR
from origins.utils import (
	get_filename,
	get_filepath,
	get_outward_codes,
	get_url,
	process_df_columns,
)
from origins.onthemarket.schema import schema


# ================================================================================
# 									Logging
# ================================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s:')

file_handler = logging.FileHandler('../../logs/onthemarket.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
# ================================================================================


yyyymm = datetime.now().strftime('%Y%m')

BASE_URL = 'https://www.onthemarket.com/async/search/properties/?search-type={search_type}&retirement=false&location-id={location_id}&page={page}'

DIR_PATH_RAW = f'../../data/onthemarket/property_tiles/raw/{yyyymm}'
DIR_PATH_PROCESSED = f'../../data/onthemarket/property_tiles/processed/{yyyymm}'
DIR_PATH_AGGREGATED = f'../../data/onthemarket/property_tiles/aggregated/'

# Create directories if they do not exist
for _dir in [DIR_PATH_RAW, DIR_PATH_PROCESSED, DIR_PATH_AGGREGATED]:
	if not os.path.exists(_dir):
		os.makedirs(_dir)


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

def _save_response(json_data, fp):
	"""
	Saves response from request to filepath.
	"""
	with open(fp, 'w') as f:
		json.dump(json_data, f, indent=4)


def download():
	logger.info('Starting Scraper...')
	outward_codes = get_outward_codes()

	for location in outward_codes:
		logger.info(f'==location: {location}==')

		for page in range(1, 42):

			url = get_url(BASE_URL, 'new-homes', location, page)
			filename = get_filename('new-homes', location, page)
			logger.info(f'url={url} - filename={filename}')
			
			fp = get_filepath(DIR_PATH_RAW, filename)
			if os.path.exists(fp):
				logger.info(f'fp exists: {fp}')
				continue

			response = requests.request('GET', url, headers=HEADER_URL, data={})
			time.sleep(1)

			if response.status_code == 200:
				json_data = response.json()
				if json_data['properties']:
					_save_response(json_data, fp)
				else:
					logger.info('No properties found...')
					break


def _get_files(dir_path: str) -> Generator[str, None, None]:
	"""
	Returns a generator where each item is a filepath
	"""
	for root, dirs, files in os.walk(dir_path):
		for file in files:
			yield os.path.join(root, file)


def _read_file(fp: str) -> str:
	with open(fp, 'r') as f:
		data = f.read()
	return data


def _data_to_json(data: str) -> dict:
	return json.loads(data)


def _process_property(property_row: dict) -> dict:
	result = {
		'id':						property_row.get('id', ''),
		'images-count':				property_row.get('images-count', ''),
		'price-qualifier':			property_row.get('price-qualifier', ''),
		'new-home-flag':			property_row.get('new-home-flag', ''),
		'display_address':			property_row.get('display_address', ''),
		'cover-images-default':		property_row.get('cover-images', {}).get('default', ''),
		'cover-images-webp':		property_row.get('cover-images', {}).get('webp', ''),
		'floorplans-count':			property_row.get('floorplans-count', ''),
		'summary':					property_row.get('summary', ''),
		'property-labels':			property_row.get('property-labels', ''),
		'property-title':			property_row.get('property-title', ''),
		'property-link':			property_row.get('property-link', ''),
		'cover-image':				property_row.get('cover-image', ''),
		'price':					property_row.get('price', ''),
		'floorplans?':				property_row.get('floorplans?', ''),
		'for-sale?':				property_row.get('for-sale?', ''),
		'agent-base-contact-url':	property_row.get('agent', {}).get('base-contact-url', ''),
		'agent-contact-url':		property_row.get('agent', {}).get('contact-url', ''),
		'agent-details-url':		property_row.get('agent', {}).get('details-url', ''),
		'agent-development?':		property_row.get('agent', {}).get('development?', ''),
		'agent-display-logo-url':	property_row.get('agent', {}).get('display-logo', {}).get('url', ''),
		'agent-id':					property_row.get('agent', {}).get('id', ''),
		'agent-name':				property_row.get('agent', {}).get('name', ''),
		'agent-telephone':			property_row.get('agent', {}).get('telephone', ''),
	}

	return result


def _flatten_json(data: dict) -> list:
	result = []

	property_rows = data.get('properties', [])
	for property_row in property_rows:
		dict_row = _process_property(property_row)
		result.append(dict_row)

	return result


def _save_as_csv(data, fp):
	df = pd.DataFrame(data)
	df.to_csv(fp, index=False)


def process():
	files = _get_files(DIR_PATH_RAW)

	for fp_json in files:
		logger.info(fp_json)

		data = _read_file(fp_json)
		data_json = _data_to_json(data)
		data_flattened = _flatten_json(data_json)

		csv_fp = os.path.join(DIR_PATH_PROCESSED, os.path.basename(fp_json).rsplit('.', 1)[0] + '.csv')
		_save_as_csv(data_flattened, csv_fp)


HEADER_CSV = [
	'images-count',
	'price-qualifier',
	'new-home-flag',
	'display_address',
	'cover-images-default',
	'cover-images-webp',
	'floorplans-count',
	'summary',
	'property-labels',
	'property-title',
	'id',
	'property-link',
	'cover-image',
	'price',
	'floorplans?',
	'for-sale?',
	'agent-base-contact-url',
	'agent-contact-url',
	'agent-details-url',
	'agent-development?',
	'agent-display-logo-url',
	'agent-id',
	'agent-name',
	'agent-telephone',
]

def _fp_to_df(fp: str) -> pd.DataFrame:
	return pd.read_csv(fp)


def _df_to_csv(df, fp):
	df.to_csv(fp, index=False)


def _concat_dfs(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
	return pd.concat([df1, df2], ignore_index=True)


def aggregate():
	result_df = pd.DataFrame(columns=HEADER_CSV)
	result_df = process_df_columns(result_df, HEADER_CSV)

	files = _get_files(DIR_PATH_PROCESSED)

	for fp_csv in files:
		logger.info(fp_csv)

		df = _fp_to_df(fp_csv)
		df = process_df_columns(df, HEADER_CSV)
		result_df = _concat_dfs(result_df, df)
	
	csv_fp = os.path.join(DIR_PATH_AGGREGATED, f'{yyyymm}.csv')

	_df_to_csv(result_df, csv_fp)
	logger.info(f'Success...file written to={csv_fp}')


if __name__ == '__main__':
	
	# ===========================================================
	# 						Helper Functions
	# ===========================================================

	# files = _get_files(DIR_PATH_RAW)
	# fp_json = next(files)
	# print(f'fp_json: {fp_json}')
	# logger.info(f'fp_json: {fp_json}')


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
	download()
	process()
	aggregate()




