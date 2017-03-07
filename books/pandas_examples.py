get_ipython().magic('matplotlib inline')
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
plt.rcParams['figure.figsize'] = (15, 5)
broken_df = pd.read_csv('../data/bikes.csv')
broken_df[:3]
fixed_df = pd.read_csv('../data/bikes.csv', sep=';', encoding='latin1', parse_dates=['Date'], dayfirst=True, index_col='Date')
fixed_df[:3]
fixed_df['Berri 1']
fixed_df['Berri 1'].plot()
fixed_df.plot(figsize=(15, 10))
df = pd.read_csv('../data/bikes.csv', sep=';', encoding='latin1', parse_dates=['Date'], dayfirst=True, index_col='Date')
df['Berri 1'].plot()
get_ipython().magic('matplotlib inline')
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.mpl_style', 'default')
pd.set_option('display.width', 5000) 
pd.set_option('display.max_columns', 60)
plt.rcParams['figure.figsize'] = (15, 5)
complaints = pd.read_csv('../data/311-service-requests.csv')
complaints
complaints['Complaint Type']
complaints[:5]
complaints['Complaint Type'][:5]
complaints[:5]['Complaint Type']
complaints[['Complaint Type', 'Borough']]
complaints[['Complaint Type', 'Borough']][:10]
complaints['Complaint Type'].value_counts()
complaint_counts = complaints['Complaint Type'].value_counts()
complaint_counts[:10]
complaint_counts[:10].plot(kind='bar')
get_ipython().magic('matplotlib inline')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
pd.set_option('display.mpl_style', 'default')
plt.rcParams['figure.figsize'] = (15, 5)
pd.set_option('display.width', 5000) 
pd.set_option('display.max_columns', 60)
complaints = pd.read_csv('../data/311-service-requests.csv')
complaints[:5]
noise_complaints = complaints[complaints['Complaint Type'] == "Noise - Street/Sidewalk"]
noise_complaints[:3]
complaints['Complaint Type'] == "Noise - Street/Sidewalk"
is_noise = complaints['Complaint Type'] == "Noise - Street/Sidewalk"
in_brooklyn = complaints['Borough'] == "BROOKLYN"
complaints[is_noise & in_brooklyn][:5]
complaints[is_noise & in_brooklyn][['Complaint Type', 'Borough', 'Created Date', 'Descriptor']][:10]
pd.Series([1,2,3])
np.array([1,2,3])
pd.Series([1,2,3]).values
arr = np.array([1,2,3])
arr != 2
arr[arr != 2]
is_noise = complaints['Complaint Type'] == "Noise - Street/Sidewalk"
noise_complaints = complaints[is_noise]
noise_complaints['Borough'].value_counts()
noise_complaint_counts = noise_complaints['Borough'].value_counts()
complaint_counts = complaints['Borough'].value_counts()
noise_complaint_counts / complaint_counts
noise_complaint_counts / complaint_counts.astype(float)
(noise_complaint_counts / complaint_counts.astype(float)).plot(kind='bar')
get_ipython().magic('matplotlib inline')
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier
plt.rcParams['figure.figsize'] = (15, 5)
plt.rcParams['font.family'] = 'sans-serif'
pd.set_option('display.width', 5000) 
pd.set_option('display.max_columns', 60)
bikes = pd.read_csv('../data/bikes.csv', sep=';', encoding='latin1', parse_dates=['Date'], dayfirst=True, index_col='Date')
bikes['Berri 1'].plot()
berri_bikes = bikes[['Berri 1']].copy()
berri_bikes[:5]
berri_bikes.index
berri_bikes.index.day
berri_bikes.index.weekday
berri_bikes.loc[:,'weekday'] = berri_bikes.index.weekday
berri_bikes[:5]
weekday_counts = berri_bikes.groupby('weekday').aggregate(sum)
weekday_counts
weekday_counts.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_counts
weekday_counts.plot(kind='bar')
bikes = pd.read_csv('../data/bikes.csv', 
sep=';', encoding='latin1', 
parse_dates=['Date'], dayfirst=True, 
index_col='Date')
berri_bikes = bikes[['Berri 1']].copy()
berri_bikes.loc[:,'weekday'] = berri_bikes.index.weekday
weekday_counts = berri_bikes.groupby('weekday').aggregate(sum)
weekday_counts.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_counts.plot(kind='bar')
get_ipython().magic('matplotlib inline')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
pd.set_option('display.mpl_style', 'default')
plt.rcParams['figure.figsize'] = (15, 3)
plt.rcParams['font.family'] = 'sans-serif'
weather_2012_final = pd.read_csv('../data/weather_2012.csv', index_col='Date/Time')
weather_2012_final['Temp (C)'].plot(figsize=(15, 6))
url_template = "http://climate.weather.gc.ca/climateData/bulkdata_e.html?format=csv&stationID=5415&Year={year}&Month={month}&timeframe=1&submit=Download+Data"
url = url_template.format(month=3, year=2012)
weather_mar2012 = pd.read_csv(url, skiprows=15, index_col='Date/Time', parse_dates=True, encoding='latin1', header=True)
weather_mar2012
weather_mar2012[u"Temp (\xc2\xb0C)"].plot(figsize=(15, 5))
weather_mar2012.columns = [
u'Year', u'Month', u'Day', u'Time', u'Data Quality', u'Temp (C)', 
u'Temp Flag', u'Dew Point Temp (C)', u'Dew Point Temp Flag', 
u'Rel Hum (%)', u'Rel Hum Flag', u'Wind Dir (10s deg)', u'Wind Dir Flag', 
u'Wind Spd (km/h)', u'Wind Spd Flag', u'Visibility (km)', u'Visibility Flag',
u'Stn Press (kPa)', u'Stn Press Flag', u'Hmdx', u'Hmdx Flag', u'Wind Chill', 
u'Wind Chill Flag', u'Weather']
weather_mar2012 = weather_mar2012.dropna(axis=1, how='any')
weather_mar2012[:5]
weather_mar2012 = weather_mar2012.drop(['Year', 'Month', 'Day', 'Time', 'Data Quality'], axis=1)
weather_mar2012[:5]
temperatures = weather_mar2012[[u'Temp (C)']].copy()
print(temperatures.head)
temperatures.loc[:,'Hour'] = weather_mar2012.index.hour
temperatures.groupby('Hour').aggregate(np.median).plot()
def download_weather_month(year, month):
if month == 1:
year += 1
url = url_template.format(year=year, month=month)
weather_data = pd.read_csv(url, skiprows=15, index_col='Date/Time', parse_dates=True, header=True)
weather_data = weather_data.dropna(axis=1)
weather_data.columns = [col.replace('\xb0', '') for col in weather_data.columns]
weather_data = weather_data.drop(['Year', 'Day', 'Month', 'Time', 'Data Quality'], axis=1)
return weather_data
download_weather_month(2012, 1)[:5]
data_by_month = [download_weather_month(2012, i) for i in range(1, 13)]
weather_2012 = pd.concat(data_by_month)
weather_2012
weather_2012.to_csv('../data/weather_2012.csv')
get_ipython().magic('matplotlib inline')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
pd.set_option('display.mpl_style', 'default')
plt.rcParams['figure.figsize'] = (15, 3)
plt.rcParams['font.family'] = 'sans-serif'
weather_2012 = pd.read_csv('../data/weather_2012.csv', parse_dates=True, index_col='Date/Time')
weather_2012[:5]
weather_description = weather_2012['Weather']
is_snowing = weather_description.str.contains('Snow')
is_snowing[:5]
is_snowing.plot()
weather_2012['Temp (C)'].resample('M', how=np.median).plot(kind='bar')
is_snowing.astype(float)[:10]
is_snowing.astype(float).resample('M', how=np.mean)
is_snowing.astype(float).resample('M', how=np.mean).plot(kind='bar')
temperature = weather_2012['Temp (C)'].resample('M', how=np.median)
is_snowing = weather_2012['Weather'].str.contains('Snow')
snowiness = is_snowing.astype(float).resample('M', how=np.mean)
temperature.name = "Temperature"
snowiness.name = "Snowiness"
stats = pd.concat([temperature, snowiness], axis=1)
stats
stats.plot(kind='bar')
stats.plot(kind='bar', subplots=True, figsize=(15, 10))
get_ipython().magic('matplotlib inline')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
pd.set_option('display.mpl_style', 'default')
plt.rcParams['figure.figsize'] = (15, 5)
plt.rcParams['font.family'] = 'sans-serif'
pd.set_option('display.width', 5000) 
pd.set_option('display.max_columns', 60)
requests = pd.read_csv('../data/311-service-requests.csv')
requests['Incident Zip'].unique()
na_values = ['NO CLUE', 'N/A', '0']
requests = pd.read_csv('../data/311-service-requests.csv', na_values=na_values, dtype={'Incident Zip': str})
requests['Incident Zip'].unique()
rows_with_dashes = requests['Incident Zip'].str.contains('-').fillna(False)
len(requests[rows_with_dashes])
requests[rows_with_dashes]
long_zip_codes = requests['Incident Zip'].str.len() > 5
requests['Incident Zip'][long_zip_codes].unique()
requests['Incident Zip'] = requests['Incident Zip'].str.slice(0, 5)
requests[requests['Incident Zip'] == '00000']
zero_zips = requests['Incident Zip'] == '00000'
requests.loc[zero_zips, 'Incident Zip'] = np.nan
unique_zips = requests['Incident Zip'].unique()
unique_zips.sort()
unique_zips
zips = requests['Incident Zip']
is_close = zips.str.startswith('0') | zips.str.startswith('1')
is_far = ~(is_close) & zips.notnull()
zips[is_far]
requests[is_far][['Incident Zip', 'Descriptor', 'City']].sort('Incident Zip')
requests['City'].str.upper().value_counts()
na_values = ['NO CLUE', 'N/A', '0']
requests = pd.read_csv('../data/311-service-requests.csv', 
na_values=na_values, 
dtype={'Incident Zip': str})
def fix_zip_codes(zips):
zips = zips.str.slice(0, 5)

zero_zips = zips == '00000'
zips[zero_zips] = np.nan

return zips
requests['Incident Zip'] = fix_zip_codes(requests['Incident Zip'])
requests['Incident Zip'].unique()
import pandas as pd
popcon = pd.read_csv('../data/popularity-contest', sep=' ', )[:-1]
popcon.columns = ['atime', 'ctime', 'package-name', 'mru-program', 'tag']
popcon[:5]
popcon['atime'] = popcon['atime'].astype(int)
popcon['ctime'] = popcon['ctime'].astype(int)
popcon['atime'] = pd.to_datetime(popcon['atime'], unit='s')
popcon['ctime'] = pd.to_datetime(popcon['ctime'], unit='s')
popcon['atime'].dtype
popcon[:5]
popcon = popcon[popcon['atime'] > '1970-01-01']
nonlibraries = popcon[~popcon['package-name'].str.contains('lib')]
nonlibraries.sort('ctime', ascending=False)[:10]
import pandas as pd
import sqlite3
con = sqlite3.connect("../data/weather_2012.sqlite")
df = pd.read_sql("SELECT * from weather_2012 LIMIT 3", con)
df
df = pd.read_sql("SELECT * from weather_2012 LIMIT 3", con, index_col='id')
df
df = pd.read_sql("SELECT * from weather_2012 LIMIT 3", con, 
index_col=['id', 'date_time'])
df
weather_df = pd.read_csv('../data/weather_2012.csv')
con = sqlite3.connect("../data/test_db.sqlite")
con.execute("DROP TABLE IF EXISTS weather_2012")
weather_df.to_sql("weather_2012", con)
con = sqlite3.connect("../data/test_db.sqlite")
df = pd.read_sql("SELECT * from weather_2012 LIMIT 3", con)
df
con = sqlite3.connect("../data/test_db.sqlite")
df = pd.read_sql("SELECT * from weather_2012 ORDER BY Weather LIMIT 3", con)
df
import MySQLdb
con = MySQLdb.connect(host="localhost", db="test")
import psycopg2
con = psycopg2.connect(host="localhost")
