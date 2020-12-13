import calendar
import mechanize
import requests
from bs4 import BeautifulSoup
from flask import render_template

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def months_dict():
    """Dictionary of names of months with cardinal number counterparts"""

    months = {}

    # Iterate through the months dictionary
    for i in range(1, 13):

        # Give single-digit months a leading zero
        if i < 10:

            # Add a key:value pair to dictionary (e.g., January:01)
            months[calendar.month_name[i]] = str(i).zfill(2)

        # Leave double-digit months as they are with two digits
        else:

            # Add a key:value pair to dictionary (e.g, October:10)
            months[calendar.month_name[i]] = str(i)

    return months

# def inflation_answer():


# def inflation_years():
#     """List of years for calculating inflation adjusted price"""

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

