import base64
import csv
from datetime import datetime
import json
import os
from pprint import pprint
import time

import pandas as pd

from utils import (
	get_filename,
	get_filepath,
	get_outward_codes,
	get_url,
)


yyyymm = datetime.now().strftime('%Y%m')

DIR_PATH = f'../data/onthemarket/raw/{yyyymm}'

def _get_files(dir_path: str):
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


def _process_property_agent(property_agent_row):
	return ''

def _process_property(property_row):
	header = [
		'images-count',
		'price-qualifier',
		'new-home-flag',
		'display_address',
		'cover-images',
		'floorplans-count',
		'agent',
		'summary',
		'property-labels',
		'property-title',
		'id',
		'property-link',
		'cover-image',
		'price',
		'floorplans?',
		'for-sale?',
	]

	result = {}
	for k, v in property_row.items():
		property_row[]

	return


def _json_to_csv(data) -> list:
	property_rows = data['properties']
	for property_row in property_rows:
		_process_property(property_row)
		break

	return []


def _save_csv():
	return


def process():
	return


if __name__ == '__main__':
	
	files = _get_files(DIR_PATH)
	fp = next(files)
	assert isinstance(fp, str)

	data = _read_file(fp)
	assert isinstance(data, str)

	data_json = _data_to_json(data)
	assert isinstance(data_json, dict)


	data_csv = _json_to_csv(data_json)
	assert isinstance(data_csv, list)	
	
	pass
























