import requests

from utils import url_to_filename, filename_to_url

"""
Get list of all stations in london, loop through them.
"""

def test_request():
	import requests

	url = "https://www.onthemarket.com/async/search/properties/?search-type=new-homes&location-id=london&retirement=false&view=grid"

	payload={}
	headers = {
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

	response = requests.request("GET", url, headers=headers, data=payload)

	print(response.text)



	

if __name__ == '__main__':
	url = "https://www.onthemarket.com/async/search/properties/?search-type=for-sale&location-id=london&page=1"
	

