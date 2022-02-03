import pandas as pd


# Set options
pd.set_option('display.max_columns', 50)

df = pd.read_csv('../../../scooter.csv')


for i, row in df.head().iterrows():
    if row['trip_id'] == 1613335:
        df.loc[i, 'new_column'] = 'Yes'
    else:
        df.loc[i, 'new_column'] = 'No'


print(df[['trip_id', 'new_column']].head())


df2 = df[['trip_id', 'started_at']].head()
print(df2['started_at'].str.split())


df3 = df2['started_at'].str.split(expand=True)
print(df3)

df2['date'] = df3[0]
df2['time'] = df3[1]
print(df2)


when = '2019-05-23'
x = df.loc[df['started_at'] > when]
print(len(x))


df2['started_at'] = pd.to_datetime(df['started_at'], format='%m/%d/%Y %H:%M')
print(df2.dtypes)


when = '2019-05-23'
print(df2.loc[df['started_at'] > when])