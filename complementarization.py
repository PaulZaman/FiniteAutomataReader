from completion import *
# this file contains complementarisation algorithms


def complementarize(automaton):
    table = copy.deepcopy(automaton.table)
    final_states = []

    for state in automaton.states:
        if not is_in_list(state, automaton.final_states):
            final_states.append(state)

    return FiniteAutomata(table=table, final_states=final_states, initial_states=automaton.initial_states)


'''f = FiniteAutomata("Int-1-6-21")
f_complete = complete(f)
f_complete_complementary = complementarize(f_complete)
for line in f_complete_complementary.table:
    print(line)
print(f_complete_complementary.is_deterministic)'''
