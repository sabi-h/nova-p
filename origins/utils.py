import base64


def url_to_filename(url: str) -> bytes:
	return base64.b64encode(url.encode())


def filename_to_url(filename: str) -> str:
	return base64.b64decode(filename).decode()


def url_to_fp(url):
	return base64.b64encode(url.encode(encoding='utf-8')).decode(encoding='utf-8')


def fp_to_url(fp):
	return base64.b64decode(fp.encode(encoding='utf-8')).decode(encoding='utf-8')


if __name__ == '__main__':

	# Tests
	url = "https://www.onthemarket.com/async/search/properties/?search-type=for-sale&location-id=london&page=1"
	filename = url_to_filename(url)
	url_next = filename_to_url(filename)
	assert url == url_next


	