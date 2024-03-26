
<!-- ABOUT THE PROJECT -->
## About The Project

Using a docker-compose file, developed a completely dockerized ELT pipeline with MySQL for data storage, Airflow for automation and orchestration

### Built With

Tech Stack used in this project
* [MYSQL](https://dev.mysql.com/doc/)
* [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/)


<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

Make sure you have docker installed on local machine.
* Docker
* DockerCompose
  
### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/pyjavo/update_csv_pipeline
   ```
2. Run (This will create Airflow and MySQL Containers)
   ```sh
    docker-compose up
   ```
3. Exec into MySQL Container 
    ```
    docker exec -it mysql_container_sales

    ```  
4. Connect MySQL
    ```mysql -h 127.0.0.1 -P 3306 -u root -p
    password : root_admin 
    create database sales_raw;
    create database sales_aggregate;
    ```
5. Open Airflow web browser
   ```JS
   Navigate to `http://localhost:8000/` on the browser
   use `airflow` for username
   use `airflow` for password
   ```
6. First Step is to Define Airflow Variables
   ```JS
   Navigate to `http://localhost:8080/` on the browser
   use `airflow` for username
   use `airflow` for password
   from Drop Down click on connections 
   Add connections (Refer to the File /scripts_airflow/init.sh)
   Add variables (Refer to the File /scripts_airflow/init.sh)
   ```

### Documentation
Recommended docstring format is [Google format](https://google.github.io/styleguide/pyguide.html#381-docstrings)

<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: Capture.PNG

