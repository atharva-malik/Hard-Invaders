import pygame
from random import randint

class Game:
    def __init__(self):
        #region
        self.level = 0
        
        #* Player setup
        self.player = pygame.sprite.GroupSingle(Spaceship())
        
        #* Fortification setup
        self.shape = [
            '  xxxxxxx',
            ' xxxxxxxxx',
            'xxxxxxxxxxx',
            'xxxxxxxxxxx',
            'xxxxxxxxxxx',
            'xxx     xxx',
            'xx       xx']
        self.blocks = pygame.sprite.Group()
        self.fortification_pos = [0, 180, 360, 540]
        self.build_multiple_forts(57, 480, self.fortification_pos)
        #endregion
        
        #* Enemy Setup
        #self.enemies = self.order_enemies(self.generate_enemies())
        self.enemies = pygame.sprite.Group()
        self.enemies_lst = self.generate_enemies()
        self.enemy_setup(6, 8)
    
    def build_fortification(self, x_offset, y_offset, offset):
        for row_index, row in enumerate(self.shape):
            for column_index, column in enumerate(row):
                if column == "x":
                    x_coordinate = column_index * 6 + x_offset + offset
                    y_coordinate = row_index * 6 + y_offset
                    block = Fortification(6, (241, 79, 80), x_coordinate, y_coordinate)
                    self.blocks.add(block)
    
    def build_multiple_forts(self, start_x, start_y, nums):
        for i in nums:
            self.build_fortification(start_x, start_y, i)
    
    def sort_with_high_in_middle(self, inp):
        out = inp.copy()
        out.sort()
        return out[len(out)%2::2] + out[::-2]
    
    def generate_enemies(self):
        out = []
        extra = []
        for i in range(48):
            en = randint(1, 100) * self.level/10
            if en <= 78:
                out.append(1)
            elif en <= 93:
                out.append(2)
            elif en <= 98:
                out.append(3)
            else:
                out.append(3)
                extra.append(4)
        out.sort(reverse=True)
        output = [self.sort_with_high_in_middle(out[:8]), self.sort_with_high_in_middle(out[8:16]), self.sort_with_high_in_middle(out[16:24]), self.sort_with_high_in_middle(out[24:32]), self.sort_with_high_in_middle(out[32:40]), self.sort_with_high_in_middle(out[40:]), extra]
        return output
    
    def enemy_setup(self, rows, columns, x_offset=70, y_offset=100):
        for row in range(rows):
            for column in range(columns):
                x = column * 60 + x_offset
                y = row * 48 + y_offset
                num = self.enemies_lst[row][column]
                if num == 1: enemy_sprite = Rare_Enemy(x, y)
                elif num == 2: enemy_sprite = Epic_Enemy(x, y)
                elif num == 3: enemy_sprite = Mythic_Enemy(x, y)
                self.enemies.add(enemy_sprite)
    
    def update(self, screen):
        self.player.update()
        self.enemies.update(1)
        
        self.player.sprite.bullets.draw(screen)
        self.player.draw(screen)
        
        self.blocks.draw(screen)
        self.enemies.draw(screen)

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets\player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(360,680))
        self.speed = 8
        self.can_shoot = True
        self.bullet_time = 0
        self.bullet_cooldown = 600
        
        self.bullets = pygame.sprite.Group()
    
    def update(self):
        self.move_shoot()
        self.bullets.update()
    
    def move_shoot(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.x > 5:
            self.rect.x -= self.speed
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.x < 1210:
            self.rect.x += self.speed
        
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.shoot()
            self.can_shoot = False
            self.bullet_time = pygame.time.get_ticks()
        
        if pygame.time.get_ticks() - self.bullet_time >= self.bullet_cooldown:
            self.can_shoot = True
    
    def shoot(self):
        self.bullets.add(Bullet(self.rect.center))
    

class Fortification(pygame.sprite.Sprite):
    def __init__(self, size, colour, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(colour)
        self.rect = self.image.get_rect(topleft=(x,y))
    

class Enemy(pygame.sprite.Sprite):
    # Spawn Rates: 78, 15, 5, 2 
    def __init__(self, type, x, y):
        super().__init__()
        self.image = pygame.image.load("Assets/Alien_" + type + ".png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
    
    def update(self, direction):
        self.rect.x += direction
    

class Rare_Enemy(Enemy):
    def __init__(self, x, y):
        super().__init__("Rare", x, y)
    

class Epic_Enemy(Enemy):
    def __init__(self, x, y):
        super().__init__("Epic", x, y)
    

class Mythic_Enemy(Enemy):
    def __init__(self, x, y):
        super().__init__("Mythic", x, y)
    

class Legendary_Enemy(Enemy):
    def __init__(self):
        super().__init__()
    

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, speed=8):
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image.fill("yellow")
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -50 or self.rect.y >= 770:
            self.kill()

if __name__ == "__main__":
    import main.py # Run the game