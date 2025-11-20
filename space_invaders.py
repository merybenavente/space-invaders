import curses
import time
import random

from enemy import Enemy, ENEMY_LIFE_MAPPING


class Board:
  TITLE = "SPACE INVADERS"
  PLATFORM = "=====^====="

  def __init__(self, stdscr):
    h, w = stdscr.getmaxyx()
    self.win_h, self.win_w = h // 2, w // 2
    start_y = (h - self.win_h) // 2
    start_x = (w - self.win_w) // 2

    self.canvas = curses.newwin(
      self.win_h, self.win_w,
      start_y, start_x
    )

    self.canvas.keypad(True)
    self.canvas.nodelay(True)
    self.canvas.keypad(True)

    self.state = {
      "title": {"y": 2, "x": (self.win_w - len(self.TITLE)) // 2, "str": self.TITLE},
      "platform": {
        'y': self.win_h - 2,
        'x': max(
          1, min(
            (self.win_w - len(self.PLATFORM)) // 2, self.win_w - 1 - len(self.PLATFORM)
          )
        ),
        "str": self.PLATFORM
      }
    }
    self.enemies: list[Enemy] = []
    [self.create_enemy() for i in range(random.randint(1, 4))]

    self.reprint_board()

  def reprint_board(self):
    self.canvas.erase()

    for e in self.enemies:
      sprite = ENEMY_LIFE_MAPPING[e.lifes].value.splitlines()
      for i, line in enumerate(sprite):
        self.canvas.addstr(e.y + i, e.x, line)

    for item in self.state.values():
      self.canvas.addstr(item['y'], item['x'], item['str'])

    self.canvas.box()
    self.canvas.refresh()
    self.move_enemies()


  def shoot(self):
    plat = self.state['platform']
    for pium_y in range(plat['y'] - 1, 0, -1):
      self.canvas.addstr(pium_y, plat['x'] + len(self.PLATFORM) // 2, '*')
      self.canvas.refresh()
      time.sleep(0.05)
      self.canvas.clear()
      self.reprint_board()

  def create_enemy(self):
    self.enemies.append(
      Enemy(
        y=random.randint(4, self.win_h-20),
        x=random.randint(4, self.win_w-6),
        lifes=4
      )
    )

  def move_enemies(self):
    new_enemies_position = []
    for e in self.enemies:
      e.x = max(1, min(e.x + (1 * e.direction), self.win_w - 2))
      new_enemies_position.append(e)
      if random.random() < 0.2:
        e.direction *= -1
    self.enemies = new_enemies_position

def pause_game(board):
  board.canvas.addstr(board.win_h // 2, (board.win_w - len('GAME PAUSE, PRESS "R" TO RESUME')) // 2, 'GAME PAUSE, PRESS "R" TO RESUME')
  board.canvas.refresh()
  while True:
    char = board.canvas.getch()
    if char == ord('r'):
      return


def main(stdscr):
  curses.curs_set(0)
  curses.noecho()
  curses.cbreak()
  board = Board(stdscr)

  key = ''
  while True:
    key = board.canvas.getch()

    if key == curses.KEY_LEFT:
      board.state['platform']['x'] -= 1
    if key == curses.KEY_RIGHT:
      board.state['platform']['x'] += 1

    board.reprint_board()

    match key:
      case curses.KEY_UP:
        board.shoot()
      case _ if key == ord('p'):
        pause_game(board)
      case _ if key == ord('e'):
        board.create_enemy()
      case _ if key == ord('q'):
        return

    time.sleep(0.05)

curses.wrapper(main)