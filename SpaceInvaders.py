import pygame, sys
from random import randint, choice

class Game:
    def __init__(self, level=0, score=0, lives=1):
        self.level = level
        self.game_over = 0
        
        music = pygame.mixer.Sound("Assets/music.wav")
        music.set_volume(0.2)
        music.play(loops=-1 )
        self.bullet_sound = pygame.mixer.Sound("Assets/bullet.wav")
        self.bullet_sound.set_volume(0.1)
        self.explosion_sound = pygame.mixer.Sound("Assets/explosion.wav")
        self.explosion_sound.set_volume(0.3)
        
        self.player = pygame.sprite.GroupSingle(Spaceship())
        self.lives = lives
        self.score = score
        self.font = pygame.font.Font("Assets/Pixeled.ttf", 20)
        
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
        
        self.enemies = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemies_lst = self.generate_enemies()
        self.enemy_direction = 1
        self.enemy_cooldown = 0
        self.enemy_setup(6, 8)
        self.legendary = pygame.sprite.GroupSingle()
        try:
            if self.enemies_lst[-1][0] == 4:
                self.legendary_count = len(self.enemies_lst[-1])
        except IndexError:
            self.legendary_count = 0
        self.legend_spawn_time = randint(400, 800) #* Once every 400-800 frames
    
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
    
    def enemy_move_down(self,distance):
        if self.enemies:
            for alien in self.enemies.sprites():
                alien.rect.y += distance
    
    def enemy_position_checker(self):
        all_enemies = self.enemies.sprites()
        for enemy in all_enemies:
            if enemy.rect.right >= 720:
                self.enemy_direction = -1
                self.enemy_move_down(2)
            elif enemy.rect.left <= 0:
                self.enemy_direction = 1
                self.enemy_move_down(2)
    #TODO: FINISH THIS
    def enemy_shoot(self):
        self.enemy_cooldown += 1
        if self.enemies.sprites() and self.enemy_cooldown > (60/(self.level+1)): #* The second number is the lasers per second
            randEnemy = choice(self.enemies.sprites())
            # bullet = randEnemy.shoot() #TODO: Implement this
            bullet = Bullet(randEnemy.rect.center, -6, "red")
            self.enemy_bullets.add(bullet)
            self.enemy_cooldown = 0
            self.bullet_sound.play()
    
    def legendary_spawner(self):
        self.legend_spawn_time -= 1
        if self.legend_spawn_time <= 0 and self.legendary_count > 0:
            self.legendary.add(Legendary_Enemy(choice(["right", "left"])))
            self.legend_spawn_time = randint(400, 800)
            self.legendary_count -= 1
    
    def display_lives_score(self, screen):
        score = self.font.render("Score: " + str(self.score), False, 'white')
        score_rect = score.get_rect(center=(80,20))
        screen.blit(score, score_rect)
        score = self.font.render("Health: " + str(self.lives), False, 'white')
        score_rect = score.get_rect(center=(620,20))
        screen.blit(score, score_rect)
    
    def check_collisions(self):
        if self.player.sprite.bullets:
            for bul in self.player.sprite.bullets:
                if pygame.sprite.spritecollide(bul, self.blocks, True):
                    bul.kill()
                enemy_hit_list = pygame.sprite.spritecollide(bul, self.enemies, True)
                if enemy_hit_list:
                    for enemy in enemy_hit_list:
                        self.score += enemy.value
                    bul.kill()
                    self.explosion_sound.play()
                if pygame.sprite.spritecollide(bul, self.legendary, True):
                    self.score += 1000
                    bul.kill()
                if pygame.sprite.spritecollide(bul, self.enemy_bullets, True):
                    self.score += 5
                    bul.kill()
        if self.enemies:
            for en in self.enemies:
                pygame.sprite.spritecollide(en, self.blocks, True)
                if pygame.sprite.spritecollide(en, self.player, True):
                    pygame.quit() #TODO: FIX
                    sys.exit()
        if self.enemy_bullets:
            for bul in self.enemy_bullets:
                if pygame.sprite.spritecollide(bul, self.blocks, True):
                    bul.kill()
                if pygame.sprite.spritecollide(bul, self.player, False):
                    bul.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = -1
                        pygame.quit() #TODO: FIX
                        sys.exit()
    
    def victory_message(self, screen):
        if not self.enemies.sprites():
            self.game_over = 1
            victory = self.font.render('You Won', False, 'white')
            victory_rect = victory.get_rect(center=(360,360))
            screen.blit(victory, victory_rect)
    
    def update(self, screen):
        if self.game_over == 0:
            self.player.update()
            self.enemies.update(self.enemy_direction)
            self.enemy_position_checker()
            self.enemy_shoot()
            self.enemy_bullets.update()
            self.enemy_bullets.draw(screen)
            self.legendary_spawner()
            self.legendary.draw(screen)
            self.legendary.update()
            
            self.check_collisions()
            self.victory_message(screen)
            
            self.player.sprite.bullets.draw(screen)
            self.player.draw(screen)
            self.display_lives_score(screen)
            
            self.blocks.draw(screen)
            self.enemies.draw(screen)
        elif self.game_over == -1:
            return 0, 0, 1
        elif self.game_over == 1:
            return self.level+1, self.score, self.lives+1

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bullet_sound = pygame.mixer.Sound("Assets/bullet.wav")
        self.bullet_sound.set_volume(0.5)
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
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.x < 655:
            self.rect.x += self.speed
        
        if keys[pygame.K_SPACE] and self.can_shoot:
            self.shoot()
            self.bullet_sound.play()
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
    def __init__(self, type, x, y, val=10):
        super().__init__()
        self.image = pygame.image.load("Assets/Alien_" + type + ".png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.value = val
    
    def update(self, direction):
        self.rect.x += direction
    

class Rare_Enemy(Enemy):
    def __init__(self, x, y):
        super().__init__("Rare", x, y)
    

class Epic_Enemy(Enemy):
    def __init__(self, x, y):
        super().__init__("Epic", x, y, 20)
    

class Mythic_Enemy(Enemy):
    def __init__(self, x, y):
        super().__init__("Mythic", x, y, 40)
    

#* The behaviour of this enemy is so different to the normal enemies
#* that it is not worth inheriting from the base class.
class Legendary_Enemy(pygame.sprite.Sprite):
    def __init__(self, side):
        super().__init__()
        self.image = pygame.image.load("Assets/UFO_Legendary.png").convert_alpha()        
        if side == "right":
            x = 770
            self.speed = -2
        else:
            x = -50
            self.speed = 2
        self.rect = self.image.get_rect(topleft=(x,80))
    
    def update(self):
        self.rect.x += self.speed
    

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, speed=8, colour="yellow"):
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image.fill(colour)
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -50 or self.rect.y >= 770:
            self.kill()

if __name__ == "__main__":
    import main.py # Run the game