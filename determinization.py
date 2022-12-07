import copy
# this file contains determinization algorithms


from Finite_automata import *

def from_state_to_exits(FA, letter_of_alphabet, state):
    # from a state ex: 012
    # returns a string containing all exits of all different states

    # Add into "states", next states
    states = []
    for i in range(1, len(FA.table)):
        for k in range(len(state)):
            if FA.table[i][0] == state[k] and FA.table[i][FA.table[0].index(letter_of_alphabet)] != '--':
                states.append(FA.table[i][FA.table[0].index(letter_of_alphabet)])

    # clean up list, remove "--" and remove commas into seperate numbers
    i = 0
    while i < len(states):
        # remove commas
        if is_in_list(",", states[i]):
            numbers = states[i].split(",")
            for num in numbers:
                states.append(num)
            states.remove(states[i])
            i = -1
        i += 1

    # sort and remove occurences
    states.sort()
    states = remove_occurences(states)

    # create a string from state list
    states_string = ""
    for state in states:
        states_string += state
    if states_string == "":
        states_string = "--"
    return states_string

def determinize(FA):
    table = copy.deepcopy(FA.table)
    # create new table
    new_table = [table[0]]

    # add first line
    # find entry states and add to "states to add list"
    entry = ""
    for state in FA.initial_states:
        entry += state

    states_to_add = [entry]
    first_column_of_new_table = []

    while len(states_to_add) >= 1:
        # add new state
        new_table.append([states_to_add[0]])
        states_to_add.remove(states_to_add[0])

        # add line of new state
        for i in range(1, len(table[0])):
            new_table[len(new_table)-1].append(from_state_to_exits(FA, table[0][i], new_table[len(new_table)-1][0]))

        # get first column of new table
        for i in range(len(new_table)):
            if not is_in_list(new_table[i][0], first_column_of_new_table):
                  first_column_of_new_table.append(new_table[i][0])

        # if new_states are not in 1rst column, add them to states_to_add
        for state in new_table[len(new_table)-1]:
            if not is_in_list(state, states_to_add) and not is_in_list(state, first_column_of_new_table) and state != '--':
                states_to_add.append(state)

    # find new exits
    final_states = []
    for line in new_table:
        for letter in line[0]:
            if is_in_list(letter, FA.final_states):
                final_states.append(line[0])

    final_states = remove_occurences(final_states)

    return FiniteAutomata(table=new_table, initial_states=[new_table[1][0]], final_states=final_states)
