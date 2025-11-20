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

    if self.win_h <= 20 or self.win_w <= 40:
      self.canvas.addstr(1, 1, "Window size too small, please relaunch on a larger screen")
      self.canvas.refresh()
      time.sleep(5)
      raise ValueError("Window too small")

    self.canvas.keypad(True)
    self.canvas.nodelay(True)
    self.canvas.keypad(True)

    self.score = 0
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
      },
      "score": {"y": 2, "x": 2}
    }
    self.pium = []
    self.enemies: list[Enemy] = []
    [self.create_enemy() for i in range(random.randint(1, 4))]

    self.reprint_board()

  def reprint_board(self):
    self.canvas.erase()

    for e in self.enemies:
      sprite = ENEMY_LIFE_MAPPING[e.lifes].value.strip("\n").split("\n")

      for i, line in enumerate(sprite):
        y = e.y + i
        if 0 <= y < self.win_h:
          limit = self.win_w - e.x - 1
          if limit <= 0:
            continue
          if safe_line := line if limit >= len(line) else line[:limit]:
            self.canvas.addstr(y, e.x, safe_line)

    for key, item in self.state.items():
      if key == 'score':
        self.canvas.addstr(item['y'], item['x'], f"SCORE {self.score}")
      else:
        self.canvas.addstr(item['y'], item['x'], item['str'])

    new_shots = []
    for shoot in self.pium:
      self.canvas.addstr(shoot['y'], shoot['x'], shoot['str'])
      hit_enemy = False
      for e in self.enemies:
        if e.lifes <= 0:
          continue
        sprite = ENEMY_LIFE_MAPPING[e.lifes].value.strip("\n").split("\n")
        if shoot['y'] in [e.y + i for i, _ in enumerate(sprite)]:
          if shoot['x'] in [e.x + i for i in range(7)]:
            e.lifes -= 1
            hit_enemy = True
            self.score += 10
      if not hit_enemy and shoot['y'] != 0:
        shoot['y'] -= 1
        new_shots.append(shoot)
    self.pium = new_shots

    self.move_enemies()
    self.canvas.box()
    self.canvas.refresh()

  def shoot(self):
    self.pium.append({
        "x": self.state["platform"]['x'] + len(self.PLATFORM) // 2,
        "y": self.state["platform"]['y'] - 1,
        "str": '*',
    })

  def create_enemy(self):
    sprite_w = max(len(l) for l in ENEMY_LIFE_MAPPING[4].value)
    self.enemies.append(
      Enemy(
        y=random.randint(4, self.win_h-(self.win_h//3)),
        x=random.randint(1, self.win_w - sprite_w - 1),
        lifes=4
      )
    )


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

      if e.lifes > 0:
        future_enemies.append((e, new_x_position, new_direction))
      else:
        self.score += 20

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

def won_game(board):
  board.canvas.addstr(board.win_h // 2, (board.win_w - len(f'SCORE: {board.score}')) // 2, f'SCORE: {board.score}')
  board.canvas.refresh()
  time.sleep(5)

def main(stdscr):
  curses.curs_set(0)
  curses.noecho()
  curses.cbreak()

  board = Board(stdscr)
  key = ''
  while len(board.enemies) > 0:
    board.reprint_board()

    if random.random() < 0.005:
      board.create_enemy()

    key = board.canvas.getch()
    match key:
      case curses.KEY_LEFT:
        board.state['platform']['x'] -= 1
      case curses.KEY_RIGHT:
        board.state['platform']['x'] += 1
      case curses.KEY_UP:
        board.shoot()
      case _ if key == ord('p'):
        pause_game(board)
      case _ if key == ord('e'):
        board.create_enemy()
      case _ if key == ord('q'):
        return

    time.sleep(0.05)
  won_game(board)

curses.wrapper(main)