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

  def enemies_will_collide(self, new_x, new_y, other_enemies):
    return any(o.x == new_x and o.y == new_y for o in other_enemies)

  def move_enemies(self):
    future_enemies = []
    for e in self.enemies:
      new_direction = e.direction
      # randomly update trajectory
      if random.random() < 0.2:
        new_direction *= -1
      new_x_position = e.x + (1 * new_direction)

      # bounce if we find a wall
      if new_x_position <= 1 or new_x_position >= self.win_w - 7:
        new_direction *= -1
        new_x_position = e.x + new_direction

      future_enemies.append((e, new_x_position, new_direction))

    for e, np, nd in future_enemies:
      if sum(1 for _, fx2, _ in future_enemies if fx2 == np) > 1:
        nd = -nd
        np = e.x + nd

      e.direction = nd
      e.x = np

    self.enemies = [e[0] for e in future_enemies]

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