import tdl



SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20


class Buffer(object):
    '''Gets pushed to the window and then blitted to the console'''
    pass


class Cursor(object):
    '''Dictates where the characters are placed'''

    def __init__(self, x, y, console):
        self.x = x
        self.y = y
        self.char = 221
        self.colour = 0xFFFFFF
        self.con = console

    def move(self, dx, dy):
        # Moves the cursor by the given amount
        self.x += dx
        self.y += dy

    def draw(self):
        # Draws the cursor
        self.con.draw_char(self.x, self.y, self.char, self.colour, bg=None)

    def clear(self):
        # Erase the cursor
        self.con.draw_char(self.x, self.y, ' ', self.colour, bg=None)


def keybinds():

    pass

##############################
# Initialisation & Main Loop #
##############################

def main():
    tdl.set_font('terminal16x16_gs_ro.png', greyscale=True, altLayout=False)
    root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="tdl text editor", fullscreen=False)
    tdl.setFPS(LIMIT_FPS)
    con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)

    cursor = Cursor(0, 0, con)

    while not tdl.event.is_window_closed():

        cursor.draw()

        root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        tdl.flush()

        cursor.clear()


if __name__ == "__main__":
    main()
