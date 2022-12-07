from listfunctions import *
# This file contains basic menu functions such as draw text and button
#basic menu functions

def return_to_menu(screen):
    # This function creates a button for returning to menu,
    # returns next action if button is pressed
    restart = button(screen, "Return to menu", black, less_white, GRIDWIDTH/2, 32, 13, 2)
    if restart == "Return to menu":
        return restart

def draw_text(screen, text, size, color, x, y, nogrid=False, midtop=True, table=False):
    # This function draws text on screen, and dosen't return anything
    font = pg.font.Font('freesansbold.ttf', size)
    text_surface = font.render(text, True, color)
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    text_rect = text_surface.get_rect()
    if midtop:
        if not nogrid:
            text_rect.midtop = (x * TILESIZE, y * TILESIZE)
        if nogrid:
            if table:
                text_rect.midtop = (x, y - text_height/2)
            else:
                text_rect.midtop = (x, y)
    else:
        if not nogrid:
            text_rect.topleft = (x * TILESIZE, y * TILESIZE)
        if nogrid:
            text_rect.topleft = (x, y)

    screen.blit(text_surface, text_rect)

def draw_grid(screen):
    # This function draws grid on screen (only used while develloping)
    for x in range(0, screen_width, TILESIZE):
        pg.draw.line(screen, light_blue, (x, 0), (x, screen_height))
    for y in range(0, screen_height, TILESIZE):
        pg.draw.line(screen, light_blue, (0, y), (screen_width, y))

def button(screen, text, button_color, text_color, x, y, w, h, border_radius=10, text_size=30):
    # This function creates a button on screen
    # it returns the text of the button if it is pressed, and none otherwise
    # changes the color of box when mouse is hovering over it
    x = x*TILESIZE
    y = y*TILESIZE
    w = w*TILESIZE
    h = h*TILESIZE
    mouse = pg.mouse.get_pos()
    rect = pg.rect.Rect(0, 0, w, h)
    rect.midtop = (x, y)
    if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height:
        button_color = grey
        pg.event.get()
        click = pg.mouse.get_pressed()
        if click[0] == 1:
            return text
    pg.draw.rect(screen, button_color, rect, border_radius=border_radius)
    if text_size >= 30:
        draw_text(screen, text, text_size, text_color, x, 5 + y, True)
    else:
        draw_text(screen, text, text_size, text_color, x, y, True)

def text_button(screen, text, text_color, x, y, w, h):
    # This function is similar to button, but does not create a box for the button,
    # it simply uses the text
    # it returns the text of the button if it is pressed, and none otherwise
    # changes the color of text when mouse is hovering over it
    mouse = pg.mouse.get_pos()
    rect = pg.rect.Rect(0, 0, w * TILESIZE, h * TILESIZE)
    rect.midtop = (x * TILESIZE, y * TILESIZE)
    if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height:
        text_color = less_white
        pg.event.get()
        if pg.mouse.get_pressed()[0] == 1:
            return text
    draw_text(screen, text, 25, text_color, x * TILESIZE, y * TILESIZE, True)

def switch(screen, x, y, w, h, state, color):
    # this function creates a on/off switch, a bit like a radio button
    # returns the stated of the button: on or off
    # changes color when pressed
    mouse = pg.mouse.get_pos()
    rect = pg.rect.Rect(0, 0, w * TILESIZE, h * TILESIZE)
    rect.midtop = (x * TILESIZE, y * TILESIZE)
    pg.event.get()
    click = pg.mouse.get_pressed()

    if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height and click[0] == 1:
        if not state:
            time.sleep(0.2)
            state = True
        else:
            time.sleep(0.2)
            state = False

    if state:
        text = "ON"
    else:
        text = "OFF"
        color = black

    pg.draw.rect(screen, color, rect)
    draw_text(screen, text, 30, white, x * TILESIZE, 5 + y * TILESIZE, True)
    return state

def text_box(screen, text, x, y, w, h, time):
    # creates a text box with inputted text
    # makes box grow as text is growing
    # creates a vertical white bar to animate a bit
    x = x*TILESIZE
    y = y*TILESIZE
    w = w*TILESIZE
    h = h*TILESIZE
    font = pg.font.Font('freesansbold.ttf', 25)
    text_surface = font.render(text, True, white)
    text_box.text_width = text_surface.get_width()
    text_box.text_rect = text_surface.get_rect()
    text_box.text_rect.midtop = (x, 5+y)

    if text_box.text_width+40 > w:
        w = 40 + text_box.text_width
    rect = pg.rect.Rect(0, 0, w, h)
    rect.midtop = (x, y)
    pg.draw.rect(screen, black, rect)
    if (pg.time.get_ticks() - time)%500 < 250:
        pg.draw.line(screen, white, (x + text_box.text_width/2, y), (x+text_box.text_width/2, y + 40), 3)

    screen.blit(text_surface, text_box.text_rect)

def img_button(screen, name, imgunpressed, imgpressed, x, y, w=0, h=0, decalage=43):
    # This function creates a button on screen with an image
    # it returns the text of the button if it is pressed
    # changes the image when mouse is hovering over it
    x = x*TILESIZE
    y = y*TILESIZE
    w = w*TILESIZE
    h = h*TILESIZE
    mouse = pg.mouse.get_pos()
    if w!= 0 and h!=0:
        imgpressed = pg.transform.scale(imgpressed, (w, h))
        imgunpressed = pg.transform.scale(imgunpressed, (w, h))

    rect = imgunpressed.get_rect()
    rect.midtop = (x + decalage, y)
    #pg.draw.rect(screen, red, rect)

    if rect.x < mouse[0] < rect.x + rect.width and rect.y < mouse[1] < rect.y + rect.height:
        screen.blit(imgpressed,  (x, y))
        pg.event.get()
        click = pg.mouse.get_pressed()
        if click[0] == 1:
            return name
    else:
        screen.blit(imgunpressed, (x, y))

def animate_table(x,y,w,h, x_final,y_final,w_final,h_final, proportion):
    x = x + (x_final-x) * proportion/100
    y = y + (y_final - y) * proportion / 100
    w = w + (w_final - w) * proportion / 100
    h = h + (h_final - h) * proportion / 100
    return x, y, w,h

def move_tables_left(fa1_x, fa2_x, fa3_x):
    fa1_x_obj = -350
    fa2_x_obj = 50
    fa3_x_obj = 450
    fa1_x = fa1_x - (fa1_x - fa1_x_obj)*0.1
    fa2_x = fa2_x - (fa2_x - fa2_x_obj) * 0.1
    fa3_x = fa3_x - (fa3_x - fa3_x_obj) * 0.1
    return int(fa1_x), int(fa2_x), int(fa3_x)

def draw_right_arrow(screen, color, startpos, endpos, width=10):
    length = math.sqrt((startpos[0]-endpos[0])*(startpos[0]-endpos[0]) + (startpos[1]-endpos[1])*(startpos[1] - endpos[1]))

    pg.draw.polygon(screen, color, (
        startpos,
        (startpos[0], startpos[1] +width/2),
        (startpos[0] + length * 0.8, startpos[1] + width/2),
        (startpos[0] + length * 0.8, startpos[1] + 2*width),
        endpos,
        (startpos[0] + length * 0.8, startpos[1] - 2 * width),
        (startpos[0] + length * 0.8, startpos[1] - width / 2),
        (startpos[0], startpos[1] - width / 2),
    ))

def draw_left_arrow(screen, color, startpos, endpos, width=10):
    length = math.sqrt((startpos[0]-endpos[0])*(startpos[0]-endpos[0]) + (startpos[1]-endpos[1])*(startpos[1] - endpos[1]))

    pg.draw.polygon(screen, color, (
        startpos,
        (startpos[0], startpos[1] -width/2),
        (startpos[0] - length * 0.8, startpos[1] - width/2),
        (startpos[0] - length * 0.8, startpos[1] - 2*width),
        endpos,
        (startpos[0] - length * 0.8, startpos[1] + 2 * width),
        (startpos[0] - length * 0.8, startpos[1] + width / 2),
        (startpos[0], startpos[1] + width / 2),
    ))