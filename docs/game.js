import { Enemy, ENEMY_SPRITES } from './enemy.js';

class Board {
  static TITLE = "SPACE INVADERS";
  static PLATFORM = "=====^=====";

  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');

    this.winW = 80;
    this.winH = 40;

    this.charWidth = 10;
    this.charHeight = 16;

    canvas.width = this.winW * this.charWidth;
    canvas.height = this.winH * this.charHeight;

    this.ctx.font = '16px monospace';
    this.ctx.textBaseline = 'top';

    this.score = 0;
    this.paused = false;
    this.gameOver = false;
    this.frameCount = 0;

    this.state = {
      title: { y: 2, x: Math.floor((this.winW - Board.TITLE.length) / 2), str: Board.TITLE },
      platform: {
        y: this.winH - 2,
        x: Math.max(1, Math.min(
          Math.floor((this.winW - Board.PLATFORM.length) / 2),
          this.winW - 1 - Board.PLATFORM.length
        )),
        str: Board.PLATFORM
      },
      score: { y: 2, x: 2 }
    };

    this.pium = [];
    this.enemies = [];

    const initialEnemies = Math.floor(Math.random() * 4) + 1;
    for (let i = 0; i < initialEnemies; i++) {
      this.createEnemy();
    }

    this.setupControls();
  }

  setupControls() {
    document.addEventListener('keydown', (e) => {
      if (this.gameOver) return;

      switch(e.key) {
        case 'ArrowLeft':
          e.preventDefault();
          this.state.platform.x = Math.max(1, this.state.platform.x - 1);
          break;
        case 'ArrowRight':
          e.preventDefault();
          this.state.platform.x = Math.min(
            this.winW - Board.PLATFORM.length - 1,
            this.state.platform.x + 1
          );
          break;
        case 'ArrowUp':
          e.preventDefault();
          if (!this.paused) {
            this.shoot();
          }
          break;
        case 'p':
        case 'P':
          e.preventDefault();
          this.paused = true;
          break;
        case 'r':
        case 'R':
          e.preventDefault();
          this.paused = false;
          break;
        case 'e':
        case 'E':
          e.preventDefault();
          if (!this.paused) {
            this.createEnemy();
          }
          break;
        case 'q':
        case 'Q':
          e.preventDefault();
          this.quitGame();
          break;
      }
    });
  }

  shoot() {
    this.pium.push({
      x: this.state.platform.x + Math.floor(Board.PLATFORM.length / 2),
      y: this.state.platform.y - 1,
      str: '*'
    });
  }

  quitGame() {
    this.gameOver = true;
    const floppyDisk = document.getElementById('floppyDisk');
    const happyMac = document.getElementById('happyMac');
    const controls = document.querySelector('.controls');

    const canvasRect = this.canvas.getBoundingClientRect();
    const centerX = canvasRect.left + canvasRect.width / 2;
    const centerY = canvasRect.top + canvasRect.height / 2;

    floppyDisk.style.left = `${centerX}px`;
    floppyDisk.style.top = `${centerY}px`;

    happyMac.style.left = `${centerX}px`;
    happyMac.style.top = `${centerY + 180}px`;

    floppyDisk.classList.add('show');
    happyMac.classList.add('show');
    this.canvas.classList.add('shrinking');
    controls.classList.add('hidden');

    this.setupDragAndDrop();
  }

  setupDragAndDrop() {
    const floppyDisk = document.getElementById('floppyDisk');
    const happyMac = document.getElementById('happyMac');
    let isDragging = false;
    let offsetX = 0;
    let offsetY = 0;

    floppyDisk.addEventListener('mousedown', (e) => {
      isDragging = true;
      floppyDisk.classList.add('dragging');

      const rect = floppyDisk.getBoundingClientRect();
      offsetX = e.clientX - rect.left - rect.width / 2;
      offsetY = e.clientY - rect.top - rect.height / 2;

      e.preventDefault();
    });

    document.addEventListener('mousemove', (e) => {
      if (!isDragging) return;

      const x = e.clientX - offsetX;
      const y = e.clientY - offsetY;

      floppyDisk.style.left = `${x}px`;
      floppyDisk.style.top = `${y}px`;
      floppyDisk.style.transform = 'translate(-50%, -50%)';

      const macRect = happyMac.getBoundingClientRect();
      const diskRect = floppyDisk.getBoundingClientRect();

      const isOverMac = !(
        diskRect.right < macRect.left ||
        diskRect.left > macRect.right ||
        diskRect.bottom < macRect.top ||
        diskRect.top > macRect.bottom
      );

      if (isOverMac) {
        happyMac.classList.add('highlight');
      } else {
        happyMac.classList.remove('highlight');
      }
    });

    document.addEventListener('mouseup', (e) => {
      if (!isDragging) return;

      isDragging = false;
      floppyDisk.classList.remove('dragging');

      const macRect = happyMac.getBoundingClientRect();
      const diskRect = floppyDisk.getBoundingClientRect();

      const isOverMac = !(
        diskRect.right < macRect.left ||
        diskRect.left > macRect.right ||
        diskRect.bottom < macRect.top ||
        diskRect.top > macRect.bottom
      );

      happyMac.classList.remove('highlight');

      if (isOverMac) {
        this.resumeGame();
      }
    });
  }

  resetGame() {
    this.score = 0;
    this.paused = false;
    this.gameOver = false;
    this.frameCount = 0;
    this.pium = [];
    this.enemies = [];

    const initialEnemies = Math.floor(Math.random() * 4) + 1;
    for (let i = 0; i < initialEnemies; i++) {
      this.createEnemy();
    }
  }

  resumeGame() {
    const floppyDisk = document.getElementById('floppyDisk');
    const happyMac = document.getElementById('happyMac');
    const controls = document.querySelector('.controls');

    floppyDisk.classList.remove('show');
    happyMac.classList.remove('show');
    this.canvas.classList.remove('shrinking');
    controls.classList.remove('hidden');

    const canvasRect = this.canvas.getBoundingClientRect();
    const centerX = canvasRect.left + canvasRect.width / 2;
    const centerY = canvasRect.top + canvasRect.height / 2;

    floppyDisk.style.left = `${centerX}px`;
    floppyDisk.style.top = `${centerY}px`;

    happyMac.style.left = `${centerX}px`;
    happyMac.style.top = `${centerY + 180}px`;

    this.resetGame();
    this.reprintBoard();
    lastUpdateTime = performance.now();
    requestAnimationFrame(gameLoop);
  }

  createEnemy() {
    const spriteW = Math.max(...ENEMY_SPRITES[4].map(line => line.length));
    this.enemies.push(new Enemy(
      Math.floor(Math.random() * (this.winH - Math.floor(this.winH / 3) - 4)) + 4,
      Math.floor(Math.random() * (this.winW - spriteW - 1)) + 1,
      4
    ));
  }

  moveEnemies() {
    const futureEnemies = [];

    for (const e of this.enemies) {
      let newDirection = e.direction;

      if (Math.random() < 0.2) {
        newDirection *= -1;
      }

      let newXPosition = e.x + (1 * newDirection);

      if (newXPosition <= 1 || newXPosition >= this.winW - 7) {
        newDirection *= -1;
        newXPosition = e.x + newDirection;
      }

      if (e.lifes > 0) {
        futureEnemies.push({ enemy: e, newPos: newXPosition, newDir: newDirection });
      } else {
        this.score += 20;
      }
    }

    for (const item of futureEnemies) {
      const collisionCount = futureEnemies.filter(f => f.newPos === item.newPos).length;
      if (collisionCount > 1) {
        item.newDir = -item.newDir;
        item.newPos = item.enemy.x + item.newDir;
      }

      item.enemy.direction = item.newDir;
      item.enemy.x = item.newPos;
    }

    this.enemies = futureEnemies.map(item => item.enemy);
  }

  drawText(y, x, text) {
    this.ctx.fillText(text, x * this.charWidth, y * this.charHeight);
  }

  reprintBoard() {
    this.ctx.fillStyle = '#000';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    this.ctx.strokeStyle = '#fff';
    this.ctx.strokeRect(0, 0, this.canvas.width, this.canvas.height);

    const aliveEnemies = this.enemies.filter(e => e.lifes > 0);
    const hasHadEnemies = this.enemies.length > 0 || this.score > 0;
    const gameWon = hasHadEnemies && aliveEnemies.length === 0;

    if (!gameWon) {
      this.ctx.fillStyle = '#0f0';

      for (const e of aliveEnemies) {
        const sprite = e.getSprite();
        for (let i = 0; i < sprite.length; i++) {
          const y = e.y + i;
          if (y >= 0 && y < this.winH) {
            const limit = this.winW - e.x - 1;
            if (limit > 0) {
              const line = limit >= sprite[i].length ? sprite[i] : sprite[i].substring(0, limit);
              if (line) {
                this.drawText(y, e.x, line);
              }
            }
          }
        }
      }
    }

    this.ctx.fillStyle = '#fff';
    this.drawText(this.state.title.y, this.state.title.x, this.state.title.str);
    this.drawText(this.state.platform.y, this.state.platform.x, this.state.platform.str);

    if (!gameWon) {
      this.drawText(this.state.score.y, this.state.score.x, `SCORE ${this.score}`);
    }

    // Only draw and update bullets if game is not won
    if (!gameWon) {
      this.ctx.fillStyle = '#ff0';
      if (!this.paused) {
        const newShots = [];
        for (const shoot of this.pium) {
          this.drawText(shoot.y, shoot.x, shoot.str);

          let hitEnemy = false;
          for (const e of this.enemies) {
            if (e.lifes <= 0) continue;

            const sprite = e.getSprite();
            const enemyYPositions = sprite.map((_, i) => e.y + i);
            const enemyXPositions = Array.from({ length: 7 }, (_, i) => e.x + i);

            if (enemyYPositions.includes(shoot.y) && enemyXPositions.includes(shoot.x)) {
              e.lifes -= 1;
              hitEnemy = true;
              this.score += 10;
              break;
            }
          }

          if (!hitEnemy && shoot.y !== 0) {
            shoot.y -= 1;
            newShots.push(shoot);
          }
        }
        this.pium = newShots;

        this.frameCount++;
        if (this.frameCount % 3 === 0) {
          this.moveEnemies();
        }
      } else {
        // Still draw shots when paused, but don't move them
        for (const shoot of this.pium) {
          this.drawText(shoot.y, shoot.x, shoot.str);
        }
      }
    }

    if (this.paused) {
      this.ctx.fillStyle = '#ff0';
      const pauseMsg = 'GAME PAUSE, PRESS "R" TO RESUME';
      this.drawText(
        Math.floor(this.winH / 2),
        Math.floor((this.winW - pauseMsg.length) / 2),
        pauseMsg
      );
    }

    if (gameWon && !this.gameOver) {
      this.pium = [];
      this.ctx.fillStyle = '#0f0';
      const winMsg = `SCORE: ${this.score}`;
      this.drawText(
        Math.floor(this.winH / 2),
        Math.floor((this.winW - winMsg.length) / 2),
        winMsg
      );
      this.gameOver = true;

      setTimeout(() => {
        this.quitGame();
      }, 5000);
    }
  }
}

const canvas = document.getElementById('gameCanvas');
const board = new Board(canvas);

let lastUpdateTime = 0;
const UPDATE_INTERVAL = 50; // 50ms to match Python's time.sleep(0.05)

function gameLoop(currentTime) {
  if (currentTime - lastUpdateTime >= UPDATE_INTERVAL) {
    if (!board.paused && !board.gameOver) {
      board.reprintBoard();

      if (Math.random() < 0.005) {
        board.createEnemy();
      }
    } else if (board.paused) {
      board.reprintBoard();
    }

    lastUpdateTime = currentTime;
  }

  if (!board.gameOver) {
    requestAnimationFrame(gameLoop);
  }
}

requestAnimationFrame(gameLoop);
