FROM quay.io/astronomer/astro-runtime:8.4.0


RUN pip install 'apache-airflow[amazon]'
