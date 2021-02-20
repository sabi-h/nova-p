from origins.onthemarket_processor import (
	# _get_files,
	# _read_file,
	# _data_to_json,
	_process_property_agent,
	# _process_property,
	# _json_to_csv,
	# _save_csv,
	# process,
)


# def test_get_files():
# 	assert False


# def test_read_file():
# 	assert False


# def test_data_to_json():
# 	assert False


def test_process_property_agent():
	agent_raw = {
		'base-contact-url': '/agents/contact/9527875/',
		'contact-url': '/agents/contact/9527875/?form-name=details-contact',
		'details-url': '/agents/branch/blueprint-properties-london/',
		'development?': False,
		'display-logo': {   
			'height': 53,
			'resized?': True,
			'url': 'https://media.onthemarket.com/agents/companies/8005/180920104655149/logo-100x65.png',
			'width': 100
		},
		'id': 48801,
		'name': 'Blueprint Properties - London',
		'telephone': '020 8128 1242'
	}

	agent_expected = {
		'base-contact-url': '/agents/contact/9527875/',
		'contact-url': '/agents/contact/9527875/?form-name=details-contact',
		'details-url': '/agents/branch/blueprint-properties-london/',
		'development?': False,
		'display-logo-url': 'https://media.onthemarket.com/agents/companies/8005/180920104655149/logo-100x65.png',
		'id': 48801,
		'name': 'Blueprint Properties - London',
		'telephone': '020 8128 1242'
	}

	agent_processed = _process_property_agent(agent_raw)
	assert agent_processed == agent_expected


# def test_process_property():
# 	assert False


# def test_json_to_csv():
# 	assert False


# def test_save_csv():
# 	assert False


# def testprocess():
# 	assert False






