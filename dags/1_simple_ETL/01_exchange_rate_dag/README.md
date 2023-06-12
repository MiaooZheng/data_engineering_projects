### Notes:

Since AWS redshift seems not free any more, I only complete my Extract and Load (to S3) steps with airflow. 
But for my previous plan is to load on AWS redshift raw table using SUPER type column, which is a specific type that AWS provides to store JSON data. And then extract the needed information as columns in staging and production tables. 
