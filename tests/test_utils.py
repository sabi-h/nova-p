from origins.utils import (
	url_to_filename, 
	filename_to_url,
	request_data_to_filename,
)


def test_url_to_filename():
	url = 'https://www.onthemarket.com/async/search/properties/?search-type=new-homes&location-id=WIJ&retirement=false&view=grid'
	fp = url_to_filename(url)
	assert fp == 'aHR0cHM6Ly93d3cub250aGVtYXJrZXQuY29tL2FzeW5jL3NlYXJjaC9wcm9wZXJ0aWVzLz9zZWFyY2gtdHlwZT1uZXctaG9tZXMmbG9jYXRpb24taWQ9V0lKJnJldGlyZW1lbnQ9ZmFsc2Umdmlldz1ncmlk'


def test_filename_to_url():
	fp = 'aHR0cHM6Ly93d3cub250aGVtYXJrZXQuY29tL2FzeW5jL3NlYXJjaC9wcm9wZXJ0aWVzLz9zZWFyY2gtdHlwZT1uZXctaG9tZXMmbG9jYXRpb24taWQ9V0lKJnJldGlyZW1lbnQ9ZmFsc2Umdmlldz1ncmlk'
	url = filename_to_url(fp)
	assert url == 'https://www.onthemarket.com/async/search/properties/?search-type=new-homes&location-id=WIJ&retirement=false&view=grid'


def test_request_data_to_filename():
	request_data = {
		'search_type': 'new-homes',
		'location_id': 'e10',
		'page': '1',
	}
	
	fname = request_data_to_filename(request_data)
	assert fname == 'new-homes-e10-1'