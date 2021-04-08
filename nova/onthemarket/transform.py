
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




