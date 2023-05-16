import requests 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class Linkedin_Search:
    def __init__(self, path):
        self.driver = webdriver.Chrome(path)


    def search_product(self):
        self.driver.get("https://www.linkedin.com/feed/")
        


client = Linkedin_Search(path = "/Users/miaoz/Desktop/github_projects/email_api/checkout_bot/chromedriver")
client.search_product()