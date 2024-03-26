"""
sales data pipeline

Steps:
1. Read config from airflow 
2. Read Data from CSV
3. Read Users data from API
4. Read Weather data from API
5. Merge Users, Sales data, and weather data and store it in the Raw Layer

"""

from datetime import datetime
from airflow.decorators import dag
import pandas as pd
import requests
from airflow.decorators import task
from common import get_weather_info, get_engine

default_args = {
    "owner": "vivek.saini@gmail.com",
    "depends_on_past": False,
    "catchup": False,
}


@dag(schedule="@daily", start_date=datetime(2021, 12, 1), catchup=False)
def sales_data_pipeline():
    @task()
    def get_sales_data_from_csv():
        csv_file_path = "/usr/local/airflow/dags/AI/sales_data.csv"
        sales_data_df = pd.read_csv(csv_file_path)
        return sales_data_df

    @task()
    def get_users_data_from_api():
        users_api_url = "https://jsonplaceholder.typicode.com/users"
        response = requests.get(users_api_url)
        if response.status_code == 200:
            users_data = response.json()
            extracted_data = []
            for user in users_data:
                user_info = {
                    "id": user["id"],
                    "name": user["name"],
                    "username": user["username"],
                    "email": user["email"],
                    "latitude": user["address"]["geo"]["lat"],
                    "longitude": user["address"]["geo"]["lng"],
                }
                extracted_data.append(user_info)

            return pd.DataFrame(extracted_data)
        else:
            print(f"Failed to fetch user data. Status code: {response.status_code}")
            return None

    @task
    def build_exec_pipeline_sales_data(sales_data_df, users_data_df):
        users_sales_data_df = pd.merge(
            users_data_df, sales_data_df, left_on="id", right_on="customer_id"
        )
        weather_info_df = users_sales_data_df.head(5).apply(get_weather_info, axis=1)
        users_sales_data_df = pd.concat([users_sales_data_df, weather_info_df], axis=1)
        users_sales_data_df["sunrise_time"] = pd.to_datetime(
            users_sales_data_df["sunrise"], unit="s"
        ).dt.time
        users_sales_data_df["sunset_time"] = pd.to_datetime(
            users_sales_data_df["sunset"], unit="s"
        ).dt.time
        users_sales_data_df.drop(columns=["sunrise", "sunset"], inplace=True)
        mysql_connection_id = "mysql_conn"
        engine = get_engine(mysql_connection_id)
        users_sales_data_df.to_sql(
            "sales_raw_data_tbl",
            con=engine,
            schema="sales_raw",
            if_exists="append",
            index=False,
        )

    build_exec_pipeline_sales_data(get_sales_data_from_csv(), get_users_data_from_api())


sales_data_pipeline()
