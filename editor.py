import tdl



SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20


# Initialisation & Main Loop

def main():
    tdl.set_font('terminal16x16_gs_ro.png', greyscale=True, altLayout=False)
    root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="tdl text editor", fullscreen=False)
    tdl.setFPS(LIMIT_FPS)
    con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)

    while not tdl.event.is_window_closed():
        pass

if __name__ == "__main__":
    main()
