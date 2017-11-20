import tdl
import keybinds


#############
# Constants #
#############
MAIN_HEIGHT = 50
PANEL_HEIGHT = 2
SCREEN_WIDTH = 80
SCREEN_HEIGHT = MAIN_HEIGHT + PANEL_HEIGHT
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
LIMIT_FPS = 60


class Buffer(object):
    '''Holds, all the text that is supposed to be displayed on screen.
    Gets pushed to the window and then blitted to the console
    '''

    def __init__(self, text, window):
        self.text = text
        self.window = window
        self.colour = 0xFFFFFF
        self.bg = 0x000000


    def draw(self):
        '''Draws the buffer to the console'''
        for i in range(len(self.text)):
            for j in range(len(self.text[i])):
                self.window.draw_char(j, i, self.text[i][j], self.colour, bg=self.bg) 


    def addchar(self, char, x, y):
        '''Adds a character to the buffer'''
        # You can insert multiple characters with 1 call
        # First character of a line
        if len(self.text[y]) == 0:
            self.text[y] = char
        else:
            self.text[y] = (self.text[y][:x] + char + self.text[y][x:])


    def delchar(self, x, y):
        '''Deletes a character from the buffer'''
        # First character of a line
        self.text[y] = (self.text[y][:x - 1] + self.text[y][x:])


    def newline(self, y):
        '''Adds a new line'''
        # If at the end of the buffer
        if y == len(self.text):
            self.text.append('')
        else:
            self.text = self.text[:y] + [''] + self.text[y:]


class Cursor(object):
    '''Dictates where the keybindings are invoked'''

    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        self.window = window
        self.char = '221'
        self.colour = 0xFFFFFF
        self.bg = 0x000000


    def draw(self):
        '''Draws the cursor'''
        try:
            self.textchar = current_buffer.text[self.y][self.x] 
            if self.textchar != ' ':
                self.window.draw_char(self.x, self.y, self.textchar, self.bg, bg=self.colour)
            else:
                self.window.draw_char(self.x, self.y, self.char, self.colour, bg=self.colour)
        except IndexError:
            self.window.draw_char(self.x, self.y, self.char, self.colour, bg=self.colour)


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



class NormalKeybinds():
    '''Handles all the keypresses.
    Certain commands are defined here because they won't be used elsewhere
    curs_x == cursor.getpos()[0]
    curs_y == cursor.getpos()[1]
    '''

    def __init__(self):
        # Non-ASCII keypresses
        self.commands = {'UP'       : lambda : self.up(*cursor.getpos()),
                         'DOWN'     : lambda : self.down(*cursor.getpos()),
                         'LEFT'     : lambda : self.left(*cursor.getpos()),
                         'RIGHT'    : lambda : self.right(*cursor.getpos()),
                         'SPACE'    : lambda : self.space(*cursor.getpos()),
                         'BACKSPACE': lambda : self.backspace(*cursor.getpos()),
                         'ENTER'    : lambda : self.enter(*cursor.getpos()),
                         'TAB'      : lambda : self.tab(*cursor.getpos()),
                         'DELETE'   : lambda : self.delete(*cursor.getpos()),
                         'ESCAPE'   : self.escape}


    def up(self, curs_x, curs_y):
        '''Moves the cursor upwards except when on the top most line'''
        # Moving the cursor upwards if cursor position y isn't 0
        if curs_y != 0:
            # Moving the cursor to the left is the line above is shorter than the current one
            if curs_x > len(current_buffer.text[curs_y - 1]):
                cursor.setpos(dx=len(current_buffer.text[curs_y - 1]))
                cursor.move(0, -1)
            else:
                cursor.move(0, -1)
        else:
            pass


    def down(self, curs_x, curs_y):
        '''Moves the cursor Downwards, except when on the bottom most line'''
        # Moving the cursor downwards if the cursor position y isn't the last line in the buffer
        if curs_y != (len(current_buffer.text) - 1):
            # Moving the cursor to the left is the line below is shorter than the current one
            if curs_x > len(current_buffer.text[curs_y + 1]):
                cursor.setpos(dx=len(current_buffer.text[curs_y + 1]))
                cursor.move(0, 1)
            else:
                cursor.move(0, 1)
        else:
            pass


    def left(self, curs_x, curs_y):
        '''Moves the cursor to the left, except at the start of a line where it moves it
        upwards and to the end of that line
        '''
        if curs_x == 0:
            if curs_y != 0:
                cursor.setpos(dx=len(current_buffer.text[curs_y - 1]))
                cursor.move(0, -1)
            else:
                pass
        else:
            cursor.move(-1, 0)


    def right(self, curs_x, curs_y):
        '''Moves the cursor to the right, except at the end of a line where it moves it
        downwards and to the start of that line
        '''
        if curs_x == len(current_buffer.text[curs_y]):
            if curs_y < (len(current_buffer.text) - 1):
                cursor.setpos(dx=0)
                cursor.move(0, 1)
            else:
                pass
        else:
            cursor.move(1, 0)


    def space(self, curs_x, curs_y):
        '''Inserts a space at cursor position'''
        current_buffer.addchar(' ', curs_x, curs_y)
        cursor.move(1, 0)


    def backspace(self, curs_x, curs_y):
        '''Deletes a character at that cursor position and moves the cursor.
        Also deletes empty lines and appends the line above with the current line if
        curs_x == 0
        '''
        # Backspacing an empty line
        if (curs_x == 0 and curs_y != 0 and current_buffer.text[curs_y] == ''):
            del current_buffer.text[curs_y] 
            self.left(curs_x, curs_y)

        # Pressing backspace when the cursor is at (0, y != 0)
        elif curs_x == 0 and curs_y != 0:
            # A temporary value used to move the cursor into the correct position later
            temp = len(current_buffer.text[curs_y - 1])
            
            # Appending the line the cursor is on to the above line and then deleting it
            current_buffer.text[curs_y - 1] = (current_buffer.text[curs_y - 1] +
            current_buffer.text[curs_y])
            del current_buffer.text[curs_y]

            # Moving the cursor upwards and to the correct position in the x axis
            cursor.setpos(dx=temp)
            cursor.move(0, -1)

        # Normal Backspacing
        elif curs_x != 0:
            current_buffer.delchar(curs_x, curs_y)
            cursor.move(-1, 0)

        else:
            pass


    def enter(self, curs_x, curs_y):
        '''Creates a new line and moves the cursor down along with any characters
        to the right of the cursor
        '''
        # If the cursor is at the end of a line
        if curs_x == len(current_buffer.text[curs_y]):
            current_buffer.newline(curs_y + 1)

        else:
            current_buffer.newline(curs_y + 1)
            current_buffer.text[curs_y + 1] = current_buffer.text[curs_y][curs_x:]
            current_buffer.text[curs_y] = current_buffer.text[curs_y][:curs_x]

        # Don't indent this
        cursor.setpos(dx=0)
        cursor.move(0, 1)


    def tab(self, curs_x, curs_y):
        current_buffer.addchar('    ', curs_x, curs_y)
        cursor.move(4, 0)


    def delete(self, curs_x, curs_y):
        # Pressing Delete while at the end of a line
        if curs_y != len(current_buffer.text) - 1 and curs_x == len(current_buffer.text[curs_y]):
            current_buffer.text[curs_y] = (current_buffer.text[curs_y] +
                                           current_buffer.text[curs_y + 1])
            del current_buffer.text[curs_y + 1]
        else:
            current_buffer.delchar(curs_x + 1, curs_y)


    def escape(self):
        global current_keybinds
        global current_buffer
        global cursor
        current_keybinds = keybinds_list[1]
        cursor.window = panel
        cursor.setpos(0, 0)
        current_buffer = panel_buffer


    def nothing(self):
        pass


    def handle_keys(self):

        keypress = False
        for event in tdl.event.get(): # Getting events
            if event.type == 'KEYDOWN': # Making sure the event is a keypress
                user_input = event
                
                # All keybinds get called in this if statement
                if len(user_input.keychar) == 1: # For single characters

                    if user_input.shift == True:
                        # While pressing shift
                        current_buffer.addchar(keys.shift_char.get(user_input.keychar, '?'),
                                               *cursor.getpos())

                        cursor.move(1, 0)
                    else:
                        # Without pressing shift
                        current_buffer.addchar(keys.normal_char.get(user_input.keychar, '?'),
                                               *cursor.getpos())
                        cursor.move(1, 0)

                else:
                    self.commands.get(user_input.keychar, self.nothing)()

                keypress = True
            if not keypress: # Because it is realtime
                return


class CommandKeybinds(NormalKeybinds):
    '''Used for when you are on the command line'''

    def __init__(self):
        super().__init__()


    def enter(self, curs_x, curs_y):
        line = panel_buffer.text[0].split()
        self.parse_command(line[0], ' '.join(line[1:]))

    
    def parse_command(self, command, modifier):
        pass


def render_all():
    for each in buffers:
        each.draw()

    cursor.draw()
    panel.draw_str(0, 1, mode_message, 0xFF0000)

    root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
    root.blit(panel, 0, PANEL_Y, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0)
    tdl.flush()

    panel.clear()
    con.clear()

    
##############################
# Initialisation & Main Loop #
############################## 
if __name__ == "__main__":
    tdl.set_font('terminal16x16_gs_ro.png', greyscale=True, altLayout=False)
    root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="tdl text editor", fullscreen=False)
    con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
    panel = tdl.Console(SCREEN_WIDTH, PANEL_HEIGHT)
    tdl.setFPS(LIMIT_FPS)

    # Other initialisation
    cursor = Cursor(0, 0, con) # Invoking the cursor, you should only have to do this once
    buffer1 = Buffer([''], con) # Passing an array with an empty string
    panel_buffer = Buffer([''], panel) # For typing single lines at the bottom of the screen
    buffers = [buffer1, panel_buffer] # List of all the buffers so they render

    keys = keybinds.Keybinds() # Normal keys
    keybinds_list = [NormalKeybinds(), CommandKeybinds()]
    current_keybinds = keybinds_list[0]

    current_buffer = buffer1 # Assigning the buffer to be written to

    mode_message = 'INSERT'

    # main loop 
    while not tdl.event.is_window_closed():

        # Draw everything
        render_all()

        # Handle Keypresses
        current_keybinds.handle_keys()
