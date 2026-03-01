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
                
        if self.x < 0:
            self.x = 0
        if self.x > pyxel.width - self.w:
            self.x = pyxel.width - self.w
            
        if pyxel.btn(pyxel.KEY_SPACE):
            if len(bullets) < 10:
                bullets.append(Bullet(self.x + self.w / 2, self.y))
            
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 0)
        
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = -2
    
    def update(self):
        self.y += self.vy
        if self.y < 0:
            bullets.remove(self)
            
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
        self.score = 100
        self.game_over = False
        self.block_spawn_timer = 0
        pyxel.run(self.update, self.draw)
        
    def update(self):
        self.player.update()
        for bullet in bullets:
            bullet.update()
        for enemy in self.enemies:
            enemy.update()
        for block in self.blocks:
            block.update()
            
        self.block_spawn_timer += 1
        if self.block_spawn_timer > 30: 
            self.blocks.append(Block())
            self.block_spawn_timer = 0   
            
        bullets_to_remove = []
        enemies_to_remove = []
        blocks_to_remove = []
            
        for bullet in bullets:
            for enemy in self.enemies:
                if (enemy.x < bullet.x < enemy.x + 16 and enemy.y < bullet.y < enemy.y + 16):
                    enemies_to_remove.append(enemy)
                    bullets_to_remove.append(bullet)
                    break
                
            for bullet in bullets:
                for block in self.blocks:
                    if ((block.x < bullet.x < block.x + 16 and block.y < bullet.y < block.y + 16)):
                        blocks_to_remove.append(block)
                        bullets_to_remove.append(bullet)
                    break
            
        for bullet in bullets_to_remove:
            if bullet in bullets:
                bullets.remove(bullet)
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)
        for block in blocks_to_remove:
            if block in self.blocks:
                self.blocks.remove(block)
        
        for block in self.blocks:
            if (self.player.x < block.x + 8 and self.player.x + self.player.w > block.x and self.player.y < block.y + 8 and self.player.y + self.player.h > block.y):
                self.score -= 1
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