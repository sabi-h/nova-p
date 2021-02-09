import base64


def url_to_filename(url: str) -> bytes:
	return base64.b64encode(url.encode())


def filename_to_url(filename: str) -> str:
	return base64.b64decode(filename).decode()




if __name__ == '__main__':

	# Tests
	url = "https://www.onthemarket.com/async/search/properties/?search-type=for-sale&location-id=london&page=1"
	filename = url_to_filename(url)
	url_next = filename_to_url(filename)
	assert url == url_next


	