from enum import Enum


class EnemyState(Enum):
  enemy_0 = """
 _____
 |o o|
-| - |-
  ┘ └
    """
  enemy_1 = """
 _____
 |o o|
\\| O |/
  ┘ └
  """
  enemy_2 = """
 _____
 |* *|
/| ~ |\\
  ┘ └
  """
  enemy_3 = """
 _____
 |> <|
┌| _ |┐
  ┘ └
  """

class Enemy:
  def __init__(self, y: int, x: int, lifes = 4):
    self.x = x
    self.y = y
    self.direction = -1
    self.lifes = lifes

ENEMY_LIFE_MAPPING = {
  4: EnemyState.enemy_0,
  3: EnemyState.enemy_1,
  2: EnemyState.enemy_2,
  1: EnemyState.enemy_3,
}