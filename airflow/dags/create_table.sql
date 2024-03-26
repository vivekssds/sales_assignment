
CREATE TABLE `sales_raw.sales_raw_data_tbl` (
  `sales_id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `id` int DEFAULT NULL,
  `order_id` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `customer_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `price` float DEFAULT NULL,
  `order_date` datetime DEFAULT NULL,
  `weather_description` varchar(500) DEFAULT NULL,
  `temp_min` float DEFAULT NULL,
  `temp_max` float DEFAULT NULL,
  `wind_speed` float DEFAULT NULL,
  `sunrise_time` time DEFAULT NULL,
  `sunset_time` time DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=9001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE `sales_aggregate.monthly_sales_tbl` (
  `monthly_sales_id` INT AUTO_INCREMENT PRIMARY KEY ,
  `month` text,
  `monthly_sales` double DEFAULT NULL,
  `prev_monthly_sales` double DEFAULT NULL,
  `percentage_change` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE IF NOT EXISTS `sales_aggregate.top5_products_by_sales_tbl` (
  `product_sales_id` INT AUTO_INCREMENT PRIMARY KEY ,
  `productid` bigint DEFAULT NULL,
  `nooforders` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE `sales_aggregate.average_quality_per_product_tbl` (
 `id` INT AUTO_INCREMENT PRIMARY KEY ,
  `averagequantity` double DEFAULT NULL,
  `product_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE TABLE `sales_aggregate.sales_by_customer_tbl` (
   `sales_customer_id` INT AUTO_INCREMENT PRIMARY KEY ,
  `total_sales` double DEFAULT NULL,
  `customer_name` text,
  `id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci