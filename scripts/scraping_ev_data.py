from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://ev-database.org/#group=vehicle-group&rs-pr=10000_100000&rs-er=0_1000&rs-ld=0_1000&rs-ac=2_23&rs-dcfc=0_300&rs-ub=10_200&rs-tw=0_2500&rs-ef=100_350&rs-sa=-1_5&rs-w=1000_3500&rs-c=0_5000&rs-y=2010_2030&s=1&p=0-10'
page = requests.get(url)
soup = BeautifulSoup(page.text,'html')
#print(soup.prettify())

cars = soup.find_all('div', class_='list-item')
car_list = []

for car in cars:
    #print(car.prettify())
    
    # Extract the Brand and Model
    name = car.find('h2').text.strip()
    brand = name.split(' ', 1)[0]
    model = name.split(' ', 1)[1]

    # Extract the Range data
    data_tooltip1 = car.find('div', attrs={'data-tooltip': 'Real range under standardized conditions'})
    range = data_tooltip1.find('span', class_='erange_real').text

    # Extract the Efficiency data
    data_tooltip2 = car.find('div', attrs={'data-tooltip': 'Efficiency under standardized conditions'})
    efficiency = data_tooltip2.find('span', class_='efficiency').text

    # Extract the Battery data
    data_tooltip3 = car.find('div', attrs={'data-tooltip': 'Useable battery capacity.'})
    battery = data_tooltip3.find('span', class_='battery hidden').text

    # Extract the fastcharge data
    data_tooltip4 = car.find('div', attrs={'data-tooltip': 'Average charging power over a charging session of 10% to 80% SoC'})
    fastcharge = data_tooltip4.find('span', class_='fastcharge_speed hidden').text

    # Extract the Price/range data
    data_tooltip5 = car.find('div', attrs={'data-tooltip': 'Price per km of range: indication of value for money. Combination of affordability and range. Lower figure is better.'})
    pricerange = data_tooltip5.find('span', class_='priceperrange hidden').text

    # Extract the Price
    pricingorg = car.find('div', class_='pricing org')
    price_de = pricingorg.find('span', class_='country_de').text
    price_nl = pricingorg.find('span', class_='country_nl').text
    price_uk = pricingorg.find('span', class_='country_uk').text
    
    car_list.append({
        'Brand': brand,
        'Model': model,
        'Range_km': range.split(' ', 1)[0],
        'Efficiency_Wh/km': efficiency.split(' ', 1)[0],
        'Battery_kWh': battery,
        'Fastcharge Speed_kW': fastcharge,
        'Price/Range_€/km': pricerange,
        'Price in German_€': price_de.replace('€', '').replace(',', '').replace('*', ''),
        'Price in Netherlands_€': price_nl.replace('€', '').replace(',', '').replace('*', ''),
        'Price in UK_£': price_uk.replace('£', '').replace(',', '').replace('*', '')
    })

df = pd.DataFrame(car_list)
df.to_csv('ev_raw_data.csv', index=False)

print(f'Finished scraping, and extracted {len(df)} cars')