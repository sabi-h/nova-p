from origins.utils import (
	url_to_filename, 
	filename_to_url,
	get_outward_codes,
	get_filename,
	get_filepath,
	get_url,
)

def test_url_to_filename():
	url = 'https://www.onthemarket.com/async/search/properties/?search-type=new-homes&location-id=WIJ&retirement=false&view=grid'
	fp = url_to_filename(url)
	assert fp == 'aHR0cHM6Ly93d3cub250aGVtYXJrZXQuY29tL2FzeW5jL3NlYXJjaC9wcm9wZXJ0aWVzLz9zZWFyY2gtdHlwZT1uZXctaG9tZXMmbG9jYXRpb24taWQ9V0lKJnJldGlyZW1lbnQ9ZmFsc2Umdmlldz1ncmlk'


def test_filename_to_url():
	fp = 'aHR0cHM6Ly93d3cub250aGVtYXJrZXQuY29tL2FzeW5jL3NlYXJjaC9wcm9wZXJ0aWVzLz9zZWFyY2gtdHlwZT1uZXctaG9tZXMmbG9jYXRpb24taWQ9V0lKJnJldGlyZW1lbnQ9ZmFsc2Umdmlldz1ncmlk'
	url = filename_to_url(fp)
	assert url == 'https://www.onthemarket.com/async/search/properties/?search-type=new-homes&location-id=WIJ&retirement=false&view=grid'


def test_get_outward_codes():
	result = get_outward_codes()
	assert isinstance(result, list)
	assert len(result) > 0


def test_get_filename():
	assert get_filename('new-homes', 'e10', 1) == 'new-homes-e10-1.json'


def test_get_filepath():
	assert get_filepath('path/to/dir', 'example.json') == 'path/to/dir/example.json'


def test_get_url():
	url = get_url('https://base/', 'new-home', 'e10', 1)
	assert isinstance(url, str)

if __name__ == '__main__':
	print('yay')