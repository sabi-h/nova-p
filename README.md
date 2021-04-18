## nova-p
One stop shop for your housing market data.

#### Setup project in dev mode

```
git clone https://github.com/sabih-h/nova-p.git
cd nova-p
pip install -e .
```

#### Basic Usage
```
import nova

outward_code = 'e1'
data = nova.get_data_onthemarket(outward_code)

for row in data:
    print(row)

>>> {'id': 1, 'price': 350000, 'bedrooms': 3, 'display_address': 'Tower Bridge, Whitechapel E1', ...}
```

#### Data Sources

- [x] [OnTheMarket](https://www.onthemarket.com/)
- [ ] [Price Paid data by gov.uk](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads)


#### Helper datasets
- [London Postal Disticts](https://en.wikipedia.org/wiki/London_postal_district)


#### Testing
`pytest -v`

