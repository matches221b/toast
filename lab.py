def descending_order(num):

    # Convert the number to a string
    string = str(num)

    unordered_list = []

    # Convert each numeral to an int and add them (one-at-a-time) to a list
    for x in string:

        unordered_list.append(int(x))

    ordered_list_descending = sorted(unordered_list, reverse=True)

    ordered_string_descending = "".join(ordered_list_descending)

    ordered_int_descending = int(ordered_string_descending)

    return ordered_int_descending

num = 12345

print(num)

num_2 = descending_order(num)

print(num_2)

