import curses
import time

enemy_0 = """
 _____
 |o o|
-| - |-
 =====
  / \
"""
enemy_1 = """
 _____
 |o o|
\| O |/
 =====
  / \
"""
enemy_2 = """
 _____
 |* *|
/| ~ |\
 =====
  / \
"""
enemy_3 = """
 _____
 |> <|
/| _ |\
 =====
  / \
"""
enemy_status = [enemy_0, enemy_1, enemy_2, enemy_3]


def pause_game(stdscr):
    # TODO
    # until r for resume
    stdscr.addstr("[paused]")

def shoot(stdscr, x: int, y: int):
    # TODO
    stdscr.addstr("[pium pium]")

def create_enemy(stdscr):
    # TODO
    stdscr.addstr(enemy_status[0])

def move_enemies(stdscr, x: int, y: int):
    # TODO
    pass

def main(stdscr):
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.nodelay(True)
    stdscr.keypad(True)
    stdscr.clear()

    platform = "=====^====="
    key = ''
    y, x = 10, 10

    h, w = stdscr.getmaxyx()
    win_h, win_w = h - 4, w - 4
    win = curses.newwin(win_h, win_w, 2, 2)
    win.box()
    # TODO: fix title
    title_x = (w - len(" pium piuum ")) // 2
    win.addstr(2, title_x, " pium piuum ")

    plat_y = win_h - 2
    plat_x = max(1, min((win_w - len(platform)) // 2, win_w - 1 - len(platform)))
    win.refresh()

    while True:
        key = stdscr.getch()
        win.addstr(plat_y, plat_x, platform)
        stdscr.refresh()

        if key == curses.KEY_LEFT:  plat_x -= 1
        if key == curses.KEY_RIGHT: plat_x += 1

        plat_x = max(1, min(plat_x, win_w - 1 - len(platform)))

        win.erase()
        win.box()

        try:
            win.addstr(plat_y, plat_x, platform)
        except curses.error:
            pass
        win.refresh()
        stdscr.refresh()

        match key:
            case curses.KEY_UP:
                shoot(stdscr, x, y)
            case _ if key == ord('p'):
                pause_game(stdscr)
            case _ if key == ord('q'):
                return

        time.sleep(0.05)

curses.wrapper(main)