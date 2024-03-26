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
from airflow.decorators import task
from common import execute_query_and_write_to_table

default_args = {
    "owner": "vivek.saini@gmail.com",
    "depends_on_past": False,
    "catchup": False,
}

@dag(schedule="@daily", start_date=datetime(2021, 12, 1), catchup=False)
def sales_populate_datamarts():  
    @task()
    def populate_sales_by_customer():
        #Calculate total sales amount per customer.
        mysql_connection_id = 'mysql_conn'
        query=f"""Select sum(price) as total_sales,name as customer_name,id  from card_service.sales_raw_data_tbl
        group by name,id"""
        execute_query_and_write_to_table(query,'sales_by_customer_tbl',"sales_aggregate",mysql_connection_id)
    @task()
    def populate_average_quality_per_product():
        #Calculate average quality per product.
        mysql_connection_id = 'mysql_conn'
        query=f"""Select AVG(quantity) as averagequantity,product_id  from card_service.sales_raw_data_tbl
            group by product_id """
        execute_query_and_write_to_table(query,'average_quality_per_product_tbl',"sales_aggregate",mysql_connection_id)
    @task()    
    def populate_top5_products_by_sales():
        #Calculate top 5 products by quantity.
        mysql_connection_id = 'mysql_conn'
        query=f"""select product_id  as 'productid',sum(quantity) as 'nooforders' from card_service.sales_raw_data_tbl
            group by product_id order by 2 desc
            limit 5"""
        execute_query_and_write_to_table(query,'top5_products_by_sales_tbl',"sales_aggregate",mysql_connection_id)
    @task()
    def analyse_monthly_sales():
        #Calculate monthly sales.
        mysql_connection_id = 'mysql_conn'
        query="""SELECT 
                    curr.month,
                    curr.monthly_sales,
                    prev.monthly_sales AS prev_monthly_sales,
                    ROUND(((curr.monthly_sales - prev.monthly_sales) / prev.monthly_sales) * 100, 2) AS percentage_change
                FROM
                    (SELECT 
                        DATE_FORMAT(order_date, '%%Y-%%m') AS month,
                        SUM(price) AS monthly_sales
                    FROM
                        card_service.sales_raw_data_tbl
                    GROUP BY month) AS curr
                LEFT JOIN
                    (SELECT 
                        DATE_FORMAT(DATE_SUB(order_date, INTERVAL 1 MONTH), '%%Y-%%m') AS month,
                        SUM(price) AS monthly_sales
                    FROM
                        card_service.sales_raw_data_tbl
                    GROUP BY month) AS prev ON curr.month = prev.month;
            """
        execute_query_and_write_to_table(query,'monthly_sales_tbl',"sales_aggregate",mysql_connection_id)
    populate_sales_by_customer() >> populate_average_quality_per_product() >> populate_top5_products_by_sales() >> analyse_monthly_sales()
sales_populate_datamarts()
    

