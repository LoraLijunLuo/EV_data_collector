import requests
import pandas as pd

url = 'https://api.openchargemap.io/v3/poi/'
parameters = {
    'output': 'json',
    'countrycode': 'DK',
    'maxresults': 5000,
    'compact': True,
    'verbose': False,
    'key': '8e8c6b2d-6735-4fab-8a64-09672c92c3ba'  
}

response = requests.get(url, params=parameters)
data = response.json()

df = pd.json_normalize(data)
df.to_csv('data/charging_stations.csv', index=False)

print(f'Finished scraping, and extracted {len(df)} records of charging stations')


# Data cleaning
print(df.columns)
columns_to_keep = ['AddressInfo.Latitude', 'AddressInfo.Longitude',
                   'AddressInfo.CountryID', 'NumberOfPoints']
df_clean = df[columns_to_keep].copy()

df_clean = df_clean.rename(columns={
    "AddressInfo.Latitude": "Latitude",
    "AddressInfo.Longitude": "Longitude",
    "AddressInfo.CountryID": "CountryCode"
})

df_clean = df_clean.dropna(subset=['Latitude', 'Longitude']) # Define in which columns to look for missing values. Drop when any of the 2 columns has missing values

df_clean.to_csv('data/charging_cleaned.csv', index=False)