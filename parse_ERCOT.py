import pandas as pd
import os
import requests

supply_url = 'https://www.ercot.com/api/1/services/read/dashboards/supply-demand.json'
system_demand_url = 'https://www.ercot.com/api/1/services/read/dashboards/system-wide-demand.json'

ercot_data = [supply_url, system_demand_url]
os.makedirs('data/raw/environment', exist_ok=True)
for data in ercot_data:
    r = requests.get(data)
    fname = data.split('/')[-1].split('.')[0]
    if 'supply' in fname:
        # print('supply')
        df = pd.DataFrame(r.json()['data'])
        df['forecast_text'] = df['forecast'].apply(lambda x: "Current" if int(x) == 0 else "Forecast")
        df['timestamp_hour'] = pd.to_datetime(df['timestamp']).dt.hour
        
    else:
        df = pd.DataFrame(r.json()['currentDay']['data'])
    
    df.to_csv(f'data/raw/environment/{fname}.csv', index=False)