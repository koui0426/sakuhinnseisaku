import pyxel
import random

class Player:
    def __init__(self):
        self.x = pyxel.width / 2
        self.y = pyxel.height - 20
        self.w = 16
        self.h = 16
        self.speed = 2
        
    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
        if pyxel.btn(pyxel.KEY_SPACE):
            if len(bullets) < 3:
                bullets.append(Bullet(self.x + self.w /2, self.y))
                
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 0)
        
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = -2
    
    def update(self):
        self.y += self.vy
        
    def draw(self):
        pyxel.rect(self.x, self.y, 2, 4, 10)
        
class Enemy:
    def __init__(self):
        self.x = random.randint(0, pyxel.width -8)
        self.y = random.randint(0, pyxel.height / 2)
        self.vy = 3
        
    def update(self):
        self.y += self.vy
        if self.y > pyxel.height:
            self.y = random.randint(0, pyxel.height / 2)
            self.x = random.randint(0, pyxel.width -8)
            
    def draw(self):
        pyxel.blt(self.x, self.y, 2, 0, 0, 16, 16, 0)
        
class Block:
    def __init__(self):
        self.x = random.randint(0, pyxel.width - 8)
        self.y = 0
        self.vy = random.uniform(2, 5)
        
    def update(self):
        self.y += self.vy
        if self.y > pyxel.height:
            self.y = 0
            self.x = random.randint(0, pyxel.width - 8)
            self.vy = random.uniform(1, 3)
            
    def draw(self):
        pyxel.blt(self.x, self.y, 1, 0, 0, 16, 16, 0)
        
class App:
    def __init__(self):
        pyxel.init(160, 120, title="シューティングゲーム")
        pyxel.load("aaaaa.pyxres")
        self.player = Player()
        self.enemies = [Enemy() for _ in range(5)]
        self.blocks = [Block() for _ in range(3)]
        global bullets
        bullets = []
        self.score = 50
        self.game_over = False
        pyxel.run(self.update, self.draw)
        
    def update(self):
        self.player.update()
        for bullet in bullets:
            bullet.update()
        for enemy in self.enemies:
            enemy.update()
        for block in self.blocks:
            block.update()
            
        for bullet in bullets:
            for enemy in self.enemies:
                if (enemy.x < bullet.x < enemy.x + 8 and enemy.y < bullet.y < enemy.y + 8):
                    self.enemies.remove(enemy)
                    bullets.remove(bullet)
                    break
                
        for block in self.blocks:
            if (self.player.x < block.x + 8 and self.player.x + self.player.w > block.x and self.player.y < block.y + 8 and self.player.y + self.player.h > block.y):
                self.score -= 3
                if self.score < 0:
                    self.score = 0
                    
        if self.score < 1:
            self.game_over = True
                
    def draw(self):
        pyxel.cls(0)
        if not self.game_over:
            self.player.draw()
            for bullet in bullets:
                bullet.draw()
            for enemy in self.enemies:
                enemy.draw()
            for block in self.blocks:
                block.draw()
            pyxel.text(5, 5, f"SCORE：{self.score}", 7)
        else:
            pyxel.text(60,50, "GAME OVER", pyxel.frame_count % 16)
        
            
App()