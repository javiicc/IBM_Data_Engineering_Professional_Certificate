import pandas as pd


# Set options
pd.set_option('display.max_columns', 50)

df = pd.read_csv('../../../scooter.csv')


new = pd.DataFrame(df['start_location_name'].value_counts().head())
# print(new)
new.reset_index(inplace=True)
new.columns = ['address', 'count']
print(new)

n = new['address'].str.split(',', n=1, expand=True)
print(n)

replaced = n[0].str.replace('@', 'and')
new['street'] = replaced
print(new)


geo = pd.read_csv('../../../geocodedstreet.csv')
print(geo)


# joined = new.join(other=geo, how='left', lsuffix='_new', rsuffix='_geo')
# print('\n', joined[['street_new', 'street_geo', 'x', 'y']])


merged = pd.merge(new, geo, on='street')
print('\n', merged.columns)
