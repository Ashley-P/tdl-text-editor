import tdl
import keybinds



#############
# Constants #
#############
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 60
ALPHA = 'abcdefghijklmnopqrstuvwxyz'

############
# Keybinds #
############

class Buffer(object):
    '''Holds, all the text that is supposed to be displayed on screen.
       Gets pushed to the window and then blitted to the console'''

    def __init__(self, text):
        self.text = text
        self.colour = 0xFFFFFF

    def draw(self):
        '''Draws the buffer to the console'''
        for i in range(len(self.text)):
            for j in range(len(self.text[i])):
                con.draw_char(j, i, self.text[i][j], self.colour, bg = None) 

    def clear(self):
        '''Clears the buffer from the console'''
        for i in range(len(self.text)):
            for j in range(len(self.text[i])):
                con.draw_char(j, i, ' ', self.colour, bg = None) 

    def addchar(self, char):
        '''Adds a character to the buffer'''
        if len(self.text[0]) == 0:
            self.text[0] = char
        else:
            self.text[0] = self.text[0][:cursor.getpos()[0]] + char + self.text[0][cursor.getpos()[0]:]
        cursor.move(1, 0)

    def delchar(self):
        if len(self.text[0]) == 0:
            pass
        else:
            try:
                self.text[0] = self.text[0][:cursor.getpos()[0]] + self.text[0][cursor.getpos()[0] + 1]
            except IndexError:
                self.text[0] = self.text[0][:-1]
            finally:
                cursor.move(-1, 0)


class Cursor(object):
    '''Dictates where the keybindings are invoked'''

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.char = '221'
        self.colour = 0xFFFFFF

    def draw(self):
        '''Draws the cursor'''
        con.draw_char(self.x, self.y, self.char, self.colour, bg=None)

    def clear(self):
        '''Erase the cursor'''
        con.draw_char(self.x, self.y, ' ', self.colour, bg=None)

    def move(self, dx, dy):
        '''Moves the cursor by the given amount'''
        self.x += dx
        self.y += dy

    def setpos(self, dx, dy):
        '''Directly set the position of the cursor on the screen'''
        self.x = dx
        self.y = dy

    def getpos(self):
        '''Gets the position of the cursor and returns it as a tuple'''
        return (self.x, self.y)


def handle_keys():
    commands = {'SPACE'    : lambda:current_buffer.addchar(' '),
                'BACKSPACE': current_buffer.delchar}

    keypress = False
    for event in tdl.event.get(): # Getting events
        if event.type == 'KEYDOWN': # Making sure the event is a keypress
            user_input = event
            
            # All keybinds go here
            if len(user_input.keychar) == 1: # For single characters
                if user_input.shift == True:
                    # While pressing shift
                    current_buffer.addchar(keys.shift_char.get(user_input.keychar, '?'))
                else:
                    # Without pressing shift
                    current_buffer.addchar(keys.normal_char.get(user_input.keychar, '?'))

            else:
                commands.get(user_input.keychar, nothing)()

            keypress = True
        if not keypress: # Because it is realtime
            return


def nothing():
    pass



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
    buffer1 = Buffer(['']) # Passing an empty array with an empty string
    keys = keybinds.Keybinds()
    current_buffer = buffer1

    # main loop 
    while not tdl.event.is_window_closed():

        current_buffer.draw()
        cursor.draw()

        root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        tdl.flush()

        cursor.clear()
        handle_keys()
