import tdl



SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
AlPHA = 'abcdefghijklmnopqrstuvwxyz'



class Buffer(object):
    '''Holds, all the text that is supposed to be displayed on screen.
       Gets pushed to the window and then blitted to the console'''

    def __init__(self, text):
        self.text = text
        self.colour = 0xFFFFFF

    def draw(self):
        for i in range(len(self.text)):
            for j in range(len(self.text[i])):
                con.draw_char(j, i, self.text[i][j], self.colour, bg = None) 

    def clear(self):
        pass

    def addchar(self, char):
        if self.text[0] == '':
            self.text[0] = char
        else:
            self.text[0] = self.text[0][:cursor.getpos()[0]] + char + self.text[0][cursor.getpos()[0]:]

        cursor.move(1, 0)
        print(cursor.getpos())
        print(self.text)


class Cursor(object):
    '''Dictates where the keybindings are invoked'''

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.char = 221
        self.colour = 0xFFFFFF

    def draw(self):
        # Draws the cursor
        con.draw_char(self.x, self.y, self.char, self.colour, bg=None)

    def clear(self):
        # Erase the cursor
        con.draw_char(self.x, self.y, ' ', self.colour, bg=None)

    def move(self, dx, dy):
        # Moves the cursor by the given amount
        self.x += dx
        self.y += dy

    def setpos(self, dx, dy):
        self.x = dx
        self.y = dy

    def getpos(self):
        return (self.x, self.y)


def handle_keys():
    
    keypress = False
    for event in tdl.event.get():
        if event.type == 'KEYDOWN':
            user_input = event
            print(user_input.keychar)
            if len(user_input.keychar) == 1:
                current_buffer.addchar(user_input.keychar)
            else:
                pass
            keypress = True
        if not keypress:
            return


##############################
# Initialisation & Main Loop #
############################## 
if __name__ == "__main__":
    tdl.set_font('terminal16x16_gs_ro.png', greyscale=True, altLayout=False)
    root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="tdl text editor", fullscreen=False)
    con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
    tdl.setFPS(LIMIT_FPS)

    # Other initialisation
    cursor = Cursor(0, 0) # Invoking the cursor, you should only have to do this once
    buffer1 = Buffer(['']) # Passing an empty array because that's how I have styled the system
    current_buffer = buffer1

    # main loop 
    while not tdl.event.is_window_closed():

        cursor.draw()
        current_buffer.draw()

        root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        tdl.flush()

        cursor.clear()
        handle_keys()
