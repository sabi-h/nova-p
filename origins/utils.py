import base64
import os

import pandas as pd


def get_outward_codes():
	"""
	Returns list of london outward codes
	"""
	return pd.read_csv('../data/misc/london-outward-codes.csv')['outward_code'].str.lower().to_list()


def url_to_filename(url: str) -> str:
	return base64.b64encode(url.encode(encoding='utf-8')).decode(encoding='utf-8')


def filename_to_url(fp: str) -> str:
	return base64.b64decode(fp.encode(encoding='utf-8')).decode(encoding='utf-8')


def get_filename(search_type: str, location: str, page: int) -> str:
	return '-'.join((search_type, location, str(page))) + '.json'


def get_filepath(dir_path: str, filename: str) -> str:
	return os.path.join(dir_path, filename)


def get_url(base_url, search_type, location, page):
	request_data = {
		'search_type': search_type,
		'location_id': location,
		'page': page,
	}
	url = base_url.format(**request_data)
	return url



if __name__ == '__main__':

	# Tests
	url = "https://www.onthemarket.com/async/search/properties/?search-type=for-sale&location-id=london&page=1"
	fp = url_to_filename(url)
	url_next = filename_to_url(fp)
	result = (url == url_next)

	print(f'url == url_next: {result}')

	request_data = {
		'search_type': 'new-homes',
		'location_id': 'e10',
		'page': '1',
	}
	
	fname = get_filename(request_data)
	result = (fname == 'new-homes-e10-1')
	print(f"fname == 'new-homes-e10-1': {result}")