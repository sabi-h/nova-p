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

BASE_URL = '[BASE_URL]'

DIR_PATH_RAW = os.path.join(ROOT_DIR, f'data/onthemarket/property_details/raw/{yyyymm}')
DIR_PATH_PROCESSED = os.path.join(ROOT_DIR, f'data/onthemarket/property_details/processed/{yyyymm}')
DIR_PATH_AGGREGATED = os.path.join(ROOT_DIR, f'data/onthemarket/property_details/aggregated/')

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
	pass


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
	result = property_row
	return result


def _flatten_json(data: dict) -> list:
	result = data
	return result


def _save_as_csv(data, fp):
	df = pd.DataFrame(data)
	df.to_csv(fp, index=False)


def process():
	pass


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
	pass


if __name__ == '__main__':
	
	# ===========================================================
	# 						Main pipeline
	# ===========================================================
	download()
	process()
	aggregate()




