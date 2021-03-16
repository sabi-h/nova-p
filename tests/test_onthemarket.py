
from origins.onthemarket.property_tiles import (
	_save_response,
	# _get_files,
	# _read_file,
	# _data_to_json,
	# _process_property,
	# _flatten_json,
	# _save_as_csv,
	# _fp_to_df,
	# _df_to_csv,
	# _concat_dfs,
	# download,
	# process,
	# aggregate,
)

# def test_TO_REWRITE():
# 	agent_processed = _process_property_agent(agent_raw)
# 	assert agent_processed == agent_expected

# 	files = _get_files(DIR_PATH_RAW)
# 	fp_json = next(files)
# 	assert isinstance(fp_json, str)

# 	data = _read_file(fp_json)
# 	assert isinstance(data, str)

# 	data_json = _data_to_json(data)
# 	assert isinstance(data_json, dict)

# 	data_flattened = _flatten_json(data_json)
# 	assert isinstance(data_flattened, list)

# 	csv_fp = os.path.join(DIR_PATH_PROCESSED, os.path.basename(fp_json).rsplit('.', 1)[0] + '.csv')
# 	_save_as_csv(data_flattened, csv_fp)


def test__save_response():
	assert False


# def test__get_files():
# 	files = _get_files('../data/onthemarket/raw/202102')
# 	for fp_json in files:
# 		assert '../data/onthemarket/raw/202102' in fp_json


# def test__read_file():
# 	assert True


# def test__data_to_json():
# 	data = json.dumps({"hello": "world"})
# 	assert isinstance(_data_to_json(data), dict)


# def test__process_property():
# 	from origins.schemas import onthemarket as onthemarket_schema

# 	fields = [x['name'] for x in onthemarket_schema]
# 	mock_property_row = {x:'' for x in fields}
# 	processed_data = _process_property(mock_property_row)
	
# 	assert list(processed_data.keys()) == list(fields)


# def test__flatten_json():
# 	assert False


# def test__save_as_csv():
# 	assert False


# def test__fp_to_df():
# 	assert False


# def test__df_to_csv():
# 	assert False


# def test__concat_dfs():
# 	assert False


# def test_download():
# 	assert False


# def test_process():
# 	assert False


# def test_aggregate():
# 	assert False







