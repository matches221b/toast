#
import os
# from flask import Flask, render_template, request
from flask import Flask, flash, jsonify, make_response, redirect, render_template, request, session
# from flask.ext.mobility import Mobility
# from flask_compressor import Mobility
# from flask.ext.mobility import Mobility
# from flask_mobility import Mobility
from flask_mobility import Mobility
# from flask_restful import make_template_fragment_key
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import sqlite3
import pandas as pd
import datetime
from cs50 import SQL
from helpers import months_dict, usd, BeautifulSoup, requests, apology
from urllib.request import urlopen

# import os

# from cs50 import SQL
# from flask import Flask, flash, jsonify, redirect, render_template, request, session
# from flask_session import Session
# from tempfile import mkdtemp
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash

# pip install xlrd

# conda install -c anaconda xlrd

# Configure application
app = Flask(__name__)
Mobility(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# def usd(value):
#     """Format value as USD."""
#     return f"${value:,.2f}"

# dataframe = pd.read_excel("games.xlsx")

dataframe = pd.read_excel("console_info.xlsx")

# connection = sqlite3.connect("database01.db")

connection = sqlite3.connect("database.db")

cursor = connection.cursor()

# dataframe.to_sql("TOAST", con=connection, if_exists="replace", index=True)

dataframe.to_sql("console_info", con=connection, if_exists="replace", index=True)

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///database01.db")

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# db = pd.read_excel("games.xlsx")

# db.head()

# df = pd.read_excel('NameNumbers.xlsx')
# df.head()

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/goodbye")
def bye():

    return "Goodbye!"


@app.route("/laboratory")
def laboratory():

    return render_template("laboratory.html")

# Use the info at the following links to generalize the release price pages to one route
# I.e., get the company name from the URL and use that as the "seed" for the SQL queries
# But this might not work since you are expanding to stuff beyond release prices
# https://stackoverflow.com/questions/35188540/get-a-variable-from-the-url-in-a-flask-route
# https://flask.palletsprojects.com/en/1.1.x/quickstart/#variable-rules

# (0) index
# (1) release prices
# (2) number of units sold
# (3) fun facts

@app.route("/microsoft", methods=["GET", "POST"])
def microsoft():
    """Show information about Microsoft's consoles"""

    # if request.MOBILE == True:
    if request.MOBILE == True:
        mobile = True

    else:
        mobile = False

    # Route for access via GET
    if request.method == "GET":

        console_info = db.execute("SELECT * FROM TOAST WHERE company = :company", company="Microsoft")

        cardinal_numbers = list(range(0,len(console_info)))

        for i in range(0, len(console_info)):

            # Change from zero-index to one-index
            console_info[i]["cardinal_number"] = i + 1

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # date_partially_formatted = datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S")

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Get date completely formatted
            date_completely_formatted = date_partially_formatted.strftime("%A, %B %d, %Y")

            # console_info[i]["usa_release_date"] = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Put completely formatted date in the list of dicts
            console_info[i]["usa_release_date"] = date_completely_formatted

            console_info[i]["formatted_release_price"] = usd(console_info[i]["usa_release_date_usa_price"])

        # Get a dictionary of months of the year (e.g., January:01)
        months = months_dict()

        # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
        years = list(range(1913, 2021))

        # Reverse the order of the list of years
        years.reverse()

        arrival_method = request.method

        return render_template("microsoft.html",
            console_info=console_info,
            months=months,
            years=years,
            arrival_method=arrival_method,
            mobile=mobile)

    # Route for access via POST
    elif request.method == "POST":

        # Get user selected month for inflation calculation
        inflation_month = request.form.get("month")

        if inflation_month == "":
            # Return error message
            return apology("Please select a month for the inflation calculation.")

        # Get user selected year for inflation calculation
        inflation_year = request.form.get("year")

        if inflation_year == "":
            # Return error message
            return apology("Please select a year for the inflation calculation.")

        # Make a datetime object
        inflation_month_short = datetime.datetime.strptime(inflation_month, "%m")

        # Get the short name version of months (e.g., Jan)
        inflation_month_short = inflation_month_short.strftime("%b")

        # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=100.00&year1=200001&year2=202009

        # Get list of dicts containing info from database
        console_info = db.execute("SELECT * FROM TOAST WHERE company = :company", company="Microsoft")

        # Get list of cardinal numbers
        cardinal_numbers = list(range(0,len(console_info)))

        # Get month for inflation adjusted price
        inflation_month = request.form.get("month")

        # Get year for inflation adjusted price
        inflation_year = request.form.get("year")

        # Add key:value pairs the dicts in the list of dicts
        for i in range(0, len(console_info)):

            # Change from zero-index to one-index
            console_info[i]["cardinal_number"] = i + 1

            # Create a dict to how components of the inflation URL
            url_components = {}

            # Add the base of the URL
            url_components["base"] = "https://data.bls.gov/cgi-bin/cpicalc.pl?"

            # Add the cost1 component of the URL
            url_components["cost1"] = "cost1=" + str(console_info[i]["usa_release_date_usa_price"]) + "&"

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            release_year_int = int(date_partially_formatted.strftime("%Y"))

            release_month_int = int(date_partially_formatted.strftime("%m"))

            inflation_answer = ""

            if release_year_int < 2020 or (release_year_int == 2020 and release_month_int <= 9):

                # Add the year1 component of the URL
                url_components["year1"] = "year1=" + date_partially_formatted.strftime("%Y") + date_partially_formatted.strftime("%m") + "&"

                # Add the year2 component of th URL
                url_components["year2"] = "year2=" + inflation_year + inflation_month

                # Convert the dict values to a list
                url_components_list = list(url_components.values())

                # Convert the list items to a single string
                url_string = "".join(url_components_list)

                 # # The get() method returns a requests.Response object
                inflation_answer_page = requests.get(url_string)

                # Get a BeautifulSoup object
                soup = BeautifulSoup(inflation_answer_page.text, "html.parser")

                inflation_answer_with_tags = soup.find("span", id="answer")

                inflation_answer = inflation_answer_with_tags.text

                console_info[i]["inflation_answer"] = inflation_answer_with_tags.text

            else:
                inflatio_answer_with_tags = "Not Available"

                inflation_answer = "Not Available"

                console_info[i]["inflation_answer"] = inflation_answer

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Get date completely formatted
            date_completely_formatted = date_partially_formatted.strftime("%A, %B %d, %Y")

            # Get date's year in YYYY format (e.g., 1986) for inflation calculation
            release_year = date_partially_formatted.strftime("%Y")

            # Get date's year in mm format (e.g., 10 is October) for inflation calculation
            release_month = date_partially_formatted.strftime("%m")

            # Put completely formatted date in the list of dicts
            console_info[i]["usa_release_date"] = date_completely_formatted

            # Get a formatted version of the United States release price
            console_info[i]["formatted_release_price"] = usd(console_info[i]["usa_release_date_usa_price"])

            #####################
            #                   #
            #  End of for loop  #
            #                   #
            #####################

        #############################################################################################################
        # Insert the url_string into what you created in excel.py                                                   #
        # page = requests.get("https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1%2C000.00&year1=200001&year2=202009") #
        #############################################################################################################

        # Get a dictionary of months of the year (e.g., January:01)
        months = months_dict()

        # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
        years = list(range(1913, 2021))

        # Reverse the order of the list of years
        years.reverse()

        arrival_method = request.method

        return render_template("microsoft.html",
            console_info=console_info,
            months=months,
            years=years,
            arrival_method=arrival_method,
            inflation_month=inflation_month,
            inflation_year=inflation_year,
            inflation_month_short=inflation_month_short,
            url_components=url_components,
            url_components_list=url_components_list,
            url_string=url_string,
            inflation_answer_page=inflation_answer_page,
            soup=soup,
            inflation_answer_with_tags=inflation_answer_with_tags,
            inflation_answer=inflation_answer,
            mobile=mobile)
            # date_year=date_year,
            # url_components=url_components,
            # url_components_list=url_components_list,
            # url_string=url_string,
            # inflation_answer=inflation_answer)


    # # Route for access via GET
    # if request.method == "GET":

    #     # microsoft_dict = db.execute("SELECT Console_Name, United_States_Release_Date, \
    #     #                             United_States_Release_Date_Price_(USD), Gaming_Generation, \
    #     #                             Company")

    #     microsoft_info = db.execute("SELECT * FROM TOAST WHERE company = :company", company="Microsoft")

    #     cardinal_numbers = list(range(0,len(microsoft_info)))

    #     for i in range(0, len(microsoft_info)):

    #         # Change from zero-index to one-index
    #         microsoft_info[i]["cardinal_number"] = i + 1

    #         # Get date unformatted
    #         date_unformatted = microsoft_info[i]["usa_release_date"]

    #         # date_partially_formatted = datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S")

    #         # Get date partially formatted
    #         date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

    #         # Get date completely formatted
    #         date_completely_formatted = date_partially_formatted.strftime("%A, %B %d, %Y")

    #         # microsoft_info[i]["usa_release_date"] = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

    #         # Put completely formatted date in the list of dicts
    #         microsoft_info[i]["usa_release_date"] = date_completely_formatted

    #         microsoft_info[i]["formatted_release_price"] = usd(microsoft_info[i]["usa_release_date_usa_price"])

    #     # Get a dictionary of months of the year (e.g., January:01)
    #     months = months_dict()

    #     # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
    #     years = list(range(1913, 2021))

    #     # Reverse the order of the list of years
    #     years.reverse()

    #     arrival_method = request.method

    #     return render_template("microsoft.html",
    #         microsoft_info=microsoft_info,
    #         months=months,
    #         years=years,
    #         arrival_method=arrival_method)

    # # Route for access via POST
    # elif request.method == "POST":

    #     # Get user selected month for inflation calculation
    #     inflation_month = request.form.get("month")

    #     if inflation_month == "":
    #         # Return error message
    #         return apology("Please select a month for the inflation calculation.")

    #     # Get user selected year for inflation calculation
    #     inflation_year = request.form.get("year")

    #     if inflation_year == "":
    #         # Return error message
    #         return apology("Please select a year for the inflation calculation.")

    #     # Make a datetime object
    #     inflation_month_short = datetime.datetime.strptime(inflation_month, "%m")

    #     # Get the short name version of months (e.g., Jan)
    #     inflation_month_short = inflation_month_short.strftime("%b")

    #     # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=100.00&year1=200001&year2=202009

    #     # Get list of dicts containing info from database
    #     microsoft_info = db.execute("SELECT * FROM TOAST WHERE company = :company", company="Microsoft")

    #     # Get list of cardinal numbers
    #     cardinal_numbers = list(range(0,len(microsoft_info)))

    #     # Get month for inflation adjusted price
    #     inflation_month = request.form.get("month")

    #     # Get year for inflation adjusted price
    #     inflation_year = request.form.get("year")

    #     # # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=100.00&year1=200001&year2=202009

    #     # # Create a dict to how components of the inflation URL
    #     # url_components = {}

    #     # # Add the base of the URL
    #     # url_components["base"] = "https://data.bls.gov/cgi-bin/cpicalc.pl?"

    #     # # Add the cost1 component of the URL
    #     # url_components["cost1"] = "cost1=" + str(microsoft_info[0]["usa_release_date_usa_price"]) + "&"

    #     # # Get date unformatted
    #     # date_unformatted = microsoft_info[0]["usa_release_date"]

    #     # # Get date partially formatted
    #     # date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

    #     # # Add the year1 component of the URL
    #     # url_components["year1"] = "year1=" + date_partially_formatted.strftime("%Y") + date_partially_formatted.strftime("%m") + "&"

    #     # # Add the year2 component of th URL
    #     # url_components["year2"] = "year2=" + inflation_year + inflation_month

    #     # # Convert the dict values to a list
    #     # url_components_list = list(url_components.values())

    #     # # Convert the list items to a single string
    #     # url_string = "".join(url_components_list)

    #     # # The get() method returns a requests.Response object
    #     # inflation_answer_page = requests.get(url_string)

    #     # # Get a BeautifulSoup object
    #     # soup = BeautifulSoup(inflation_answer_page.text, "html.parser")

    #     # # Find the answer in the soup
    #     # inflation_answer_with_tags = soup.find("span", id="answer")

    #     # # Remove the tags from the answer
    #     # inflation_answer = inflation_answer_with_tags.text

    #     # inflation_answer = soup.find("span", id="answer")

    #     # # list(dictionary.values())

    #     # url_components_list = list(url_components.values())

    #     # url_string = "".join(url_components_list)

    #     # inflation_answer_page = requests.get(url_string)

    #     # soup = BeautifulSoup(inflation_answer_page.text, "html.parser")

    #     # inflation_answer = soup.find("span", id="answer")

    #     # inflation_answer = inflation_answer.text


    #     # Add key:value pairs the dicts in the list of dicts
    #     for i in range(0, len(microsoft_info)):

    #         # Change from zero-index to one-index
    #         microsoft_info[i]["cardinal_number"] = i + 1

    #         # Create a dict to how components of the inflation URL
    #         url_components = {}

    #         # Add the base of the URL
    #         url_components["base"] = "https://data.bls.gov/cgi-bin/cpicalc.pl?"

    #         # Add the cost1 component of the URL
    #         url_components["cost1"] = "cost1=" + str(microsoft_info[i]["usa_release_date_usa_price"]) + "&"

    #         # Get date unformatted
    #         date_unformatted = microsoft_info[i]["usa_release_date"]

    #         # Get date partially formatted
    #         date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

    #         release_year_int = int(date_partially_formatted.strftime("%Y"))

    #         release_month_int = int(date_partially_formatted.strftime("%m"))

    #         inflation_answer = ""

    #         if release_year_int < 2020 or (release_year_int == 2020 and release_month_int <= 9):

    #             # Add the year1 component of the URL
    #             url_components["year1"] = "year1=" + date_partially_formatted.strftime("%Y") + date_partially_formatted.strftime("%m") + "&"

    #             # Add the year2 component of th URL
    #             url_components["year2"] = "year2=" + inflation_year + inflation_month

    #             # Convert the dict values to a list
    #             url_components_list = list(url_components.values())

    #             # Convert the list items to a single string
    #             url_string = "".join(url_components_list)

    #              # # The get() method returns a requests.Response object
    #             inflation_answer_page = requests.get(url_string)

    #             # Get a BeautifulSoup object
    #             soup = BeautifulSoup(inflation_answer_page.text, "html.parser")

    #             inflation_answer_with_tags = soup.find("span", id="answer")

    #             inflation_answer = inflation_answer_with_tags.text

    #             microsoft_info[i]["inflation_answer"] = inflation_answer_with_tags.text

    #         else:
    #             inflatio_answer_with_tags = "Not Available"

    #             inflation_answer = "Not Available"

    #             microsoft_info[i]["inflation_answer"] = inflation_answer



    #         # Get date unformatted
    #         date_unformatted = microsoft_info[i]["usa_release_date"]

    #         # Get date partially formatted
    #         date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

    #         # Get date completely formatted
    #         date_completely_formatted = date_partially_formatted.strftime("%A, %B %d, %Y")

    #         # Get date's year in YYYY format (e.g., 1986) for inflation calculation
    #         release_year = date_partially_formatted.strftime("%Y")

    #         # Get date's year in mm format (e.g., 10 is October) for inflation calculation
    #         release_month = date_partially_formatted.strftime("%m")

    #         # Put completely formatted date in the list of dicts
    #         microsoft_info[i]["usa_release_date"] = date_completely_formatted

    #         # Get a formatted version of the United States release price
    #         microsoft_info[i]["formatted_release_price"] = usd(microsoft_info[i]["usa_release_date_usa_price"])

    #         #####################
    #         #                   #
    #         #  End of for loop  #
    #         #                   #
    #         #####################

    #     #############################################################################################################
    #     # Insert the url_string into what you created in excel.py                                                   #
    #     # page = requests.get("https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1%2C000.00&year1=200001&year2=202009") #
    #     #############################################################################################################

    #     # Get a dictionary of months of the year (e.g., January:01)
    #     months = months_dict()

    #     # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
    #     years = list(range(1913, 2021))

    #     # Reverse the order of the list of years
    #     years.reverse()

    #     arrival_method = request.method

    #     return render_template("microsoft.html",
    #         microsoft_info=microsoft_info,
    #         months=months,
    #         years=years,
    #         arrival_method=arrival_method,
    #         inflation_month=inflation_month,
    #         inflation_year=inflation_year,
    #         inflation_month_short=inflation_month_short,
    #         url_components=url_components,
    #         url_components_list=url_components_list,
    #         url_string=url_string,
    #         inflation_answer_page=inflation_answer_page,
    #         soup=soup,
    #         inflation_answer_with_tags=inflation_answer_with_tags,
    #         inflation_answer=inflation_answer)
    #         # date_year=date_year,
    #         # url_components=url_components,
    #         # url_components_list=url_components_list,
    #         # url_string=url_string,
    #         # inflation_answer=inflation_answer)

@app.route("/nintendo", methods=["GET", "POST"])
def nintendo():
    """Show information about Nintendo's consoles"""

    # if request.MOBILE == True:
    if request.MOBILE == True:
        mobile = True

    else:
        mobile = False

    # Route for access via GET
    if request.method == "GET":

        # console_info = db.execute("SELECT * FROM TOAST WHERE company = :company", company="Nintendo")

        console_info = db.execute("SELECT * FROM console_info WHERE company = :company", company="Nintendo")

        cardinal_numbers = list(range(0,len(console_info)))

        for i in range(0, len(console_info)):

            # Change from zero-index to one-index
            console_info[i]["cardinal_number"] = i + 1

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # date_partially_formatted = datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S")

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Get date completely formatted
            date_completely_formatted = date_partially_formatted.strftime("%A, %B %d, %Y")

            # console_info[i]["usa_release_date"] = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Put completely formatted date in the list of dicts
            console_info[i]["usa_release_date"] = date_completely_formatted

            console_info[i]["formatted_release_price"] = usd(console_info[i]["usa_release_date_usa_price"])

        console_company = console_info[0]["company"].lower()

        # Get a dictionary of months of the year (e.g., January:01)
        months = months_dict()

        # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
        years = list(range(1913, 2021))

        # Reverse the order of the list of years
        years.reverse()

        arrival_method = request.method

        return render_template("nintendo.html",
            console_info=console_info,
            months=months,
            years=years,
            arrival_method=arrival_method,
            mobile=mobile,
            console_company=console_company)

    # Route for access via POST
    elif request.method == "POST":

        # Get user selected month for inflation calculation
        inflation_month = request.form.get("month")

        if inflation_month == "":
            # Return error message
            return apology("Please select a month for the inflation calculation.")

        # Get user selected year for inflation calculation
        inflation_year = request.form.get("year")

        if inflation_year == "":
            # Return error message
            return apology("Please select a year for the inflation calculation.")

        # Make a datetime object
        inflation_month_short = datetime.datetime.strptime(inflation_month, "%m")

        # Get the short name version of months (e.g., Jan)
        inflation_month_short = inflation_month_short.strftime("%b")

        # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=100.00&year1=200001&year2=202009

        # Get list of dicts containing info from database
        console_info = db.execute("SELECT * FROM TOAST WHERE company = :company", company="Nintendo")

        # Get list of cardinal numbers
        cardinal_numbers = list(range(0,len(console_info)))

        # Get month for inflation adjusted price
        inflation_month = request.form.get("month")

        # Get year for inflation adjusted price
        inflation_year = request.form.get("year")

        # Add key:value pairs the dicts in the list of dicts
        for i in range(0, len(console_info)):

            # Change from zero-index to one-index
            console_info[i]["cardinal_number"] = i + 1

            # Create a dict to how components of the inflation URL
            url_components = {}

            # Add the base of the URL
            url_components["base"] = "https://data.bls.gov/cgi-bin/cpicalc.pl?"

            # Add the cost1 component of the URL
            url_components["cost1"] = "cost1=" + str(console_info[i]["usa_release_date_usa_price"]) + "&"

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            release_year_int = int(date_partially_formatted.strftime("%Y"))

            release_month_int = int(date_partially_formatted.strftime("%m"))

            inflation_answer = ""

            if release_year_int < 2020 or (release_year_int == 2020 and release_month_int <= 9):

                # Add the year1 component of the URL
                url_components["year1"] = "year1=" + date_partially_formatted.strftime("%Y") + date_partially_formatted.strftime("%m") + "&"

                # Add the year2 component of th URL
                url_components["year2"] = "year2=" + inflation_year + inflation_month

                # Convert the dict values to a list
                url_components_list = list(url_components.values())

                # Convert the list items to a single string
                url_string = "".join(url_components_list)

                 # # The get() method returns a requests.Response object
                inflation_answer_page = requests.get(url_string)

                # Get a BeautifulSoup object
                soup = BeautifulSoup(inflation_answer_page.text, "html.parser")

                inflation_answer_with_tags = soup.find("span", id="answer")

                inflation_answer = inflation_answer_with_tags.text

                console_info[i]["inflation_answer"] = inflation_answer_with_tags.text

            else:
                inflatio_answer_with_tags = "Not Available"

                inflation_answer = "Not Available"

                console_info[i]["inflation_answer"] = inflation_answer

            console_company = console_info[0]["company"].lower()

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Get date completely formatted
            date_completely_formatted = date_partially_formatted.strftime("%A, %B %d, %Y")

            # Get date's year in YYYY format (e.g., 1986) for inflation calculation
            release_year = date_partially_formatted.strftime("%Y")

            # Get date's year in mm format (e.g., 10 is October) for inflation calculation
            release_month = date_partially_formatted.strftime("%m")

            # Put completely formatted date in the list of dicts
            console_info[i]["usa_release_date"] = date_completely_formatted

            # Get a formatted version of the United States release price
            console_info[i]["formatted_release_price"] = usd(console_info[i]["usa_release_date_usa_price"])

            #####################
            #                   #
            #  End of for loop  #
            #                   #
            #####################

        #############################################################################################################
        # Insert the url_string into what you created in excel.py                                                   #
        # page = requests.get("https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1%2C000.00&year1=200001&year2=202009") #
        #############################################################################################################

        # Get a dictionary of months of the year (e.g., January:01)
        months = months_dict()

        # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
        years = list(range(1913, 2021))

        # Reverse the order of the list of years
        years.reverse()

        arrival_method = request.method

        return render_template("nintendo.html",
            console_info=console_info,
            months=months,
            years=years,
            arrival_method=arrival_method,
            inflation_month=inflation_month,
            inflation_year=inflation_year,
            inflation_month_short=inflation_month_short,
            url_components=url_components,
            url_components_list=url_components_list,
            url_string=url_string,
            inflation_answer_page=inflation_answer_page,
            soup=soup,
            inflation_answer_with_tags=inflation_answer_with_tags,
            inflation_answer=inflation_answer,
            mobile=mobile,
            console_company=console_company)
            # date_year=date_year,
            # url_components=url_components,
            # url_components_list=url_components_list,
            # url_string=url_string,
            # inflation_answer=inflation_answer)

@app.route("/sony", methods=["GET", "POST"])
def sony():

    return render_template("sony.html")

@app.route("/sega", methods=["GET", "POST"])
def sega():

    return render_template("sega.html")

@app.route("/toast_test", methods=["GET", "POST"])
def toast_test():

    return apology("For the number of shares to buy, please enter a non-zero positive integer.", 403)

    # return render_template("toast.html")

# Use the info at the following links to generalize the release price pages to one route
# I.e., get the company name from the URL and use that as the "seed" for the SQL queries
# But this might not work since you are expanding to stuff beyond release prices
# https://stackoverflow.com/questions/35188540/get-a-variable-from-the-url-in-a-flask-route
# https://flask.palletsprojects.com/en/1.1.x/quickstart/#variable-rules

# (0) index
# (1) release prices
# (2) number of units sold
# (3) fun facts



# @app.route("/release_prices/", methods=["GET", "POST"])
# def release_prices():

#     return redirect("/release_prices/all")

@app.route("/release_prices/<company>", methods=["GET", "POST"])
def release_prices_by_company(company):

    # Put user input in lowercase
    company = company.lower()

    # Get list of dictionaries that has each unique company's name
    database_companies = db.execute("SELECT DISTINCT company FROM console_info")

    # Put unique company names in a list
    permissible_companies = [dictionary["company"] for dictionary in database_companies]

    # Add "all" to the permissible companies list
    permissible_companies.append("all")

    # Put all list items in lowercase
    permissible_companies = [item.lower() for item in permissible_companies]

    # Check validity of input
    if company not in permissible_companies:

        # Return an error for invalid input
        return apology("That is not a valid company.", 403)

    # Check whether user is accessing route via a mobile device
    if request.MOBILE == True:

        # Set mobile to True if user is using a mobile device
        mobile = True

    else:

        # Set mobile to False if user is not using a mobile device
        mobile = False

    # Empty list that will eventually hold info to display on webpage
    console_info = []

    # If user accesses route via GET
    if request.method == "GET":

        # If user wants info on all of the consoles
        if company == "all":

            # Get info from database and put it in a list
            console_info = db.execute("\
                SELECT console_name, usa_release_date, usa_release_date_usa_price, gaming_generation, company \
                FROM console_info")

        # If user wants info about a specific company's console
        else:

            # Get info from database and put it in a list
            console_info = db.execute("\
                SELECT console_name, usa_release_date, usa_release_date_usa_price, gaming_generation, company \
                FROM console_info \
                WHERE company = :company", company=company.capitalize())

        # Get a list of cardinal numbers for the table
        cardinal_numbers = list(range(0,len(console_info)))

        # Get a dictionary of months of the year (e.g., January:01)
        months = months_dict()

        # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
        years = list(range(1913, 2021))

        # Reverse the order of the list of years
        years.reverse()


        ######################################################
        # Begin for loop for populating list of dictionaries #
        ######################################################

        for i in range(0, len(console_info)):

            # Change from zero-index to one-index
            console_info[i]["cardinal_number"] = i + 1

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Put completely formatted date in the list of dicts
            console_info[i]["usa_release_date"] = date_partially_formatted.strftime("%B %d, %Y")

            # Put formated release prices in the list of dicts
            console_info[i]["formatted_release_price"] = usd(console_info[i]["usa_release_date_usa_price"])

        ####################################################
        # End for loop for populating list of dictionaries #
        ####################################################

        # Tell the route what to output
        return render_template("release_prices.html",
            cardinal_numbers=cardinal_numbers,
            arrival_method=request.method,
            months=months,
            years=years,
            company=company,
            company_uppercase=company.capitalize(),
            console_info=console_info)

    # If user accesses route via POST
    elif request.method == "POST":

        # Get user selected month for inflation calculation
        inflation_month = request.form.get("month")

        if inflation_month == "":

            # Return error message
            return apology("Please select a month for the inflation calculation.")

        # Get user selected year for inflation calculation
        inflation_year = request.form.get("year")

        if inflation_year == "":

            # Return error message
            return apology("Please select a year for the inflation calculation.")

        return "POST"

@app.route("/console_release_prices_mk_000", methods=["GET", "POST"])
def console_release_prices_mk_000():

    # Check whether user is accessing route via a mobile device
    if request.MOBILE == True:

        # Set mobile to True if user is using a mobile device
        mobile = True

    else:

        # Set mobile to False if user is not using a mobile device
        mobile = False

    # Empty list that will eventually hold info to display on webpage
    console_info = []

    # If user accesses route via GET
    if request.method == "GET":

        # Get put each database row in a dict and put each dict in a list of dicts
        console_info = db.execute("\
            SELECT console_name, usa_release_date, usa_release_date_usa_price, gaming_generation, company \
            FROM console_info")

        # Get a list of cardinal numbers for the table
        cardinal_numbers = list(range(0,len(console_info)))

        # Get a dictionary of months of the year (e.g., January:01)
        months = months_dict()

        # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
        years = list(range(1913, 2021))

        # Reverse the order of the list of years
        years.reverse()

        ######################################################
        # Begin for loop for populating list of dictionaries #
        ######################################################

        # iterate over each dictionary in the list of dictionaries
        for i in range(0, len(console_info)):

            # Change from zero-index to one-index
            console_info[i]["cardinal_number"] = i + 1

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Put completely formatted date in the list of dicts
            console_info[i]["usa_release_date"] = date_partially_formatted.strftime("%B %d, %Y")

            # Put formated release prices in the list of dicts
            console_info[i]["formatted_release_price"] = usd(console_info[i]["usa_release_date_usa_price"])

            # Store a version of the console name with underscores substituted for spaces
            temporary_storage = console_info[i]["console_name"]

            console_info[i]["console_name_underscored"] = temporary_storage.replace(" ", "_")

        ####################################################
        # End for loop for populating list of dictionaries #
        ####################################################

        # Tell the route what to output
        return render_template("console_release_prices.html",
            cardinal_numbers=cardinal_numbers,
            arrival_method=request.method,
            months=months,
            years=years,
            console_info=console_info)

    # If user accesses route via POST
    elif request.method == "POST":

        # Get user selected month for inflation calculation
        inflation_month = request.form.get("month")

        if inflation_month == "":

            # Return error message
            return apology("Please select a month for the inflation calculation.")

        # Make a datetime object from the inflation month
        inflation_month_short = datetime.datetime.strptime(inflation_month, "%m")

        # Get the short name version of months (e.g., Jan)
        inflation_month_short = inflation_month_short.strftime("%b")

        # Get user selected year for inflation calculation
        inflation_year = request.form.get("year")

        if inflation_year == "":

            # Return error message
            return apology("Please select a year for the inflation calculation.")

        # Get put each database row in a dict and put each dict in a list of dicts
        console_info = db.execute("\
            SELECT console_name, usa_release_date, usa_release_date_usa_price, gaming_generation, company \
            FROM console_info")

        # Add key:value pairs the dicts in the list of dicts
        for i in range(0, len(console_info)):

            # Change from zero-index to one-index
            console_info[i]["cardinal_number"] = i + 1

            # Create a dict to how components of the inflation URL
            url_components = {}

            # Add the base of the URL
            url_components["base"] = "https://data.bls.gov/cgi-bin/cpicalc.pl?"

            # Add the cost1 component of the URL
            url_components["cost1"] = "cost1=" + str(console_info[i]["usa_release_date_usa_price"]) + "&"

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Transform the release year into an integer
            release_year_int = int(date_partially_formatted.strftime("%Y"))

            # Transfor the release month into an integer
            release_month_int = int(date_partially_formatted.strftime("%m"))

            # Create a variable to hold the inflation adjusted price
            inflation_answer = ""

            # Get current month as an int (e.g., November would be 11)
            current_month = datetime.datetime.now().month

            # Get current year as an int (e.g., 2019 would be 2019)
            current_year = datetime.datetime.now().year

            # Get the release price adjusted for inflation
            # if int(inflation_year) < current_year or (int(inflation_year) == 2020 and int(inflation_month) < current_month):
            if release_year_int < current_year or (release_year_int == current_year and release_month_int < current_month):

                if int(inflation_year) < current_year or (int(inflation_year) == current_year and int(inflation_month) < current_month):

                    # Add the year1 component of the URL
                    url_components["year1"] = "year1=" + date_partially_formatted.strftime("%Y") + date_partially_formatted.strftime("%m") + "&"

                    # Add the year2 component of th URL
                    url_components["year2"] = "year2=" + inflation_year + inflation_month

                    # Convert the dict values to a list
                    url_components_list = list(url_components.values())

                    # Convert the list items to a single string
                    url_string = "".join(url_components_list)

                    # The get() method returns a requests.Response object
                    inflation_answer_page = requests.get(url_string)

                    # Get a BeautifulSoup object
                    soup = BeautifulSoup(inflation_answer_page.text, "html.parser")

                    # Search the soup for the inflation adjusted price
                    inflation_answer_with_tags = soup.find("span", id="answer")

                    # Put the release price (adjusted for inflation) in the dictionary
                    console_info[i]["inflation_answer"] = inflation_answer_with_tags.text

                # Scenario for inflation price data is unavailable
                else:

                    # Put the data-is-unavailabe message in the dictionary
                    console_info[i]["inflation_answer"] = "Not Available"

            # Scenario for when inflation price data is unavailable
            else:

                # Put the data-is-unavailabe message in the dictionary
                console_info[i]["inflation_answer"] = "Not Available"

            #
            console_company = console_info[0]["company"].lower()

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Get date completely formatted
            date_completely_formatted = date_partially_formatted.strftime("%A, %B %d, %Y")

            # Get date's year in YYYY format (e.g., 1986) for inflation calculation
            release_year = date_partially_formatted.strftime("%Y")

            # Get date's year in mm format (e.g., 10 is October) for inflation calculation
            release_month = date_partially_formatted.strftime("%m")

            # Put completely formatted date in the list of dicts
            console_info[i]["usa_release_date"] = date_completely_formatted

            # Get a formatted version of the United States release price
            console_info[i]["formatted_release_price"] = usd(console_info[i]["usa_release_date_usa_price"])

            ##############################################################################
            #                                                                            #
            #  End of for loop for adding information to the dicts in the list of dicts  #
            #                                                                            #
            ##############################################################################

        # Get a list of cardinal numbers for the table
        cardinal_numbers = list(range(0,len(console_info)))

        # Get a dictionary of months of the year (e.g., January:01)
        months = months_dict()

        # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
        years = list(range(1913, 2021))

        # Reverse the order of the list of years
        years.reverse()

        # Tell the route what to output
        return render_template("console_release_prices.html",
            arrival_method=request.method,
            cardinal_numbers=cardinal_numbers,
            console_info=console_info,
            inflation_month_short=inflation_month_short,
            inflation_year=inflation_year,
            months=months,
            years=years)

        return "POST"

@app.route("/console_release_prices", methods=["GET", "POST"])
def console_release_prices():

    # Check whether user is accessing route via a mobile device
    if request.MOBILE == True:

        # Set mobile to True if user is using a mobile device
        mobile = True

    else:

        # Set mobile to False if user is not using a mobile device
        mobile = False

    # Empty list that will eventually hold info to display on webpage
    console_info = []

    # If user accesses route via GET
    if request.method == "GET":

        # Get put each database row in a dict and put each dict in a list of dicts
        console_info = db.execute("\
            SELECT console_name, usa_release_date, usa_release_date_usa_price, gaming_generation, company \
            FROM console_info")

        # Get a list of cardinal numbers for the table
        cardinal_numbers = list(range(0,len(console_info)))

        # Get a dictionary of months of the year (e.g., January:01)
        months = months_dict()

        # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
        years = list(range(1913, 2021))

        # Reverse the order of the list of years
        years.reverse()

        ######################################################
        # Begin for loop for populating list of dictionaries #
        ######################################################

        # iterate over each dictionary in the list of dictionaries
        for i in range(0, len(console_info)):

            # Change from zero-index to one-index
            console_info[i]["cardinal_number"] = i + 1

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Put completely formatted date in the list of dicts
            console_info[i]["usa_release_date"] = date_partially_formatted.strftime("%B %d, %Y")

            # Put formated release prices in the list of dicts
            console_info[i]["formatted_release_price"] = usd(console_info[i]["usa_release_date_usa_price"])

            # Store a version of the console name with underscores substituted for spaces
            temporary_storage = console_info[i]["console_name"]

            console_info[i]["console_name_underscored"] = temporary_storage.replace(" ", "_")

        ####################################################
        # End for loop for populating list of dictionaries #
        ####################################################

        # Tell the route what to output
        return render_template("console_release_prices.html",
            cardinal_numbers=cardinal_numbers,
            arrival_method=request.method,
            months=months,
            years=years,
            console_info=console_info)

    # If user accesses route via POST
    elif request.method == "POST":

        # Get user selected month for inflation calculation
        inflation_month = request.form.get("month")

        if inflation_month == "":

            # Return error message
            return apology("Please select a month for the inflation calculation.")

        # Make a datetime object from the inflation month
        inflation_month_short = datetime.datetime.strptime(inflation_month, "%m")

        # Get the short name version of months (e.g., Jan)
        inflation_month_short = inflation_month_short.strftime("%b")

        # Get user selected year for inflation calculation
        inflation_year = request.form.get("year")

        if inflation_year == "":

            # Return error message
            return apology("Please select a year for the inflation calculation.")

        # Get put each database row in a dict and put each dict in a list of dicts
        console_info = db.execute("\
            SELECT console_name, usa_release_date, usa_release_date_usa_price, gaming_generation, company \
            FROM console_info")

        # Add key:value pairs the dicts in the list of dicts
        for i in range(0, len(console_info)):

            # Change from zero-index to one-index
            console_info[i]["cardinal_number"] = i + 1

            # Create a dict to how components of the inflation URL
            url_components = {}

            # Add the base of the URL
            url_components["base"] = "https://data.bls.gov/cgi-bin/cpicalc.pl?"

            # Add the cost1 component of the URL
            url_components["cost1"] = "cost1=" + str(console_info[i]["usa_release_date_usa_price"]) + "&"

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Transform the release year into an integer
            release_year_int = int(date_partially_formatted.strftime("%Y"))

            # Transfor the release month into an integer
            release_month_int = int(date_partially_formatted.strftime("%m"))

            # Create a variable to hold the inflation adjusted price
            inflation_answer = ""

            # Get current month as an int (e.g., November would be 11)
            current_month = datetime.datetime.now().month

            # Get current year as an int (e.g., 2019 would be 2019)
            current_year = datetime.datetime.now().year

            # Get the release price adjusted for inflation
            # if int(inflation_year) < current_year or (int(inflation_year) == 2020 and int(inflation_month) < current_month):
            if release_year_int < current_year or (release_year_int == current_year and release_month_int < current_month):

                if int(inflation_year) < current_year or (int(inflation_year) == current_year and int(inflation_month) < current_month):

                    # Add the year1 component of the URL
                    url_components["year1"] = "year1=" + date_partially_formatted.strftime("%Y") + date_partially_formatted.strftime("%m") + "&"

                    # Add the year2 component of th URL
                    url_components["year2"] = "year2=" + inflation_year + inflation_month

                    # Convert the dict values to a list
                    url_components_list = list(url_components.values())

                    # Convert the list items to a single string
                    url_string = "".join(url_components_list)

                    # The get() method returns a requests.Response object
                    inflation_answer_page = requests.get(url_string)

                    # Get a BeautifulSoup object
                    soup = BeautifulSoup(inflation_answer_page.text, "html.parser")

                    # Search the soup for the inflation adjusted price
                    inflation_answer_with_tags = soup.find("span", id="answer")

                    # Put the release price (adjusted for inflation) in the dictionary
                    console_info[i]["inflation_answer"] = inflation_answer_with_tags.text

                # Scenario for inflation price data is unavailable
                else:

                    # Put the data-is-unavailabe message in the dictionary
                    console_info[i]["inflation_answer"] = "Not Available"

            # Scenario for when inflation price data is unavailable
            else:

                # Put the data-is-unavailabe message in the dictionary
                console_info[i]["inflation_answer"] = "Not Available"

            #
            console_company = console_info[0]["company"].lower()

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Get date completely formatted
            date_completely_formatted = date_partially_formatted.strftime("%A, %B %d, %Y")

            # Get date's year in YYYY format (e.g., 1986) for inflation calculation
            release_year = date_partially_formatted.strftime("%Y")

            # Get date's year in mm format (e.g., 10 is October) for inflation calculation
            release_month = date_partially_formatted.strftime("%m")

            # Put completely formatted date in the list of dicts
            console_info[i]["usa_release_date"] = date_completely_formatted

            # Get a formatted version of the United States release price
            console_info[i]["formatted_release_price"] = usd(console_info[i]["usa_release_date_usa_price"])

            ##############################################################################
            #                                                                            #
            #  End of for loop for adding information to the dicts in the list of dicts  #
            #                                                                            #
            ##############################################################################

        # Get a list of cardinal numbers for the table
        cardinal_numbers = list(range(0,len(console_info)))

        # Get a dictionary of months of the year (e.g., January:01)
        months = months_dict()

        # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
        years = list(range(1913, 2021))

        # Reverse the order of the list of years
        years.reverse()

        # Tell the route what to output
        return render_template("console_release_prices.html",
            arrival_method=request.method,
            cardinal_numbers=cardinal_numbers,
            console_info=console_info,
            inflation_month_short=inflation_month_short,
            inflation_year=inflation_year,
            months=months,
            years=years)

        return "POST"

    # If user accesses route via POST
    # elif request.method == "POST":

@app.route("/console_sales", methods=["GET", "POST"])
def console_sales():

    # Check whether user is accessing route via a mobile device
    if request.MOBILE == True:

        # Set mobile to True if user is using a mobile device
        mobile = True

    else:

        # Set mobile to False if user is not using a mobile device
        mobile = False

    # Empty list that will eventually hold info to display on webpage
    console_info = []

    # If user accesses route via GET
    if request.method == "GET":

        # Get put each database row in a dict and put each dict in a list of dicts
        console_info = db.execute("\
            SELECT console_name, usa_release_date, units_sold, gaming_generation, company \
            FROM console_info")

        # Get a list of cardinal numbers for the table
        cardinal_numbers = list(range(0,len(console_info)))

        # Get a dictionary of months of the year (e.g., January:01)
        months = months_dict()

        # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
        years = list(range(1913, 2021))

        # Reverse the order of the list of years
        years.reverse()

        ######################################################
        # Begin for loop for populating list of dictionaries #
        ######################################################

        # iterate over each dictionary in the list of dictionaries
        for i in range(0, len(console_info)):

            # Change from zero-index to one-index
            console_info[i]["cardinal_number"] = i + 1

            # Get date unformatted
            date_unformatted = console_info[i]["usa_release_date"]

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Put completely formatted date in the list of dicts
            console_info[i]["usa_release_date"] = date_partially_formatted.strftime("%B %d, %Y")

            # Put formatted number of units sold in the list of dicts
            # TODO

            if console_info[i]["units_sold"] != "Not Applicable":

                temporary_string_storage = int(float(console_info[i]["units_sold"]))

                console_info[i]["units_sold_formatted"] = f"{temporary_string_storage:,}"

            else:

                console_info[i]["units_sold_formatted"] = console_info[i]["units_sold"]

            # Put formated release prices in the list of dicts
            # console_info[i]["formatted_release_price"] = usd(console_info[i]["usa_release_date_usa_price"])

            # Store a version of the console name with underscores substituted for spaces
            temporary_storage = console_info[i]["console_name"]

            console_info[i]["console_name_underscored"] = temporary_storage.replace(" ", "_")

        ####################################################
        # End for loop for populating list of dictionaries #
        ####################################################

        # Tell the route what to output
        return render_template("console_sales.html",
            cardinal_numbers=cardinal_numbers,
            arrival_method=request.method,
            months=months,
            years=years,
            console_info=console_info)

    # If user accesses route via POST
    else:

        # Return error message
        return apology("You should only be accessing this route via a GET request.")

@app.route("/console_release_prices_test", methods=["POST"])
def console_release_prices_test():

    # https://pythonise.com/series/learning-flask/flask-and-fetch-api

    request_mk_007 = request.get_json()

    print(f"year = {request_mk_007['year']} | month = {request_mk_007['month']}")

    # response_mk_007 = jsonify({"message": "Go Go Power Rangers!"})

    # Get user selected year for inflation calculation
    inflation_year = request_mk_007["year"]

    if inflation_year == "":

        # Return error message
        return apology("Please select a year for the inflation calculation.")

    # Get user selected month for inflation calculation
    inflation_month = request_mk_007["month"]

    # Check whether user provided an inflation month
    if inflation_month == "":

        # Return error message
        return apology("Please select a month for the inflation calculation.")

    # Make a datetime object from the inflation month
    inflation_month_short = datetime.datetime.strptime(inflation_month, "%m")

    # Get the short name version of months (e.g., Jan)
    inflation_month_short = inflation_month_short.strftime("%b")

    # Get put each database row in a dict and put each dict in a list of dicts
    console_info = db.execute("\
        SELECT console_name, usa_release_date, usa_release_date_usa_price, gaming_generation, company \
        FROM console_info")

    # Add key:value pairs the dicts in the list of dicts
    # for i in range(0, len(console_info)):

    #     # Change from zero-index to one-index
    #     console_info[i]["cardinal_number"] = i + 1

    #     # Create a dict to how components of the inflation URL
    #     url_components = {}

    #     # Add the base of the URL
    #     url_components["base"] = "https://data.bls.gov/cgi-bin/cpicalc.pl?"

    #     # Add the cost1 component of the URL
    #     url_components["cost1"] = "cost1=" + str(console_info[i]["usa_release_date_usa_price"]) + "&"

    #     # Get date unformatted
    #     date_unformatted = console_info[i]["usa_release_date"]

    #     # Get date partially formatted
    #     date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

    #     # Transform the release year into an integer
    #     release_year_int = int(date_partially_formatted.strftime("%Y"))

    #     # Transfor the release month into an integer
    #     release_month_int = int(date_partially_formatted.strftime("%m"))

    #     # Create a variable to hold the inflation adjusted price
    #     inflation_answer = ""

    #     # Get current month as an int (e.g., November would be 11)
    #     # current_month = datetime.datetime.now().month
    #     current_month = int(datetime.datetime.now().month)

    #     # Get current year as an int (e.g., 2019 would be 2019)
    #     # current_year = datetime.datetime.now().year
    #     current_year = int(datetime.datetime.now().year)

    #     # https://www.bls.gov/data/inflation_calculator.htm
    #     # About the CPI Inflation Calculator
    #     # The CPI inflation calculator uses the Consumer Price Index for All Urban Consumers (CPI-U)
    #         # U.S. city average series for all items, not seasonally adjusted. This data represents
    #         # changes in the prices of all goods and services purchased for consumption by urban households.
    #     # CUUR0000SA0


    #     # Get the release price adjusted for inflation
    #     if release_year_int < current_year or (release_year_int == current_year and release_month_int < current_month - 1):

    #         if int(inflation_year) < current_year or (int(inflation_year) == current_year and int(inflation_month) < current_month - 1):

    #             # Add the year1 component of the URL
    #             url_components["year1"] = "year1=" + date_partially_formatted.strftime("%Y") + date_partially_formatted.strftime("%m") + "&"

    #             # Add the year2 component of th URL
    #             url_components["year2"] = "year2=" + inflation_year + inflation_month

    #             # Convert the dict values to a list
    #             url_components_list = list(url_components.values())

    #             # Convert the list items to a single string
    #             url_string = "".join(url_components_list)

    #             # The get() method returns a requests.Response object
    #             inflation_answer_page = requests.get(url_string)

    #             # Get a BeautifulSoup object
    #             soup = BeautifulSoup(inflation_answer_page.text, "html.parser")

    #             # Search the soup for the inflation adjusted price
    #             inflation_answer_with_tags = soup.find("span", id="answer")

    #             # Put the release price (adjusted for inflation) in the dictionary
    #             console_info[i]["inflation_answer"] = inflation_answer_with_tags.text

    #         # Scenario for inflation price data is unavailable
    #         else:

    #             # Put the data-is-unavailabe message in the dictionary
    #             console_info[i]["inflation_answer"] = "Not Available"

    #     # Scenario for when inflation price data is unavailable
    #     else:

    #         # Put the data-is-unavailabe message in the dictionary
    #         console_info[i]["inflation_answer"] = "Not Available"

    #     # Get date unformatted
    #     date_unformatted = console_info[i]["usa_release_date"]

    #     # Get date partially formatted
    #     date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

    #     # Get date completely formatted
    #     date_completely_formatted = date_partially_formatted.strftime("%A, %B %d, %Y")

    #     # Get date's year in YYYY format (e.g., 1986) for inflation calculation
    #     release_year = date_partially_formatted.strftime("%Y")

    #     # Get date's year in mm format (e.g., 10 is October) for inflation calculation
    #     release_month = date_partially_formatted.strftime("%m")

    #     # Put completely formatted date in the list of dicts
    #     console_info[i]["usa_release_date"] = date_completely_formatted

    #     # Get a formatted version of the United States release price
    #     console_info[i]["formatted_release_price"] = usd(console_info[i]["usa_release_date_usa_price"])

    #     # Store the inflation year
    #     console_info[i]["inflation_year"] = inflation_year

    #     # Store the short version of the inflation month (e.g., January gets stored at Jan)
    #     console_info[i]["inflation_month_short"] = inflation_month_short

    #     # Store a version of the console name with underscores substituted for spaces
    #     temporary_storage = console_info[i]["console_name"]

    #     console_info[i]["console_name_underscored"] = temporary_storage.replace(" ", "_")


    #     ##############################################################################
    #     #                                                                            #
    #     #  End of for loop for adding information to the dicts in the list of dicts  #
    #     #                                                                            #
    #     ##############################################################################

    # Get Consumer Price Index Data from the Bureau of Labor Statistics
    consumer_price_index_data_raw = urlopen("https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems")

    # Read the raw CPI data
    cpi_data = consumer_price_index_data_raw.read()

    # Make each line of data a list in a list of lists
    cpi_data_list = cpi_data.splitlines()

    # Prepare a list to hold the decoded CPI data
    cpi_data_list_decoded = []

    # Prepare a list to hold the relevan CPI data
    cpi_data_targeted = []

    # Decode the CPI data
    for i in range(0, len(cpi_data_list), 1):

        # Decode a line of cpi data and add it to the decoded list
        cpi_data_list_decoded.append(cpi_data_list[i].decode("utf8"))

        # Remove the none alphanumeric characters from each line in the data
        cpi_data_list_decoded[i] = cpi_data_list_decoded[i].split()

        if cpi_data_list_decoded[i][0] == "CUUR0000SA0":

            # Add the string to the targeted list of lists
            cpi_data_targeted.append(cpi_data_list_decoded[i])

    # Add key:value pairs the dicts in the list of dicts
    for i in range(0, len(console_info)):

        # Change from zero-index to one-index
        console_info[i]["cardinal_number"] = i + 1

        # Get date unformatted
        date_unformatted = console_info[i]["usa_release_date"]

        # Get date partially formatted
        date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

        # Transform the release year into an integer
        release_year_int = int(date_partially_formatted.strftime("%Y"))

        # Transfor the release month into an integer
        release_month_int = int(date_partially_formatted.strftime("%m"))

        # Create a variable to hold the inflation adjusted price
        inflation_answer = ""

        # Get current month as an int (e.g., November would be 11)
        current_month = int(datetime.datetime.now().month)

        # Get current year as an int (e.g., 2019 would be 2019)
        current_year = int(datetime.datetime.now().year)

        # https://www.bls.gov/data/inflation_calculator.htm
        # About the CPI Inflation Calculator
        # The CPI inflation calculator uses the Consumer Price Index for All Urban Consumers (CPI-U)
            # U.S. city average series for all items, not seasonally adjusted. This data represents
            # changes in the prices of all goods and services purchased for consumption by urban households.
        # CUUR0000SA0

        # Get the release price adjusted for inflation
        if release_year_int < current_year or (release_year_int == current_year and release_month_int < current_month - 1):

            if int(inflation_year) < current_year or (int(inflation_year) == current_year and int(inflation_month) < current_month - 1):

                # Find Consumer Price Index for the inflation date
                for j in range(0, len(cpi_data_targeted), 1):

                    # Add an "M" to the inflation month so it can be compared to the BLS data
                    inflation_month_string = "M" + inflation_month

                    # Check for the presence of the inflation year and the inflation month in BLS CPI data
                    if cpi_data_targeted[j][1] == str(inflation_year) and cpi_data_targeted[j][2] == inflation_month_string:

                        # Store the inflation date's CPI
                        inflation_date_cpi = cpi_data_targeted[j][3]

                        # print(f"i: {i} | inflation data: cpi_data_targeted[{j}]: {cpi_data_targeted[j]}")

                        break

                # Find Consumer Price Index for the release date
                for k in range(0, len(cpi_data_targeted), 1):

                    # Add an "M" to the inflation month so it can be compared to the BLS data
                    release_month_string = "M" + str(release_month_int)

                    # Check for the presence of the inflation year and the inflation month in BLS CPI data
                    if cpi_data_targeted[k][1] == str(release_year_int) and cpi_data_targeted[k][2] == release_month_string:

                        # Store the inflation date's CPI
                        release_date_cpi = cpi_data_targeted[k][3]

                        print(f"i: {i} | release data: cpi_data_targeted[{k}]: {cpi_data_targeted[k]}")

                        break

                # Calculate release price adjusted for inflation
                # https://www.maa.org/press/periodicals/loci/joma/the-consumer-price-index-and-inflation-adjust-numbers-for-inflation
                inflation_adjusted_price = (float(inflation_date_cpi) / float(release_date_cpi)) * float(console_info[i]["usa_release_date_usa_price"])

                console_info[i]["inflation_answer"] = usd(round(inflation_adjusted_price))

            # Scenario for inflation price data is unavailable
            else:

                # Put the data-is-unavailabe message in the dictionary
                console_info[i]["inflation_answer"] = "Not Available"

        # Scenario for when inflation price data is unavailable
        else:

            # Put the data-is-unavailabe message in the dictionary
            console_info[i]["inflation_answer"] = "Not Available"

        # Get date unformatted
        date_unformatted = console_info[i]["usa_release_date"]

        # Get date partially formatted
        date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

        # Get date completely formatted
        date_completely_formatted = date_partially_formatted.strftime("%A, %B %d, %Y")

        # Get date's year in YYYY format (e.g., 1986) for inflation calculation
        release_year = date_partially_formatted.strftime("%Y")

        # Get date's year in mm format (e.g., 10 is October) for inflation calculation
        release_month = date_partially_formatted.strftime("%m")

        # Put completely formatted date in the list of dicts
        console_info[i]["usa_release_date"] = date_completely_formatted

        # Get a formatted version of the United States release price
        console_info[i]["formatted_release_price"] = usd(console_info[i]["usa_release_date_usa_price"])

        # Store the inflation year
        console_info[i]["inflation_year"] = inflation_year

        # Store the short version of the inflation month (e.g., January gets stored at Jan)
        console_info[i]["inflation_month_short"] = inflation_month_short

        # Store a version of the console name with underscores substituted for spaces
        temporary_storage = console_info[i]["console_name"]

        console_info[i]["console_name_underscored"] = temporary_storage.replace(" ", "_")


        ##############################################################################
        #                                                                            #
        #  End of for loop for adding information to the dicts in the list of dicts  #
        #                                                                            #
        ##############################################################################


    # https://healeycodes.com/javascript/python/beginners/webdev/2019/04/11/talking-between-languages.html

    print("Hello, world!")

    # # Tell the route what to output
    # return "Hello, world"

    route_output = jsonify(console_info)

    return route_output

    # Tell the route what to output
    return jsonify(console_info)  # serialize and use JSON headers

    # Tell the route what to output
    return str(console_info)

    # Tell the route what to output
    return "Hello, world"
