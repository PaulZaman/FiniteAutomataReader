from settings import *

def is_in_list(letter, list):
    for letters in list:
        if letter == letters:
            return True
    return False

def is_different_than(list, letter):
    for element in list:
        if element == letter:
            return False
    return True

def list_to_string(list):
    str = ""
    for element in list:
        str += element+", "
    str = str[:-2]
    return str

def list_to_string_no_commas(list):
    string = ""
    for letter in list:
        string += letter
    return string

def order_list(list):
    # to order our list containing files
    # for beauty of display
    new_list = []
    number = 1
    while number < len(list)+1:
        for i in range(len(list)):
            if int(list[i][-2:]) == number:
                new_list.append(list[i])
                number += 1
    return new_list

def not_in_list_or_string_of_list(element, list):
    for el in list:
        if el == element:
            return False
        for letter in el:
            if letter == element:
                return False
    return True

def is_in_list_or_string_of_list(element, list):
    for el in list:
        if el == element:
            return el
        for letter in el:
            if letter == element:
                return el
    return False

def divide_list_into2(list):
    list1 = []
    list2 = []
    for i in range(int(len(list) / 2)):
        list1.append(list[i])
    for i in range(len(list) - int(len(list) / 2)):
        list2.append(list[int(len(list) / 2) + i])
    return list1, list2

def divide_list_into4(list):
    list1, list2 = divide_list_into2(list)
    res1 = divide_list_into2(list1)
    res2 = divide_list_into2(list2)
    return res1[0], res1[1], res2[0], res2[1]

def remove_occurences(list):
    new_list = []
    for element in list:
        if not is_in_list(element, new_list):
            new_list.append(element)
    return new_list

def search_state_string(state, theta):
    for el in theta:
        if state in el:
            return el
