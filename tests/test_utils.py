from origins.utils import (
	url_to_filename, 
	filename_to_url, 
	url_to_fp, fp_to_url
)


def test_url_to_fp():
	url = 'https://www.onthemarket.com/async/search/properties/?search-type=new-homes&location-id=WIJ&retirement=false&view=grid'
	fp = url_to_fp(url)
	assert fp == 'aHR0cHM6Ly93d3cub250aGVtYXJrZXQuY29tL2FzeW5jL3NlYXJjaC9wcm9wZXJ0aWVzLz9zZWFyY2gtdHlwZT1uZXctaG9tZXMmbG9jYXRpb24taWQ9V0lKJnJldGlyZW1lbnQ9ZmFsc2Umdmlldz1ncmlk'


def test_fp_to_url():
	fp = 'aHR0cHM6Ly93d3cub250aGVtYXJrZXQuY29tL2FzeW5jL3NlYXJjaC9wcm9wZXJ0aWVzLz9zZWFyY2gtdHlwZT1uZXctaG9tZXMmbG9jYXRpb24taWQ9V0lKJnJldGlyZW1lbnQ9ZmFsc2Umdmlldz1ncmlk'
	url = fp_to_url(fp)
	assert url == 'https://www.onthemarket.com/async/search/properties/?search-type=new-homes&location-id=WIJ&retirement=false&view=grid'