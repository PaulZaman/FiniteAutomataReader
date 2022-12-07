from displayfunctions import *
# This file contains Finite automata class
# word test algorithm is at bottom of class


class FiniteAutomata:
    def __init__(self, fa_filename=None, table=None, final_states=None, initial_states=None):
        if fa_filename:
            self.fa_file = fa_filename
            self.get_array_from_file()
            self.n_transitions = self.fa_array[4]
            self.get_initial_states_from_fa_array()
            self.get_final_states_from_fa_array()
            self.get_alphabet()
            self.get_table_from_array()
        if table:
            self.table = table
            self.final_states = final_states
            self.initial_states = initial_states
            self.alphabet = self.table[0][1:]

        self.get_list_of_states()
        self.is_it_asynchronous()
        self.is_it_deterministic()
        self.is_it_complete()

    # GETS
    def get_list_of_states(self):
        self.states = []
        for i in range(1, len(self.table)):
            self.states.append(self.table[i][0])

    def get_array_from_file(self):
        # creates an array containing an element(string) for each line of file
        self.fa_file = open(os.path.join(FA_folder, self.fa_file), "r")
        self.fa_array = self.fa_file.readlines()
        for idx in range(len(self.fa_array) - 1):
            self.fa_array[idx] = self.fa_array[idx][:-1]

    def get_final_states_from_fa_array(self):
        # creates a list containing final states
        self.final_states = self.fa_array[3].split(" ")
        self.final_states = self.final_states[1:]

    def get_initial_states_from_fa_array(self):
        # creates a list containing initial states
        self.initial_states = self.fa_array[2].split(" ")
        self.initial_states = self.initial_states[1:]

    def add_arrows_to_table(self):
        for line in self.table:
            if is_in_list(line[0], self.final_states):
                line[0] = "←" + line[0]
            if is_in_list(line[0].strip("←"), self.initial_states):
                line[0] = "→" + line[0]

    def remove_arrows_from_table(self):
        for line in self.table:
            if line[0] == "→":
                line[0] = line[1:]
            if line[0] == "←":
                line[0] = line[1:]

    def get_fa_array_from_fa_number(self, number):
        # creates a array containing a string for each line of the file
        self.fa_file = open(os.path.join(FA_folder, "Int-1-6-" + str(number)), "r")
        self.fa_array = self.fa_file.readlines()
        for i in range(len(self.fa_array) - 1):
            self.fa_array[i] = self.fa_array[i][:-1]
        return self.fa_array

    def get_alphabet(self):
        # creates alphabet list for particular automata
        self.alphabet = []
        for i in range(int(self.fa_array[0])):
            self.alphabet.append(chr(97 + i))

    def get_table_from_array(self):
        table = [[""]]

        # add first line
        for letter in self.alphabet:
            table[0].append(letter)

        # check if it needs an epsilon column
        for i in range(5, len(self.fa_array)):
            for character in self.fa_array[i]:
                if character == "*":
                    # add 'ε' columnif it dosen't exist
                    if table[0][len(table[0]) - 1] != 'ε':
                        table[0].append('ε')
                        for k in range(1, len(table)):
                            table[k].append('')
                    self.is_asynchronous = True

        # add states(first column) to table and fill the rest with empty spaces
        for i in range(1, int(self.fa_array[1]) + 1):
            table.append([str(i - 1)])
            for j in range(len(table[0]) - 1):
                table[i].append("")

        # fill rest of the table
        for i in range(5, len(self.fa_array)):  # iterate through array
            transition = self.fa_array[i]
            for chr_idx in range(len(transition)):
                if is_in_list(transition[chr_idx], self.alphabet):  # iterate through transition
                    from_ = int(transition[:chr_idx])  # left of transition
                    to_ = transition[1 + chr_idx:]  # right of transition
                    if len(table[1 + from_][1 + self.alphabet.index(transition[chr_idx])]) >= 1:
                        # add ", " if transition already exists
                        table[1 + from_][1 + self.alphabet.index(transition[chr_idx])] += ","
                    table[1 + from_][1 + self.alphabet.index(transition[chr_idx])] += to_  # add transition
                if transition[chr_idx] == '*':
                    # find from which state to which state
                    from_ = int(transition[:chr_idx])
                    to_ = transition[1 + chr_idx:]
                    if len(table[1 + from_][len(table[0]) - 1]) >= 1:
                        # add ", " if transition already exists
                        table[1 + from_][len(table[0]) - 1] += ","
                    table[1 + from_][len(table[0]) - 1] += to_  # add transition

        # Add '--' to empty spaces
        for i in range(1, len(table)):
            for k in range(len(table[0])):
                if table[i][k] == "":
                    table[i][k] = "--"

        self.table = table

    def is_renamed(self):
        for i in range(1, len(self.table)):
            if len(self.table[i][0]) > 1 or self.table[i][0] == 'P':
                return False
        return True

    # Deterministic, complete and asynchronous check
    def is_it_deterministic(self):
        if len(self.initial_states) > 1:
            self.is_deterministic = False
            self.why_is_not_deterministic = "Automaton has mutiple entries"
            return
        for line in self.table:
            for i in range(1, 2):
                if len(line[i].split(",")) > 1:
                    self.is_deterministic = False
                    self.why_is_not_deterministic = "State " + str(line[0]) + " has a multiple transition"
                    return
        self.is_deterministic = True
        self.why_is_not_deterministic = None

    def is_it_complete(self):
        if not self.is_deterministic:
            self.is_complete = False
            self.why_is_not_complete = "FA is not deterministic"
            return
        for line in self.table:
            for i in range(1, len(line)):
                if line[i] == "--":
                    self.is_complete = False
                    self.why_is_not_complete = "FA is missing transition at state " + line[0]
                    return
        self.is_complete = True
        self.why_is_not_complete = None

    def is_it_asynchronous(self):
        if self.table[0][len(self.table[0])-1] == 'ε':
            # find what make this automata asynchronous
            states_that_make_it_asynchronous = []
            for i in range(1, len(self.table)):
                self.why_is_asynchronous = "Because of states : "
                if self.table[i][len(self.table[0])-1] != '--':
                    states_that_make_it_asynchronous.append(self.table[i][0])
            self.why_is_asynchronous = "Because of states : "+list_to_string(states_that_make_it_asynchronous)
            self.is_asynchronous = True
            return
        self.is_asynchronous = False
        self.why_is_asynchronous = ""
        return

    # displays for menu screen
    def display_on_screen(self, screen, x_pos, y_pos, w, h, text_size=20):
        if len(self.table) >= 15:
            text_size = 14
        
        self.add_arrows_to_table()
        # get size of small block in our table
        w_block_size = w / len(self.table[0])
        h_block_size = h / len(self.table)

        # draw vertical lines lines
        for x in range(x_pos, x_pos + w+1, int(w_block_size)):
            pg.draw.line(screen, black, (x, y_pos), (x, y_pos + h))
        # draw horizontal lines
        for i in range(len(self.table)+1):
            pg.draw.line(screen, black, (x_pos, y_pos + i * h_block_size), (x_pos + w, y_pos + i * h_block_size))


        # fill table with info
        for i in range(len(self.table)):
            ##### RIGHT ARROW
            if len(self.table[i][0]) > 1 and self.table[i][0][0] == "→":
                draw_right_arrow(screen, black, (x_pos - 40, y_pos + h_block_size / 2 + int(i) * h_block_size - 5),
                                 (x_pos, y_pos + h_block_size / 2 + int(i) * h_block_size - 5),
                                 width=3)
                self.table[i][0] = self.table[i][0][1:]

            #### LEFT ARROW
            if len(self.table[i][0]) > 1 and self.table[i][0][0] == "←":
                draw_left_arrow(screen, black, (x_pos, y_pos + h_block_size / 2 + int(i) * h_block_size + 5),
                                (x_pos - 40, y_pos + h_block_size / 2 + int(i) * h_block_size + 5),
                                width=3)
                self.table[i][0] = self.table[i][0][1:]

            ##### Info
            for j in range(len(self.table[0])):
                x = x_pos + w_block_size / 2 + j*w_block_size
                y = y_pos + i*h_block_size+h_block_size/2
                draw_text(screen, self.table[i][j], text_size, red, x,y, nogrid=True, table=True)


        self.remove_arrows_from_table()

    def display_run(self, screen, x_pos, y_pos, w, h, word):
        run = self.run_word(word)
        if not run:
            return
        table = run[0]
        msg = run[1]
        draw_text(screen, msg, 20, red, x_pos + w / 2, y_pos + h + 10, nogrid=True)
        # column names
        draw_text(screen, "Step n°", 20, black, x_pos + w/10, y_pos - 20, nogrid=True)
        draw_text(screen, "State n°", 20, black, x_pos + w/2, y_pos - 20, nogrid=True)
        draw_text(screen, "Letter", 20, black, x_pos + 9*w/10, y_pos - 20, nogrid=True)
        # vertical lines
        pg.draw.aaline(screen, black, (x_pos, y_pos), (x_pos, y_pos+h))
        pg.draw.aaline(screen, black, (x_pos+1*w/5, y_pos), (x_pos+1*w/5, y_pos+h))
        pg.draw.aaline(screen, black, (x_pos + 4*w/5, y_pos), (x_pos + 4 * w / 5, y_pos + h))
        pg.draw.aaline(screen, black, (x_pos + w, y_pos), (x_pos + w, y_pos + h))
        #horizontal lines
        for y in range(y_pos, y_pos+h+1, int(h/len(table))):
            pg.draw.line(screen, black, (x_pos, y), (x_pos+w, y))
        # fill table
        for row in range(len(table)):
            draw_text(screen, table[row][0], 20, black, x_pos + w * 1 / 10, y_pos+(h/len(table))/2 + row*h/len(table), nogrid=True, table=True)
            draw_text(screen, table[row][1], 20, blue, x_pos + w * 1 / 2, y_pos + (h / len(table)) / 2 +row*h/len(table), nogrid=True,table=True)
            draw_text(screen, table[row][2], 20, blue, x_pos + w * 9 / 10, y_pos + (h / len(table)) / 2+ row*h/len(table), nogrid=True,table=True)

    # word test
    def run_word(self, word):
        # returns result of test under this form
        # result = [
        #    ["iteration n°0", [current_states], letter],
        #    ["iteration n°1", [current_states], letter],
        #    ["iteration n°2", [current_states], letter],
        result = []
        current_states = self.initial_states
        if self.is_asynchronous:
            current_states = self.pass_through_epsilon_states(current_states)

        # first line
        string_of_current_states = list_to_string(current_states)
        if string_of_current_states == '':
            string_of_current_states = '--'
        result.append(['0', string_of_current_states])

        # other lines
        for i in range(len(word)):
            # run through states
            if self.is_asynchronous:
                current_states = self.pass_through_epsilon_states(current_states)
            current_states = self.run_letter(word[i], current_states)
            if self.is_asynchronous:
                current_states = self.pass_through_epsilon_states(current_states)


            # create string from new states
            string_of_current_states = list_to_string(current_states)

            # add to result
            if string_of_current_states == '':
                string_of_current_states = '--'
            result.append([str(i+1), string_of_current_states])
            if string_of_current_states == '':
                i = len(word)-1

        # add letter to table
        for i in range(len(result)-1):
            result[i].append(word[i])

        # check if word exited or no:
        result[len(result)-1].append('--')

        # if word has already died
        if len(current_states) == 0:
            result = result[:-1]

        # if word is at exit
        for state in current_states:
            if is_in_list(state, self.final_states):
                return result, "Exited state : "+state

        # find last states before death of word
        for i in range(len(result)):
            if result[len(result)-1-i][1] != '--':
                return result, "Died states : " + str(result[len(result)-1-i][1])

        last_states = list_to_string(current_states)
        return result, "Died states : " + str(last_states)

    def run_letter(self, letter, current_states):
        next_states = []
        for state in current_states:
            states = self.run_letter_through_state(letter, state)
            if states:
                for state_ in states:
                    next_states.append(state_)
        return next_states

    def run_letter_through_state(self, letter, state):
        # find column and row index corresponding to the letter and state
        column1 = []
        for line in self.table:
            column1.append(line[0])
        column_idx = self.table[0].index(letter)
        line_idx = column1.index(state)

        if self.table[line_idx][column_idx].split(',') != ['--']:
            return self.table[line_idx][column_idx].split(',')
        else:
            return None

    def pass_through_epsilon_states(self, current_states):
        for state in current_states:
            next = self.run_letter_through_state('ε', state)
            if next:
                for state_ in next:
                    if not is_in_list(state_, current_states):
                        current_states.append(state_)
        return current_states

    def check_word(self, word):
        if word == "":
            return True

        for letter in word:
            if not is_in_list(letter, self.alphabet):
                return False
        return True



'''print("")
#f.pass_through_epsilon_states(['0', '3'])
#f.run_letter('a', ['0', '1', '2'])
res = f.run_word('ababcc')
for line in res[0]:
    print(line)
print(res[1])'''

