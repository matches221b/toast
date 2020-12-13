#
import os
# from flask import Flask, render_template, request
from flask import Flask, flash, jsonify, redirect, render_template, request, session
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

dataframe = pd.read_excel("games.xlsx")

connection = sqlite3.connect("database01.db")

cursor = connection.cursor()

dataframe.to_sql("TOAST", con=connection, if_exists="replace", index=True)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database01.db")

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


@app.route("/microsoft", methods=["GET", "POST"])
def microsoft():
    """Show information about Microsoft's consoles"""

    # Route for access via GET
    if request.method == "GET":

        # microsoft_dict = db.execute("SELECT Console_Name, United_States_Release_Date, \
        #                             United_States_Release_Date_Price_(USD), Gaming_Generation, \
        #                             Company")

        microsoft_info = db.execute("SELECT * FROM TOAST WHERE company = :company", company="Microsoft")

        cardinal_numbers = list(range(0,len(microsoft_info)))

        for i in range(0, len(microsoft_info)):

            # Change from zero-index to one-index
            microsoft_info[i]["cardinal_number"] = i + 1

            # Get date unformatted
            date_unformatted = microsoft_info[i]["usa_release_date"]

            # date_partially_formatted = datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S")

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Get date completely formatted
            date_completely_formatted = date_partially_formatted.strftime("%A, %B %d, %Y")

            # microsoft_info[i]["usa_release_date"] = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Put completely formatted date in the list of dicts
            microsoft_info[i]["usa_release_date"] = date_completely_formatted

            microsoft_info[i]["formatted_release_price"] = usd(microsoft_info[i]["usa_release_date_usa_price"])

        # Get a dictionary of months of the year (e.g., January:01)
        months = months_dict()

        # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
        years = list(range(1913, 2021))

        # Reverse the order of the list of years
        years.reverse()

        arrival_method = request.method

        return render_template("microsoft.html",
            microsoft_info=microsoft_info,
            months=months,
            years=years,
            arrival_method=arrival_method)

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
        microsoft_info = db.execute("SELECT * FROM TOAST WHERE company = :company", company="Microsoft")

        # Get list of cardinal numbers
        cardinal_numbers = list(range(0,len(microsoft_info)))

        # Get month for inflation adjusted price
        inflation_month = request.form.get("month")

        # Get year for inflation adjusted price
        inflation_year = request.form.get("year")

        # # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=100.00&year1=200001&year2=202009

        # # Create a dict to how components of the inflation URL
        # url_components = {}

        # # Add the base of the URL
        # url_components["base"] = "https://data.bls.gov/cgi-bin/cpicalc.pl?"

        # # Add the cost1 component of the URL
        # url_components["cost1"] = "cost1=" + str(microsoft_info[0]["usa_release_date_usa_price"]) + "&"

        # # Get date unformatted
        # date_unformatted = microsoft_info[0]["usa_release_date"]

        # # Get date partially formatted
        # date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

        # # Add the year1 component of the URL
        # url_components["year1"] = "year1=" + date_partially_formatted.strftime("%Y") + date_partially_formatted.strftime("%m") + "&"

        # # Add the year2 component of th URL
        # url_components["year2"] = "year2=" + inflation_year + inflation_month

        # # Convert the dict values to a list
        # url_components_list = list(url_components.values())

        # # Convert the list items to a single string
        # url_string = "".join(url_components_list)

        # # The get() method returns a requests.Response object
        # inflation_answer_page = requests.get(url_string)

        # # Get a BeautifulSoup object
        # soup = BeautifulSoup(inflation_answer_page.text, "html.parser")

        # # Find the answer in the soup
        # inflation_answer_with_tags = soup.find("span", id="answer")

        # # Remove the tags from the answer
        # inflation_answer = inflation_answer_with_tags.text

        # inflation_answer = soup.find("span", id="answer")

        # # list(dictionary.values())

        # url_components_list = list(url_components.values())

        # url_string = "".join(url_components_list)

        # inflation_answer_page = requests.get(url_string)

        # soup = BeautifulSoup(inflation_answer_page.text, "html.parser")

        # inflation_answer = soup.find("span", id="answer")

        # inflation_answer = inflation_answer.text


        # Add key:value pairs the dicts in the list of dicts
        for i in range(0, len(microsoft_info)):

            # Change from zero-index to one-index
            microsoft_info[i]["cardinal_number"] = i + 1

            # Create a dict to how components of the inflation URL
            url_components = {}

            # Add the base of the URL
            url_components["base"] = "https://data.bls.gov/cgi-bin/cpicalc.pl?"

            # Add the cost1 component of the URL
            url_components["cost1"] = "cost1=" + str(microsoft_info[i]["usa_release_date_usa_price"]) + "&"

            # Get date unformatted
            date_unformatted = microsoft_info[i]["usa_release_date"]

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

                microsoft_info[i]["inflation_answer"] = inflation_answer_with_tags.text

            else:
                inflatio_answer_with_tags = "Not Available"

                inflation_answer = "Not Available"

                microsoft_info[i]["inflation_answer"] = inflation_answer



            # Get date unformatted
            date_unformatted = microsoft_info[i]["usa_release_date"]

            # Get date partially formatted
            date_partially_formatted = datetime.datetime.strptime(date_unformatted, "%Y-%m-%d %H:%M:%S").date()

            # Get date completely formatted
            date_completely_formatted = date_partially_formatted.strftime("%A, %B %d, %Y")

            # Get date's year in YYYY format (e.g., 1986) for inflation calculation
            release_year = date_partially_formatted.strftime("%Y")

            # Get date's year in mm format (e.g., 10 is October) for inflation calculation
            release_month = date_partially_formatted.strftime("%m")

            # Put completely formatted date in the list of dicts
            microsoft_info[i]["usa_release_date"] = date_completely_formatted

            # Get a formatted version of the United States release price
            microsoft_info[i]["formatted_release_price"] = usd(microsoft_info[i]["usa_release_date_usa_price"])

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
            microsoft_info=microsoft_info,
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
            inflation_answer=inflation_answer)
            # date_year=date_year,
            # url_components=url_components,
            # url_components_list=url_components_list,
            # url_string=url_string,
            # inflation_answer=inflation_answer)


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

        console_info = db.execute("SELECT * FROM TOAST WHERE company = :company", company="Nintendo")

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

        return render_template("nintendo.html",
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
            mobile=mobile)
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

@app.route("/toast", methods=["GET", "POST"])
def toast():

    return render_template("toast.html")