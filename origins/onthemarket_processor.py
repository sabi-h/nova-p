import base64
import csv
from datetime import datetime
import json
import os
from pprint import pprint
import time
from typing import Generator

import pandas as pd

from origins.utils import (
	get_filename,
	get_filepath,
	get_outward_codes,
	get_url,
)

yyyymm = datetime.now().strftime('%Y%m')

DIR_PATH_RAW = f'../data/onthemarket/raw/{yyyymm}'
DIR_PATH_PROCESSED = f'../data/onthemarket/processed/{yyyymm}'
if not os.path.exists(DIR_PATH_PROCESSED):
	os.makedirs(DIR_PATH_PROCESSED)


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
		'images-count':			property_row.get('images-count', ''),
		'price-qualifier':		property_row.get('price-qualifier', ''),
		'new-home-flag':		property_row.get('new-home-flag', ''),
		'display_address':		property_row.get('display_address', ''),
		'cover-images-default':	property_row.get('cover-images', {}).get('default', ''),
		'cover-images-webp':	property_row.get('cover-images', {}).get('webp', ''),
		'floorplans-count':		property_row.get('floorplans-count', ''),
		'summary':				property_row.get('summary', ''),
		'property-labels':		property_row.get('property-labels', ''),
		'property-title':		property_row.get('property-title', ''),
		'id':					property_row.get('id', ''),
		'property-link':		property_row.get('property-link', ''),
		'cover-image':			property_row.get('cover-image', ''),
		'price':				property_row.get('price', ''),
		'floorplans?':			property_row.get('floorplans?', ''),
		'for-sale?':			property_row.get('for-sale?', ''),
		'base-contact-url':		property_row.get('agent', {}).get('base-contact-url', ''),
		'contact-url':			property_row.get('agent', {}).get('contact-url', ''),
		'details-url':			property_row.get('agent', {}).get('details-url', ''),
		'development?':			property_row.get('agent', {}).get('development?', ''),
		'display-logo-url':		property_row.get('agent', {}).get('display-logo', {}).get('url', ''),
		'id':					property_row.get('agent', {}).get('id', ''),
		'name':					property_row.get('agent', {}).get('name', ''),
		'telephone':			property_row.get('agent', {}).get('telephone', ''),
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


def main():
	files = _get_files(DIR_PATH_RAW)

	for fp_json in files:
		print(fp_json)

		data = _read_file(fp_json)

		data_json = _data_to_json(data)

		data_flattened = _flatten_json(data_json)

		csv_fp = os.path.join(DIR_PATH_PROCESSED, os.path.basename(fp_json).rsplit('.', 1)[0] + '.csv')
		_save_as_csv(data_flattened, csv_fp)


if __name__ == '__main__':
	
	main()	

	# Tests
	files = _get_files(DIR_PATH_RAW)
	fp_json = next(files)
	assert isinstance(fp_json, str)

	data = _read_file(fp_json)
	assert isinstance(data, str)

	data_json = _data_to_json(data)
	assert isinstance(data_json, dict)

	data_flattened = _flatten_json(data_json)
	assert isinstance(data_flattened, list)

	csv_fp = os.path.join(DIR_PATH_PROCESSED, os.path.basename(fp_json).rsplit('.', 1)[0] + '.csv')
	_save_as_csv(data_flattened, csv_fp)


	# pprint(agent, indent=4)













