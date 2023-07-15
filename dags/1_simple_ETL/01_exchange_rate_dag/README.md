### Notes:

Since AWS redshift seems not free any more, I only complete my Extract and Load (to S3) steps with airflow. 
But for my previous plan is to load on AWS redshift raw table using SUPER type column, which is a specific type that AWS provides to store JSON data. And then extract the needed information as columns in staging and production tables. 
<img width="1909" alt="Screen Shot 2023-06-11 at 6 30 20 PM" src="https://github.com/MiaooZheng/data_engineering_projects/assets/97005970/43b3fa1d-8eb0-44fa-92af-1d7a78872c49">

And once we make dag active, the daily exchange rate will upload on S3 automatically.
<img width="1631" alt="Screen Shot 2023-06-11 at 6 21 19 PM" src="https://github.com/MiaooZheng/data_engineering_projects/assets/97005970/4c593d3a-da21-41ff-98f9-2c8f7e02ea65">
