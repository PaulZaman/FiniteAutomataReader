from complementarization import *
# this file contains minimization algorithms


def rename_states(FA):
    table = copy.deepcopy(FA.table)
    first_column = list()
    for line in table:
        first_column.append(line[0])
    renamed = []

    for line in table[1:]:
        if line[0] != 'P' and len(line[0]) > 1:  # if state number is two digits or more
            # find correct state name
            i = 0
            while is_in_list(str(i), first_column): i += 1
            old_state_name = line[0]
            new_state_name = str(i)

            # find all states and replace with new_state_name
            for i in range(len(table)):
                for k in range(len(table[0])):
                    if table[i][k] == old_state_name:
                        table[i][k] = new_state_name

            # update first column table
            for lin in table:
                first_column.append(lin[0])
            renamed.append(str("State: " + old_state_name + " renamed to : " + new_state_name))

        if line[0] == 'P':
            # replace with other digit
            # find correct state name
            i = 0
            while is_in_list(str(i), first_column): i += 1
            old_state_name = line[0]
            new_state_name = str(i)

            # find all states and replace with new_state_name
            for i in range(len(table)):
                for k in range(len(table[0])):
                    if table[i][k] == old_state_name:
                        table[i][k] = new_state_name

            # update first column table
            for lin in table:
                first_column.append(lin[0])

            renamed.append(str("State: " + old_state_name + " renamed to : " + new_state_name))

    # update final and initial states
    final_states = copy.deepcopy(FA.final_states)
    initial_states = copy.deepcopy(FA.initial_states)
    for i in range(len(final_states)):
        index = FA.states.index(final_states[i]) + 1
        final_states[i] = table[index][0]
    for i in range(len(initial_states)):
        index = FA.states.index(initial_states[i]) + 1
        initial_states[i] = table[index][0]

    # display renamed table in terminal
    #print("\n")
    #for string in renamed:
    #    print(string)

    return FiniteAutomata(table=table, final_states=final_states, initial_states=initial_states)


def replace_table_by_NT_and_T(FA, table):
    # fills table passed as parameter with NT and T
    t = copy.deepcopy(table)
    for i in range(len(t)):
        for k in range(1, len(t[0])):
            if is_in_list(t[i][k], FA.final_states):
                t[i][k] = "T"
            elif not is_in_list(t[i][k], FA.final_states):
                t[i][k] = "NT"
    return t


def find_patterns(table):
    # gets table as paramater
    # returns a list (of strings) containing new states with similar patterns
    new_states = []
    for i in range(len(table)):
        similar_states = []
        for k in range(len(table)):
            if k != i:
                if table[i][1:] == table[k][1:]:
                    similar_states.append(table[k][0])
                    similar_states.append(table[i][0])
        similar_states.sort()
        similar_states = remove_occurences(similar_states)
        new_state = list_to_string_no_commas(similar_states)
        if not is_in_list(new_state, new_states):
            new_states.append(new_state)

    while '' in new_states:
        new_states.remove('')

    # add to new_states list states that are not contained in "new_states"
    for i in range(len(table)):
        if not_in_list_or_string_of_list(table[i][0], new_states):
            new_states.append(table[i][0])
    return new_states


def fill_final_table(FA, theta):
    # called when minimization is almost finished
    # fills tables with new states of theta
    final_table = []
    final_table.append(copy.deepcopy(FA.table[0]))

    # get first column (to find index)
    first_column = []
    for i in range(len(FA.table)):
        first_column.append(copy.deepcopy(FA.table[i][0]))

    # add
    for state in theta:
        if len(state) == 1:
            final_table.append(copy.deepcopy(FA.table[first_column.index(state)]))
        else:
            final_table.append(copy.deepcopy(FA.table[first_column.index(state[0])]))
            final_table[len(final_table)-1][0] = state

    for i in range(1, len(final_table)):
        for k in range(1, len(final_table[0])):
            if is_in_list_or_string_of_list(final_table[i][k], theta):
                final_table[i][k] = is_in_list_or_string_of_list(final_table[i][k], theta)

    return final_table


def table_theta(FA, state_of_theta, theta):
    # gets a table from a state of theta
    # returns the table updated with outputs corresponding toother states of theta
    table = []
    first_column = []

    # get first column (to find index)
    for i in range(len(FA.table)):
        first_column.append(copy.deepcopy(FA.table[i][0]))
    # add line corresponding to letter in state in our new table
    for letter in state_of_theta:
        '''print("letter:", letter)
        print("fC", first_column)'''
        table.append(copy.deepcopy(FA.table[first_column.index(letter)]))

    # replace states by new state
    for i in range(len(table)):
        for k in range(1, len(table[0])):
            if is_in_list_or_string_of_list(table[i][k], theta):
                table[i][k] = is_in_list_or_string_of_list(table[i][k], theta)

    return table


def minimize(FA):
    # 1rst iteration
    terminal = []
    non_terminal = []

    # separating the terminal states from the non-terminal states
    for state in FA.states:
        if is_in_list(state, FA.final_states):
            terminal.append(copy.deepcopy(FA.table[FA.states.index(state) + 1]))
        else:
            non_terminal.append(copy.deepcopy(FA.table[FA.states.index(state) + 1]))

    # replace by NT and T in tables terminal and non-terminal
    terminal = replace_table_by_NT_and_T(FA, terminal)
    non_terminal = replace_table_by_NT_and_T(FA, non_terminal)

    # Now, we are looking for patterns that are similar inside the groups
    theta = find_patterns(non_terminal)
    new_states_t = find_patterns(terminal)
    for element in new_states_t:
        theta.append(element)

    run = True
    factorized = False
    # pour chaque element dans theta reconnaitre pattern
    while run:
        for state in theta:
            # If the state is bigger than 1 -> if the state can be factorized
            if len(state) > 1:
                factorized = True
                # newtable is the FA table, but with the new names given by the factorization :
                #    a   b   c               a   b   c
                # 0  0   1   1            0  01  01   01
                # 1  1   0   2         to 1  01  01   2
                # 2  2   1   1            2  2   01   01
                newtable = table_theta(FA, state, theta)
                theta.remove(state)
                if len(find_patterns(newtable)) == 1:
                    factorized = False
                for state_ in find_patterns(newtable):
                    theta.append(state_)

                #print("\ntheta:", theta)
        # Checks whether a factorization happened. If not, exit the loop
        if not factorized:
            run = False
        factorized = False

    # Checking if the automaton is already determinized
    if len(theta) == len(FA.table)-1:
        return False

    final_table = fill_final_table(FA, theta)

    # adding all final states & the initial state
    final_states = []
    for final_state in FA.final_states:
        for state in theta:
            if final_state in state:
                final_states.append(state)

    final_states = remove_occurences(final_states)

    initial_states = []
    for initial_state in FA.initial_states:
        for state in theta:
            if initial_state in state:
                initial_states.append(state)

    return FiniteAutomata(table=final_table, initial_states=initial_states, final_states=final_states)
