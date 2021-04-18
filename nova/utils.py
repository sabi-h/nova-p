from nova.data import outward_codes


def get_outward_codes() -> list:
	"""
	Returns list of london outward codes
	"""
	return [k for k in outward_codes]


def get_district_name(outward_code):
	return outward_codes.get(outward_code.lower(), 'unknown')



def process_df_columns(df, columns):
	"""
	- Adds missing columns
	- removes extra columns
	- orders columns

	"""
	df_columns = df.columns

	# add the missing columns with null values
	for column in columns:
		if column not in df_columns:
			df[column] = None

	# Select and Order columns
	df = df[columns]

	return df


def flatten_json(y):
	"""
	Naively flattens a json.
	"""
	out = {} 

	def flatten(x, name =''): 
		
		# If the Nested key-value 
		# pair is of dict type 
		if type(x) is dict: 
			
			for a in x: 
				flatten(x[a], name + a + '_') 
				
		# If the Nested key-value 
		# pair is of list type 
		elif type(x) is list: 
			
			i = 0
			
			for a in x:              
				flatten(a, name + str(i) + '_') 
				i += 1
		else:
			out[name[:-1]] = x 

	flatten(y) 
	return out


if __name__ == '__main__':
	print(get_district_name('E1'))


