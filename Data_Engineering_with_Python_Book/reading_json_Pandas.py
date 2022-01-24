import pandas as pd

# For clean, well-formatted jason file
# df = pd.read_json('data.json')

import pandas.io.json as pd_json

# Open file
f = open('data.json', 'r')
data = pd_json.loads(f.read())

# Create DataFrame
df = pd.json_normalize(data, record_path='records')

# Save df into json file with default orient column
# df.head(2).to_json(orient='column')

# Save df into json file with orient records (preferred)
df.head(2).to_json('json_from_df.json', orient='records')
