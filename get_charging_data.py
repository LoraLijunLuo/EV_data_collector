import requests
import pandas as pd

url = 'https://api.openchargemap.io/v3/poi/'
parameters = {
    "output": 'json',
    "countrycode": 'DK',
    "maxresults": 5000,
    "compact": True,
    "verbose": False,
    "key": '8e8c6b2d-6735-4fab-8a64-09672c92c3ba'  
}

response = requests.get(url, params=parameters)
data = response.json()

df = pd.json_normalize(data)
df.to_csv("charging_stations.csv", index=False)

print(f"Finished scraping, and extracted {len(df)} records of charging stations")
