import pygame

class Game:
    def __init__(self):
        self.player = pygame.sprite.GroupSingle(Spaceship())
        #self.enemies = self.order_enemies(self.generate_enemies())
    
    def generate_enemies(self):
        pass
    
    def order_enemies(self, enemies):
        out = []
        enemies = reversed(sorted(enemies))
        for i in enemies:
            out.append(enemies)
        return out
    
    def update(self, screen):
        self.player.draw(screen)
        self.player.update()

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Assets\player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (640,680))
        self.speed = 8
    
    def update(self):
        self.get_input()
    
    def get_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.x > 5:
            self.rect.x -= self.speed
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.x < 1210:
            self.rect.x += self.speed
        
        if keys[pygame.K_SPACE]:
            self.shoot()
    
    def shoot(self):
        print("shot")
    

class Fortification(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    

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
    