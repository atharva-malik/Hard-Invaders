import pygame

class Game:
    def __init__(self):
        #* Player setup
        self.player = pygame.sprite.GroupSingle(Spaceship())
        #self.enemies = self.order_enemies(self.generate_enemies())
        
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
        self.fortification_pos = [num * 180 for num in range(4)]
        print(self.fortification_pos)
        self.build_multiple_forts(57, 480, self.fortification_pos)
    
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
    
    def generate_enemies(self):
        pass
    
    def order_enemies(self, enemies):
        out = []
        enemies = reversed(sorted(enemies))
        for i in enemies:
            out.append(enemies)
        return out
    
    def update(self, screen):
        self.player.update()
        
        self.player.sprite.bullets.draw(screen)
        self.player.draw(screen)
        
        self.blocks.draw(screen)

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
    def __init__(self):
        super().__init__()
    

class Common_Enemy(Enemy):
    def __init__(self):
        super().__init__()
    

class Rare_Enemy(Enemy):
    def __init__(self):
        super().__init__()
    

class Epic_Enemy(Enemy):
    def __init__(self):
        super().__init__()
    

class Mythic_Enemy(Enemy):
    def __init__(self):
        super().__init__()
    

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