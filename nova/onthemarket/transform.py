NUMBERS_MAP = {x:i+1 for i, x in enumerate(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'])}
def extract_bedrooms(text: str, numbers_map: dict) -> int:
    r = '''
        (one|two|three|four|five|six|seven|eight|nine|ten|\d+)
        [\s-]?
        bed
    '''
    items = re.findall(r, text, flags=re.VERBOSE | re.IGNORECASE)
    if not items:
        return 0

    bedrooms = items[0]

    if bedrooms in [str(x) for x in range(1, 11)]:
        return int(bedrooms)

    return numbers_map.get(bedrooms.lower(), 0)


OUTWARD_CODES = outward_codes['outward_code'].to_list()
def extract_outward_code(text, outward_codes):
    text = text if text else ''
    
    found_codes = []
    for outward_code in outward_codes:
        if outward_code in text:
            found_codes.append(outward_code)
            
    no_of_outward_codes = len(found_codes)

    if no_of_outward_codes == 0:
        result = None
    
    elif no_of_outward_codes == 1:
        result = found_codes[0]
        
    else:
        result = max(found_codes, key=len)

    return result

assert extract_outward_code('The Atlas Building, 145 City Road, London, EC1V', OUTWARD_CODES) == 'EC1'


def extract_price(text) -> int:
    text = text.replace(',', '').replace('£', '')
    if text and text != 'nan':
        return int(text)
    return 0

# Create clean dataframe

def run(df):

    df['outward_code'] = df['display_address'].apply(lambda x: extract_outward_code(x, OUTWARD_CODES))
    df['bedrooms'] = df['summary'].apply(lambda x: extract_bedrooms(x, NUMBERS_MAP))
    df['price_extracted'] = df['price'].astype(str).apply(lambda x: extract_price(x))

    # Filter
    df = df[df['price_extracted'] != 0]
    df = df[df['bedrooms'] != 0]

    df.shape












