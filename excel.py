import pandas as pd
import sqlite3
import mechanize

# https://www.thepythoncode.com/article/extracting-and-submitting-web-page-forms-in-python
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from urllib.parse import urljoin

# https://www.digitalocean.com/community/tutorials/how-to-scrape-web-pages-with-beautiful-soup-and-python-3
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# http://jonathansoma.com/lede/foundations/classes/friday%20sessions/advanced-scraping-form-submissions-completed/



import requests

# workbook01 = pd.ExcelFile("games.xlsx")

dataframe = pd.read_excel("games.xlsx")

# sheet_names = workbook.sheet_names()

# print(workbook01)

# conn = sqlite3.connect('TestDB1.db')
# c = conn.cursor()

# c.execute('CREATE TABLE CARS (Brand text, Price number)')
# conn.commit()

# #if the count is 1, then table exists
# if c.fetchone()[0]==1 : {
# 	print('Table exists.')
# }

connection = sqlite3.connect("database01.db")

cursor = connection.cursor()

# cursor.execute("CREATE TABLE TOAST (ID number)")

# print(dataframe)

# print(workbook.sheet_names())

# print(dataframe.keys())

# print(connection)

# DataFrame.to_sql(self, name, con, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None, dtype=None, method=None)

dataframe.to_sql("TOAST", con=connection, if_exists="replace", index=True)

# https://data.bls.gov/cgi-bin/cpicalc.pl
# https://www.bls.gov/data/inflation_calculator.htm

# http://toddhayton.com/2014/12/08/form-handling-with-mechanize-and-beautifulsoup/

br = mechanize.Browser()
br.set_handle_robots(False)
br.open("https://data.bls.gov/cgi-bin/cpicalc.pl")

response = br.response()

# URL of the page we just opened
# print(response.geturl())

# # headers
# print(response.info())

# # body
# print(response.read())

# <form method="post" action="/en/search/" id="form1">

# def select_form(form):
#   return form.attrs.get('id', None) == 'form1'

# br.select_form(predicate=select_form)
# br.submit()

# <form action="/cgi-bin/cpicalc.pl" method="get" id="cpi">

def select_form(form):
  return form.attrs.get('id', None) == 'cpi'

br.select_form(predicate=select_form)

br.form["cost1"] = "1000"
br.form["year1"] = ["191301",]
br.form["year2"] = ["202008",]

# print(br.form["cost1"])
# print(br.form["year1"])
# print(br.form["year2"])

submission = br.submit()

# print(submission)


# br.select_form("cpi")

# form["cost1"] = "1000"

# http://jonathansoma.com/lede/foundations/classes/friday%20sessions/advanced-scraping-form-submissions-completed/

# https://www.digitalocean.com/community/tutorials/how-to-scrape-web-pages-with-beautiful-soup-and-python-3
#

# # Collect first page of artists’ list
# page = requests.get('https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ1.htm')

# page = requests.get("https://data.bls.gov/cgi-bin/cpicalc.pl")

page = requests.get("https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1%2C000.00&year1=200001&year2=202009")

# Create a BeautifulSoup object
# soup = BeautifulSoup(page.text, 'html.parser')

soup = BeautifulSoup(page.text, "html.parser")

# # Pull all text from the BodyText div
# artist_name_list = soup.find(class_='BodyText')

# # Pull text from all instances of <a> tag within BodyText div
# artist_name_list_items = artist_name_list.find_all('a')

# print(soup)

# inflation_answer = soup.find("span", id="answer")

# print(inflation_answer.text)

url_test = "https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1%2C000.00&year1=200001&year2=202009"

page2 = requests.get(url_test)

soup = BeautifulSoup(page2.text, "html.parser")

inflation_answer = soup.find("span", id="answer")

print(inflation_answer.text)

