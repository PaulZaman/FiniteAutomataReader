from determinization import *
# this file contains completion algorithms


def complete(automaton):
    table = copy.deepcopy(automaton.table)

    # if automaton is not deterministic return False
    if not automaton.is_deterministic:
        return False

    # fill empty spaces with P
    for i in range(len(table)):
        for k in range(len(table[i])):
            if table[i][k] == '--':
                table[i][k] = 'P'

    # add trash state line at end of table
    p_line = []
    for i in range(len(table[0])):
        p_line.append("P")
    table.append(p_line)

    # create and return new automaton
    return FiniteAutomata(table=table, final_states=automaton.final_states, initial_states=automaton.initial_states)

