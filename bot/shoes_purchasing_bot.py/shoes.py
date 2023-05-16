from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


# for this project, i'm going to check the availability and buy the shoes on birkenstock website

product_url = 'https://www.birkenstock.com/ca/boston-suede-leather/boston-suede-suedeleather-softfootbed-eva-u_46.html?dwvar_boston-suede-suedeleather-softfootbed-eva-u__46_width=N'

# first step, let's do chromedriver on mac