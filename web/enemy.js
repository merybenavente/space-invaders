export const ENEMY_SPRITES = {
  4: [
    " _____",
    " |o o|",
    "-| - |-",
    "  ┘ └"
  ],
  3: [
    " _____",
    " |o o|",
    "\\| O |/",
    "  ┘ └"
  ],
  2: [
    " _____",
    " |* *|",
    "/| ~ |\\",
    "  ┘ └"
  ],
  1: [
    " _____",
    " |> <|",
    "┌| _ |┐",
    "  ┘ └"
  ]
};

export class Enemy {
  constructor(y, x, lifes = 4) {
    this.x = x;
    this.y = y;
    this.direction = -1;
    this.lifes = lifes;
  }

  getSprite() {
    return ENEMY_SPRITES[this.lifes] || ENEMY_SPRITES[1];
  }
}
