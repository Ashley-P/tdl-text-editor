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
    Gets pushed to the window and then blitted to the console
    '''

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
        # First character of a line
        if len(self.text[cursor.getpos()[1]]) == 0:
            self.text[cursor.getpos()[1]] = char
        else:
            self.text[cursor.getpos()[1]] = (self.text[cursor.getpos()[1]][:cursor.getpos()[0]] +
            char + 
            self.text[cursor.getpos()[1]][cursor.getpos()[0]:])

    def delchar(self):
        '''Deletes a character from the buffer'''
        # First character of a line
        if len(self.text[cursor.getpos()[1]]) == 1:
            self.text[cursor.getpos()[1]] = ''
        else:
            self.text[cursor.getpos()[1]] = (self.text[cursor.getpos()[1]][:cursor.getpos()[0] - 1] +
            self.text[cursor.getpos()[1]][cursor.getpos()[0]:])

    def newline(self):
        self.text.append('')
        cursor.setpos(dx=0)
        cursor.move(0, 1)

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

    def setpos(self, dx=None, dy=None):
        '''Directly set the position of the cursor on the screen
        If No value is passed, then the cursor just moves along
        that axis
        '''
        if dx == None:
            pass
        else:
            self.x = dx
        
        if dy == None:
            pass
        else:
            self.y = dy

    def getpos(self):
        '''Gets the position of the cursor and returns it as a tuple'''
        return (self.x, self.y)


def handle_keys():
    '''Handles all the keypresses.
    Certain commands are defined here because they won't be used elsewhere
    '''

    def up():
        # Moving the cursor upwards if cursor position y isn't 0
        if cursor.getpos()[1] != 0:
            # Moving the cursor to the left is the line above is shorter than the current one
            if (len(current_buffer.text[cursor.getpos()[1]]) >
                len(current_buffer.text[cursor.getpos()[1] - 1])):

                cursor.setpos(dx=len(current_buffer.text[cursor.getpos()[1] - 1]))
                cursor.move(0, -1)
            else:
                cursor.move(0, -1)
        else:
            pass

    def down():
        # Moving the cursor downwards if the cursor position y isn't the last line in the buffer
        if cursor.getpos()[1] != (len(current_buffer.text) - 1):
            # Moving the cursor to the left is the line below is shorter than the current one
            if cursor.getpos()[0] > len(current_buffer.text[cursor.getpos()[1] + 1]):
                cursor.setpos(dx=len(current_buffer.text[cursor.getpos()[1] + 1]))
                cursor.move(0, 1)
            else:
                cursor.move(0, 1)
        else:
            pass

    def left():
        if cursor.getpos()[0] == 0:
            if cursor.getpos()[1] != 0:
                cursor.setpos(dx=len(current_buffer.text[cursor.getpos()[1] - 1]))
                cursor.move(0, -1)
            else:
                pass
        else:
            cursor.move(-1, 0)

    def right():
        if cursor.getpos()[0] == len(current_buffer.text[cursor.getpos()[1]]):
            if cursor.getpos()[1] < (len(current_buffer.text) - 1):
                cursor.setpos(dx=0)
                cursor.move(0, 1)
            else:
                pass
        else:
            cursor.move(1, 0)

    def space():
        current_buffer.addchar(' ')
        cursor.move(1, 0)

    def backspace():
        # Backspacing an empty line
        if (cursor.getpos()[0] == 0 and 
                cursor.getpos()[1] != 0 and 
                current_buffer.text[cursor.getpos()[1]] == ''):

            left()
            del current_buffer.text[cursor.getpos()[1] + 1] 

        # Pressing backspace when the cursor is at (0, y != 0)
        elif cursor.getpos()[0] == 0 and cursor.getpos()[1] != 0:
            # A temporary value used to move the cursor into the correct position later
            temp = len(current_buffer.text[cursor.getpos()[1] - 1])
            
            # Appending the line the cursor is on to the above line and then deleting it
            current_buffer.text[cursor.getpos()[1] - 1] = (current_buffer.text[cursor.getpos()[1] - 1] +
            current_buffer.text[cursor.getpos()[1]])
            del current_buffer.text[cursor.getpos()[1]]

            # Moving the cursor upwards and to the correct position in the x axis
            cursor.setpos(dx=temp)
            cursor.move(0, -1)

        # Normal Backspacing
        elif cursor.getpos()[0] != 0:
            current_buffer.delchar()
            cursor.move(-1, 0)

        else:
            pass

    def enter():
        pass



    commands = {'UP'       : up,
                'DOWN'     : down,
                'LEFT'     : left,
                'RIGHT'    : right,
                'SPACE'    : space,
                'BACKSPACE': backspace,
                'ENTER'    : current_buffer.newline}


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
                # Don't indent this
                cursor.move(1, 0)

            else:
                commands.get(user_input.keychar, lambda: None)()

            keypress = True
        if not keypress: # Because it is realtime
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
        current_buffer.clear()
        
        handle_keys()
