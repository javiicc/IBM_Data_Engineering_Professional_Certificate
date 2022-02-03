import pandas as pd


# Set options
pd.set_option('display.max_columns', 50)

df = pd.read_csv('../../../scooter.csv')


df.drop(columns=['region_id'], inplace=True)
df.drop(index=[34225], inplace=True)

print(df.loc[df['start_location_name'].isna(), 'start_location_name'])
df.dropna(subset=['start_location_name'], inplace=True)
print('\n', df.loc[df['start_location_name'].isna(), 'start_location_name'])

print('\n')
print(df.loc[(df['start_location_name'].isna()) | (df['end_location_name'].isna()),
             ['start_location_name', 'end_location_name']])
startstop = df.loc[(df['start_location_name'].isna()) | (df['end_location_name'].isna())].copy()
value = {
    'start_location_name': 'Start St.',
    'end_location_name': 'Stop St.'
}
startstop.fillna(value=value, inplace=True)
print(startstop[['start_location_name', 'end_location_name']])

print('\n', '-'*10, 'MAY', '-'*10)
may = df[df['month'] == 'May']
print(may)

df.drop(index=may.index, inplace=True)
print(df['month'].value_counts())

# df.columns = [x.upper() for x in df.columns]
# print(df.columns)

# df.rename(columns={'DURATION': 'duration'}, inplace=True)
df.rename(columns={'DURATION': 'duration', 'region_id': 'region'}, inplace=True)

df['month'] = df['month'].str.upper()
print(df['month'].head())

