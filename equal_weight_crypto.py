import os
import requests

from selenium import webdriver 
from bs4 import BeautifulSoup

driver_dir = os.path.dirname(__file__)
chrome_driver_path = driver_dir + '\\chromedriver.exe'
cryptos_url = 'https://finance.yahoo.com/cryptocurrencies'
# cryptos_url = 'https://www.etoro.com/discover/markets/cryptocurrencies/'

driver = webdriver.Chrome(chrome_driver_path)
driver.implicitly_wait(30)
driver.maximize_window


#driver.get('https://www.google.com/')
driver.get(cryptos_url)
#list_of_cryptos = driver.find_elements_by_class_name("market-list list-views")
list_of_cryptos = driver.find_elements_by_id("screener-results")
html_text = driver.execute_script("return document.documentElement.outerHTML")
#list_of_cryptos = driver.fin
#print(html_text)


#cryptos_url = 'https://www.etoro.com/markets/btc?sort=InstrumentID'
#html_text = requests.get(cryptos_url).text
soup = BeautifulSoup(html_text, 'html.parser')
#soup = BeautifulSoup(html_text)

match = soup.find_all('div', _class = 'market-list list-view')
#match = soup.find_all('div')
#match = soup
#match = list(soup.children)
#match = list(soup.children)[1]
#list_of_cryptos = match
print(match)
