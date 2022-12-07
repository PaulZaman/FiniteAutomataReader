from minimization import *

# This file contains Menu class
# Used only for displaying information

class Menu:
    def __init__(self):
        self.action = "Start screen"
        pg.init()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption(Title)
        self.clock = pg.time.Clock()
        self.get_automata_list()
        self.old_automaton = None
        self.older_automaton = None
        self.expand = False
        self.automaton = None
        self.mainloop()

    def get_automata_list(self):
        self.file_list = []
        for file in os.listdir(FA_folder):
            try:
                if 0 < int(file[-2:]) < 50:
                    self.file_list.append(file)
            except:
                pass
        self.file_list = order_list(self.file_list)

    def draw_info_about_automaton(self, automaton, buttons=False):
        # Deterministic
        draw_text(self.screen, 'Is deterministic :', 25, black, 7, 22)
        draw_text(self.screen, str(automaton.is_deterministic), 25, red, 7, 23.5)
        draw_text(self.screen, automaton.why_is_not_deterministic, 15, black, 7, 26)
        # Asynchronous
        draw_text(self.screen, 'Is asynchronous :', 25, black, 20, 22)
        draw_text(self.screen, str(automaton.is_asynchronous), 25, red, 20, 23.5)
        draw_text(self.screen, automaton.why_is_asynchronous, 15, black, 20, 25)
        # Complete
        draw_text(self.screen, 'Is Complete :', 25, black, 33, 22)
        draw_text(self.screen, str(automaton.is_complete), 25, red, 33, 23.5)
        draw_text(self.screen, automaton.why_is_not_complete, 15, black, 33, 26)
        # buttons
        if buttons:
            if not automaton.is_asynchronous:
                if not automaton.is_deterministic:
                    if button(self.screen, "Determinize", white, black, 7, 27, 9, 2):
                        self.older_automaton = self.old_automaton
                        self.old_automaton = automaton
                        self.automaton = determinize(automaton)
                        self.set_coords_for_table()
                        time.sleep(0.2)
                if not automaton.is_complete:
                    if not automaton.is_deterministic:
                        draw_text(self.screen, "To Complete,", 20, red, 33, 27)
                        draw_text(self.screen, "determinize first", 20, red, 33, 28)
                    else:
                        if button(self.screen, "Complete", white, black, 33, 27, 9, 2):
                            self.older_automaton = self.old_automaton
                            self.old_automaton = automaton
                            self.automaton = complete(automaton)
                            self.set_coords_for_table()
                            time.sleep(0.2)
            if automaton.is_complete:
                if button(self.screen, "Complementarize", white, black, 20, 26.5, 11, 1, text_size=20):
                    self.older_automaton = self.old_automaton
                    self.old_automaton = automaton
                    self.automaton = complementarize(automaton)
                    self.set_coords_for_table()
                    time.sleep(0.2)

            else:
                draw_text(self.screen, "Before complementarization", 17, black, 20, 25.8)
                draw_text(self.screen, "Automaton has to be complete", 17, black, 20, 26.5)
            if button(self.screen, "Rename", white, black, 7, 30, 11, 2):
                self.older_automaton = self.old_automaton
                self.old_automaton = automaton
                self.automaton = rename_states(automaton)
                self.set_coords_for_table()
                time.sleep(0.2)
            if automaton.is_complete and automaton.is_deterministic and not automaton.is_asynchronous \
                    and automaton.is_renamed():
                if self.minimized:
                    draw_text(self.screen, "FA is already Minimized", 20, red, 33, 30)
                elif button(self.screen, "Minimize", white, black, 33, 30, 11, 2):
                    minimized = minimize(automaton)
                    if minimized:
                        self.automaton = minimized
                        self.older_automaton = self.old_automaton
                        self.old_automaton = automaton
                    self.minimized = True
                    self.set_coords_for_table()
                    time.sleep(0.2)


            else:
                draw_text(self.screen, "To minimize, automaton has to be", 17, black, 33, 30)
                draw_text(self.screen, "-deterministic", 17, black, 30, 31, midtop=False)
                draw_text(self.screen, "-complete", 17, black, 30, 32, midtop=False)
                draw_text(self.screen, "-renamed", 17, black, 30, 33, midtop=False)

    def display_files_on_screen(self):
        ## Cut list of files into 4
        list1, list2, list3, list4 = divide_list_into4(self.file_list)
        i = 10  ## column 1
        for file in list1:
            if text_button(self.screen, "FA n°" + file[-2:], black, 8, i, 4, 1):
                self.file_to_read = file
                self.action = "Display"
                time.sleep(0.2)
                # self.automaton = Finite_automata()
            i += 20 / len(list1)

        i = 10  ## column 1
        for file in list2:
            if text_button(self.screen, "FA n°" + file[-2:], black, 16, i, 4, 1):
                self.file_to_read = file
                self.action = "Display"
                time.sleep(0.2)
                # self.automaton = Finite_automata()
            i += 20 / len(list2)

        i = 10  ## column 1
        for file in list3:
            if text_button(self.screen, "FA n°" + file[-2:], black, 24, i, 4, 1):
                self.file_to_read = file
                self.action = "Display"
                time.sleep(0.2)
                # self.automaton = Finite_automata()
            i += 20 / len(list3)

        i = 10  ## column 2
        for file in list4:
            if text_button(self.screen, "FA n°" + file[-2:], black, 32, i, 4, 1):
                self.file_to_read = file
                self.action = "Display"
                time.sleep(0.2)
            i += 20 / len(list4)

    def mainloop(self):
        run = True
        self.file_to_read = None
        self.word = ""
        self.launch = pg.time.get_ticks()

        while run:
            self.screen.blit(Main_menubg, (0, 0))
            draw_text(self.screen, "MENU", 40, black, GRIDWIDTH / 2, 2)


            if self.action == "Modify":
                self.modify()
            if self.action == "Choose file":
                self.chooseFA_file()
            if self.action == "Start screen":
                self.start_screen()
            if self.action == "Display":
                self.display_FA()
            if self.action == "Information":
                self.get_info()
            if self.action == "STOP":
                run = False
            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return "STOP"

    def set_coords_for_table(self):
        self.fa1_x, self.fa2_x, self.fa3_x = 50, 450, 850

    ## SCREENS
    def start_screen(self):
        if button(self.screen, "Test an FA", black, white, GRIDWIDTH / 2, 13, 10, 2):
            time.sleep(0.2)
            self.action = "Choose file"
        if button(self.screen, "INFO", black, white, GRIDWIDTH / 2, 16, 6, 2):
            time.sleep(0.2)
            self.action = "Information"
        if button(self.screen, "EXIT", black, white, GRIDWIDTH / 2, 21, 5, 2):
            time.sleep(0.2)
            self.action = "STOP"

    def chooseFA_file(self):
        draw_text(self.screen, "Select base file :", 40, black, GRIDWIDTH / 2, 6)
        # this part is to draw on screen the title of the files
        self.display_files_on_screen()
        # if is going to display automaton, create automaton object
        if self.action == "Display":
            self.automaton = FiniteAutomata(self.file_to_read)
        if return_to_menu(self.screen):
            self.action = "Start screen"

    def display_FA(self):
        # display FA here
        #draw_grid(self.screen)
        draw_text(self.screen, "Finite Automata n°" + self.file_to_read[-2:], 30, black, 20, 4.5)
        if button(self.screen, "Expand", white, black, 35, 13, 6, 2):
            if self.expand:
                self.expand = False
            else:
                self.expand = True
            time.sleep(0.2)
        if self.expand:
            self.automaton.display_on_screen(self.screen, 200, 140, 400, 480)
        else:
            self.automaton.display_on_screen(self.screen, 200, 140, 400, 270)
            self.draw_info_about_automaton(self.automaton)

        # Action Panel
        if button(self.screen, "Modify", white, black, 35, 10, 6, 2):
            self.action = "Modify"

        if button(self.screen, "Run", white, black, 35, 16, 6, 2):
            if self.run(self.automaton) == "STOP":
                self.action = "STOP"

        # Return to menu button
        if return_to_menu(self.screen):
            self.action = "Start screen"
            self.file_to_read = None

        # back button
        if button(self.screen, "back", white, black, 32, 32, 4, 2):
            self.action = "Choose file"
            self.expand = False
            self.file_to_read = None

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.action = "STOP"

    def get_info(self):
        draw_text(self.screen, 'Project created by :', 30, black, 13, 6)
        draw_text(self.screen, '- Benjamin Rossignol', 30, black, 9, 9, midtop=False)
        draw_text(self.screen, '- Capucine Foucher', 30, black, 9, 11, midtop=False)
        draw_text(self.screen, '- Alexandre Dibon', 30, black, 9, 13, midtop=False)
        draw_text(self.screen, '- Paul Zamanian', 30, black, 9, 15, midtop=False)

        if return_to_menu(self.screen):
            self.action = "Start screen"

    def modify(self):
        self.fa1_x, self.fa2_x, self.fa3_x = -350, 50, 450
        self.minimized = False
        run = True
        while run:
            self.screen.blit(Main_menubg, (0, 0))
            draw_text(self.screen, "MENU", 40, black, GRIDWIDTH / 2, 2)

            draw_text(self.screen, "Finite Automata n°" + self.file_to_read[-2:], 30, black, GRIDWIDTH / 2, 4.5)
            self.draw_info_about_automaton(self.automaton, buttons=True)

            # draw automatons
            self.fa1_x, self.fa2_x, self.fa3_x = move_tables_left(self.fa1_x, self.fa2_x, self.fa3_x)
            if self.older_automaton:
                self.older_automaton.display_on_screen(self.screen, self.fa1_x, 140, 300, 270)
                self.old_automaton.display_on_screen(self.screen, self.fa2_x, 140, 300, 270)
                self.automaton.display_on_screen(self.screen, self.fa3_x, 140, 300, 270)
            elif self.old_automaton:
                self.fa2_x = 50
                self.old_automaton.display_on_screen(self.screen, self.fa2_x, 140, 300, 270)
                self.automaton.display_on_screen(self.screen, self.fa3_x, 140, 300, 270)
            else:
                self.automaton.display_on_screen(self.screen, self.fa2_x, 140, 300, 270)




            if self.automaton.is_asynchronous:
                    ## TODO display message saying we can't determinize or complete
                    pass

            if button(self.screen, "RUN", white, black, 17, 32, 4, 2):
                    time.sleep(0.2)
                    self.run(self.automaton)
            if button(self.screen, "back", white, black, 23, 32, 4, 2):
                    self.action = "Choose file"
                    self.file_to_read = None
                    self.old_automaton = None
                    self.older_automaton = None
                    self.automaton = None
                    time.sleep(0.2)
                    return
            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.action = "STOP"
                    return

    def run(self, automaton):
        run = True
        word = ''
        x, y, w, h = 200, 140, 400, 270
        while run:
            self.screen.blit(Main_menubg, (0, 0))  # BG
            draw_text(self.screen, "Run Screen", 40, black, GRIDWIDTH / 2, 2)

            # draw automaton
            automaton.display_on_screen(self.screen, int(x), int(y), int(w), int(h))
            x, y, w, h = animate_table(x, y, w, h, 50, 140, 300, 400, 10)
            # TEXT BOX AND RUN BUTTON
            text_box(self.screen, word, 10, 28, 5, 2, self.launch)
            if not automaton.check_word(word):
                draw_text(self.screen, "ERROR, character not in alphabet", 25, red, 10, 25)
            else:
                automaton.display_run(self.screen, 400, 140, 350, 400, word)
                pass

            if button(self.screen, "back", white, black, 20, 32, 4, 2):
                time.sleep(0.2)
                return
            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        word = word[:-1]
                    else:
                        word += event.unicode
                if event.type == pg.QUIT:
                    return "STOP"



m = Menu()

'''file_list = []
for file in os.listdir(FA_folder):
    try:
        if 0 < int(file[-2:]) < 50:
            file_list.append(file)
    except:
        pass

file_list = order_list(file_list)

for file in file_list:
    A = FiniteAutomata(fa_filename=file)
    print("Finite Automata N°", file[-2:])
    for line in A.table:
        print(line)
    print("initial : ", A.initial_states, ", final : ", A.final_states)
    print("")

    if not A.is_asynchronous:
        if not A.is_deterministic:
            A = determinize(A)
        if not A.is_complete:
            A = complete(A)
            A = rename_states(A)
        try:
            if minimize(A):
                A = minimize(A)
        except:
            pass

        print("Finite Automata N°", file[-2:], " minimized:")
        for line in A.table:
            print(line)
        print("initial : ", A.initial_states, ", final : ", A.final_states)
        print("")

    time.sleep(0.1)


'''