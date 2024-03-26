import pandas as pd
import requests
import os
from sqlalchemy import create_engine
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.models import Variable

BASE_DIR = os.path.dirname(__file__)
DQ_DIR = os.path.dirname(BASE_DIR)
mysql_connection_id = 'mysql_conn'


def fetch_weather_data(api_key, lat, lon):
    api_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(api_url)
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        print(f"Failed to fetch weather data for lat={lat}, lon={lon}. Status code: {response.status_code}")
        return None

def get_users_data_from_api():
    users_api_url = 'https://jsonplaceholder.typicode.com/users'
    response = requests.get(users_api_url)
    if response.status_code == 200:
        users_data = response.json()
        extracted_data = []
        for user in users_data:
            user_info = {
                'id': user['id'],
                'name': user['name'],
                'username': user['username'],
                'email': user['email'],
                'latitude': user['address']['geo']['lat'],
                'longitude': user['address']['geo']['lng']
            }
            extracted_data.append(user_info)
        
        return pd.DataFrame(extracted_data)
    else:
        print(f"Failed to fetch user data. Status code: {response.status_code}")
        return None

def get_weather_info(users_sales_data):
    weather_api_key = Variable.get("WEATHER_API_KEY")
    weather_data = fetch_weather_data(weather_api_key, users_sales_data['latitude'], users_sales_data['longitude'])
    if weather_data:
        weather_description = weather_data['weather'][0]['description']
        temp_min = weather_data['main']['temp_min']
        temp_max = weather_data['main']['temp_max']
        wind_speed = weather_data['wind']['speed']
        sunrise = weather_data['sys']['sunrise']
        sunset = weather_data['sys']['sunset']
        return pd.Series({'weather_description': weather_description,
                          'temp_min': temp_min,
                          'temp_max': temp_max,
                          'wind_speed': wind_speed,
                          'sunrise': sunrise,
                          'sunset': sunset})
    else:
        return pd.Series({'weather_description': None,
                          'temp_min': None,
                          'temp_max': None,
                          'wind_speed': None,
                          'sunrise': None,
                          'sunset': None})


def execute_query_and_write_to_table(query, target_table,schema,mysql_connection_id):
    engine = get_engine(mysql_connection_id)
    df = pd.read_sql(query, engine)
    df.to_sql(target_table, engine, if_exists='replace',schema=schema, index=False)


def get_engine(mysql_connection_id):
    conn_hook = MySqlHook.get_hook(mysql_connection_id)
    mysql_url="mysql+mysqldb" + conn_hook.get_uri()[5:]+"?autocommit=true"
    engine = create_engine(mysql_url)
    return engine
