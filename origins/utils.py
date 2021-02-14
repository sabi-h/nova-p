import base64


def url_to_filename(url: str) -> str:
	return base64.b64encode(url.encode(encoding='utf-8')).decode(encoding='utf-8')


def filename_to_url(fp: str) -> str:
	return base64.b64decode(fp.encode(encoding='utf-8')).decode(encoding='utf-8')


def request_data_to_filename(request_data: dict) -> str:
	return '-'.join([str(x) for x in request_data.values()])


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
	
	fname = request_data_to_filename(request_data)
	result = (fname == 'new-homes-e10-1')
	print(f"fname == 'new-homes-e10-1': {result}")