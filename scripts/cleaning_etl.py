import pandas as pd
import sqlite3

df = pd.read_csv('data/ev_raw_data.csv')

# Data cleaning - Handling missing data
df = df.replace('N/A', None) # Replace string N/A value with None
print(df.isnull().any(axis = 0)) # Find columns with missing values

# Found out all 3 price columns have missing values, 
# so wanted to only keep the column with the least missing values
print(df['Price in German_€'].isnull().sum())
print(df['Price in Netherlands_€'].isnull().sum())
print(df['Price in UK_£'].isnull().sum())
df_removed = df.drop(['Price in Netherlands_€', 'Price in UK_£'], axis = 1)
# Remove missing values 
df_cleaned = df_removed.dropna() # Drop rows which contain missing values
print(len(df_cleaned))

#df_cleaned['Price in German_€'] = df_cleaned['Price in German_€'].astype(int)
df_cleaned = df_cleaned.astype({'Price in German_€': 'int32'})

df_cleaned.to_csv('data/ev_data_cleaned.csv', index = False)



#Create a local SQLite database connection
conn = sqlite3.connect('data/ev_database.db')

df_cleaned.to_sql('ev_specs', conn, if_exists='replace', index=False)

result = pd.read_sql_query('SELECT * FROM ev_specs LIMIT 5;', conn)
print(result)

conn.close()