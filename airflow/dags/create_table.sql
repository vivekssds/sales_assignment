CREATE TABLE sales_raw.sales_raw_data_tbl
(
sales_id INT AUTO_INCREMENT PRIMARY KEY,
id INT,
order_id INT,
name VARCHAR(255),
username VARCHAR(255),
email VARCHAR(255),
latitude FLOAT,
longitude FLOAT,
customer_id INT,
product_id INT,
quantity INT,
price FLOAT,
order_date DATETIME,
weather_description VARCHAR(500),
temp_min FLOAT,
temp_max FLOAT,
wind_speed FLOAT,
sunrise_time TIME,
sunset_time TIME 
)