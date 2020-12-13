# # the lib that handles the url stuff
# # import os
# # import urllib2

# from urllib.request import urlopen

# # https://stackoverflow.com/questions/1393324/given-a-url-to-a-text-file-what-is-the-simplest-way-to-read-the-contents-of-the

# # it's a file like object and works just like a file
# data = urllib2.urlopen("https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems")

# for line in data: # files are iterable

#     print(line)

from urllib.request import urlopen

# from bs4 import UnicodeDammit

# data = urlopen("https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems")

consumer_price_index_data_raw = urlopen("https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems")

cpi_data = consumer_price_index_data_raw.read()

cpi_data_list = cpi_data.splitlines()

cpi_data_list_decoded = []

cpi_data_targeted = []

CUUR0000SA0_counter = 0

for i in range(0, len(cpi_data_list), 1):

    # Decode a line of cpi data and add it to the decoded list
    cpi_data_list_decoded.append(cpi_data_list[i].decode("utf8"))

    # Remove the none alphanumeric characters from each line in the data
    cpi_data_list_decoded[i] = cpi_data_list_decoded[i].split()

    if cpi_data_list_decoded[i][0] == "CUUR0000SA0":

        # Add the string to the targeted list of lists
        cpi_data_targeted.append(cpi_data_list_decoded[i])

        # print(cpi_data_list_decoded[i])

        # CUUR0000SA0_counter = CUUR0000SA0_counter + 1

# for i in range(0, len(cpi_data_targeted), 1):

#     print(cpi_data_targeted[i])

inflation_year = 1986

inflation_month = "10"

release_price = 299.99

release_year = 2001

release_month = "11"

# Find Consumer Price Index for the inflation date
for i in range(0, len(cpi_data_targeted), 1):

    # Add an "M" to the inflation month so it can be compared to the BLS data
    inflation_month_string = "M" + inflation_month

    # Check for the presence of the inflation year and the inflation month in BLS CPI data
    if cpi_data_targeted[i][1] == str(inflation_year) and cpi_data_targeted[i][2] == inflation_month_string:

        # Store the inflation date's CPI
        inflation_date_cpi = cpi_data_targeted[i][3]

        print(f"inflation date info --> year: {cpi_data_targeted[i][1]} | month: {cpi_data_targeted[i][2]} | CPI: {cpi_data_targeted[i][3]}")

# Find Conumer Price Index for the release date
for i in range(0, len(cpi_data_targeted), 1):

    # Add an "M" to the inflation month so it can be compared to the BLS data
    release_month_string = "M" + release_month

    # Check for the presence of the inflation year and the inflation month in BLS CPI data
    if cpi_data_targeted[i][1] == str(release_year) and cpi_data_targeted[i][2] == release_month_string:

        # Store the inflation date's CPI
        release_date_cpi = cpi_data_targeted[i][3]

        print(f"release date info ----> year: {cpi_data_targeted[i][1]} | month: {cpi_data_targeted[i][2]} | CPI: {cpi_data_targeted[i][3]}")

# Release Year Price
print(f"release date price ---> {release_price}")

# Calculate release price adjusted for inflation
inflation_adjusted_price = (float(inflation_date_cpi) / float(release_date_cpi)) * float(release_price)

print(f"inflation adjusted price --> ${inflation_adjusted_price}")

print(f"inflation adjusted price --> ${round(inflation_adjusted_price, 2)}")

# inflation_adjusted_price = (CPI Inflation Date / CPI Release Date) * (Release Date Price)


# for i in range(0, len(cpi_data_targeted), 1):

#     temporary_storage = "M" + inflation_month

#     if cpi_data_targeted[i][1] == str(inflation_year) and cpi_data_targeted[i][2] == temporary_storage:

#         print(temporary_storage)
#         print(cpi_data_targeted[i])
#         print(f"cpi_data_targeted[{i}][3]: {cpi_data_targeted[i][3]}")



# inflation_adjusted_price = ( CPI Year 2 / CPI Year 1 ) * (Release Year)

# print(CUUR0000SA0_counter)

# print(cpi_data_list_decoded)

# print(len(cpi_data_list))

# for line in cpi_data:

#     print(chr(line))

# print(cpi_data)

# consumer_price_index_data_decoded = consumer_price_index_data_raw.decode("utf-8")

# print(consumer_price_index_data_decoded)

# cpi_data_big_list = []

# cpi_data_targeted_list = []

# targeted_list_counter = 0

# for line in consumer_price_index_data:

#     cpi_data_big_list.append(line)

# print(len(cpi_data_big_list))

# temporary_storage = ""

# print(cpi_data_big_list[1][0:11])

# if cpi_data_big_list[1][0:11] == "CUSR0000SA0":

# # utf-8 is used here because it is a very common encoding, but you
# # need to use the encoding your data is actually in.
# >>> b"abcde".decode("utf-8")
# 'abcde'

# toast = cpi_data_big_list[1][0:11]

# test = toast.decode("utf-8")

# print(test)

# # print(f"{cpi_data_big_list[1][0:11]} == CUSR0000SA0")

# print()

# if test == "CUSR0000SA0":

#     print(f"{test} == CUSR0000SA0")

# for i in range(0, len(cpi_data_big_list)):

#     temporary_storage = ""

#     for j in range(0, 11, 1):

#         temporary_storage.append(chr(cpi_data_big_list[i][j]))

#     print(temporary_storage)

#     if temporary_storage == "CUUR0000SA0":

#         targeted_list_counter = targeted_list_counter + 1

# print(f"targeted_list_counter: {targeted_list_counter}")

# data_as_list = []

# i = 0

# for line in data:

#     data_as_list.append(line)



# print(data_as_list)

# print()

# print(f"data_as_list[1]: {data_as_list[1]}")

# print()

# print(chr(data_as_list[1][0]))

# print()

# print(f"length of data_as_list[1]: {len(data_as_list[1])}")

# for i in range(0, 42, 1):

#     print(f"data_as_list[{i}]: {chr(data_as_list[1][i])} | {data_as_list[1][i]}")

# print()

# for i in range(0, 42, 1):

#     print(f"data_as_list[{i}]: {chr(data_as_list[2][i])} | {data_as_list[2][i]}")


# print(f"data_as_list[1]: ", end="")

# counter = "toast"

# for i in range(0, 11, 1):

#     temporary_storage = []

#     temporary_storage.append(chr(data_as_list[1][i]))

#     # print(chr(data_as_list[1][i]), end="")

#     if temporary_storage == "CUUR0000SA0":

#         counter = "Yes"

#     else:

#         counter = "No"

# print()

# print(counter)

# print(len(data_as_list[1]))

# for i in range(len(data_as_list[1])):

#     print(f"data_as_list[{i}]: {data_as_list[i]}")

# for line in data:

#     if i < 10:

#         print(line)
#         print(i)

#     i = i + 1


# for line in data:

#     print(line)

# >>> a = b'asdf\nasdf'
# >>> a.split(b'\n')
# [b'asdf', b'asdf']

# print(data.split("b'\n'"))

# x = b"Bytes objects are immutable sequences of single bytes"

# print(x)

# decoded_bytes_object = data.decode()

# print(decoded_bytes_object)

# # create a string using the decode() method of bytes.
# #This method takes an encoding argument, such as UTF-8, and optionally an errors argument.
# x = b'El ni\xc3\xb1o come camar\xc3\xb3n'
# s = x.decode()
# print(type(s))
# print(s)



# from bs4 import UnicodeDammit
# dammit = UnicodeDammit("Sacr\xc3\xa9 bleu!")
# print(dammit.unicode_markup)
# # Sacré bleu!
# dammit.original_encoding
# # 'utf-8'

# unicode_version = UnicodeDammit(data)

# print(unicode_version)

# print(str(data))




# from helpers import months_dict

# months = months_dict()

# for item in months:
#     print(f"{item}: {months[item]}")

# # print(months)

# # years = list(range(1913, 2021))

# # for item in years:
# #     print(item)


# # # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
# # years_older_to_newer = list(range(1913, 2021))

# # # Reverse the order of the list of years
# # years = years_older_to_newer.reverse()

# # Get a list of years that work with the Bureau of Labor Statics' CPI Inflation Calculator
# years = list(range(1913, 2021))

# # Reverse the order of the list of years
# years.reverse()

# print(years)

