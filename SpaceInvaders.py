"""This is the file you import to play the game. It contains the main game loop and the `Game` class, which handles all of the game logic.

This file contains all of the classes needed to build and run the Space Invaders game.

Usage:
In your main file:

from SpaceInvaders import *

game = Game(level=level, score=score, lives=lives) # Where level, score, lives are the current values (or the starting values of 0, 0, 1)
while True:
    #* OTHER PYGAME CODE
    
    level, score, lives = game.update(screen) # Used to check whether the game is over, and to update the game state.
    
    #* OTHER PYGAME CODE
    
    if int(score) > last_score:
        last_score = score
        break
    elif lives == -1:
        break
"""


import pygame
from random import randint, choice

class Game:
    """The `Game` class represents the main game logic for the Space Invaders game. It handles the initialization of game state, player and enemy management, 
    collision detection, and game progression.
    
    Attributes:
        level (int): The current level of the game.
        game_over (int): A flag that is set to 1 when the player wins and -1 when the player loses.
        music (pygame.mixer.Sound): The background music for the game.
        bullet_sound (pygame.mixer.Sound): The sound played when the enemy fires a bullet.
        font (pygame.font.Font): The font used to display text on the screen.
        
        player (Player): The player object for the game.
        lives (int): The number of lives the player has.
        score (int): The player's score.
        
        shape (pygame.Surface): The desired shape of the fortifications.
        blocks (pygame.sprite.Group): The blocks that make up the fortifications.
        fortification_pos (list): The x-position offsets of the fortifications.
        
        enemies (pygame.sprite.Group): The enemies in the game.
        enemy_bullets (pygame.sprite.Group): The bullets fired by the enemies.
        enemies_lst (list): A list of the enemies in the game in order, used to generate them.
        enemy_direction (int): The direction the enemies are moving in.
        enemy_cooldown (int): The cooldown for the enemy bullets.
        legendary (pygame.sprite.Group): The legendary enemy in the game.
        legendary_count (int): The total number of legendary enemies in the whole level.
        legendary_spawn_time (int): The spawn frequency of legendary enemies.
    """
    
    def __init__(self, level=0, score=0, lives=1):
        """Initializes the game class.

        Args:
            level (int, optional): The current level. Defaults to 0.
            score (int, optional): The current player score. Defaults to 0.
            lives (int, optional): The current player lives. Defaults to 1.
        """
        self.level = level
        self.game_over = 0
        
        self.music = pygame.mixer.Sound("Assets/music.wav")
        self.music.set_volume(0.2)
        self.music.play(loops=-1 )
        self.bullet_sound = pygame.mixer.Sound("Assets/bullet.wav")
        self.bullet_sound.set_volume(0.1)
        
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
        """Builds a fortification at the specified x and y offsets, using the predefined shape.
        
        Args:
            x_offset (int): The x-coordinate offset for the fortification.
            y_offset (int): The y-coordinate offset for the fortification.
            offset (int): The additional x-coordinate offset from the left for the fortification.
        """
        for row_index, row in enumerate(self.shape):
            for column_index, column in enumerate(row):
                if column == "x":
                    x_coordinate = column_index * 6 + x_offset + offset
                    y_coordinate = row_index * 6 + y_offset
                    block = Fortification(6, (241, 79, 80), x_coordinate, y_coordinate)
                    self.blocks.add(block)
    
    def build_multiple_forts(self, start_x, start_y, nums):
        """Builds multiple fortifications at the specified starting x and y coordinates, using the offsets provided in the `nums` list.
        
        Args:
            start_x (int): The starting x-coordinate for the fortifications.
            start_y (int): The starting y-coordinate for the fortifications.
            nums (list): A list of x-coordinate offsets to use for each fortification.
        """
        for i in nums:
            self.build_fortification(start_x, start_y, i)
    
    def sort_with_high_in_middle(self, inp):
        """Sorts a list with the highest values in the middle.
        
        Used to ensure the enemy with the highest value is in the middle
        
        Args:
            inp (list): The input list to be sorted.
        
        Returns:
            list: The sorted list with the highest values in the middle.
        """
        out = inp.copy()
        out.sort()
        return out[len(out)%2::2] + out[::-2]
    
    def generate_enemies(self):
        """Generates a list of enemies with varying difficulty levels, sorted with the highest values in the middle.
        
        The method generates a list of 48 enemies, where the difficulty level of each enemy is determined by a random 
        number between 1 and 100 multiplied by the current game level. The enemies are then sorted into 6 rows, with the 
        highest values in the middle of each row.
        
        Additionally, the method generates a list of legendary enemies, which are the most difficult enemies (level 4).
        These extra enemies are added to the end of the output list.
        
        Returns:
            list: A list of 6 rows of enemies, with the highest values in the middle of each row, and a list of extra enemies at the end.
        """
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
        """Sets up the enemies on the game screen based on the provided rows, columns, and offsets.
        
        The method iterates through the rows and columns, calculating the x and y positions for each
        enemy based on the offsets. It then creates an enemy sprite of the appropriate type (Rare_Enemy, 
        Epic_Enemy, or Mythic_Enemy) and adds it to the self.enemies group.
        
        Args:
            rows (int): The number of rows of enemies to create.
            columns (int): The number of columns of enemies to create.
            x_offset (int, optional): The horizontal offset for the enemy positions. Defaults to 70.
            y_offset (int, optional): The vertical offset for the enemy positions. Defaults to 100.
        
        """
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
        """Moves all enemies down by the specified distance.
        
        This method iterates through all the enemy sprites in the `self.enemies`
        group and moves each one down by the specified `distance` value.
        
        Args:
            distance (int): The number of pixels to move the enemies down.
        
        """
        if self.enemies:
            for alien in self.enemies.sprites():
                alien.rect.y += distance
    
    def enemy_position_checker(self):
        """Checks the position of all enemies on the game screen and adjusts their movement direction and vertical position accordingly.
        
        This method iterates through all the enemy sprites in the `self.enemies` group and checks the position of each one. If an
        enemy's right edge reaches the right side of the screen (720 pixels), the `self.enemy_direction` is set to -1 to make the 
        enemies move left, and the `enemy_move_down` method is called to move all enemies down by 2 pixels. If an enemy's left edge 
        reaches the left side of the screen (0 pixels), the `self.enemy_direction` is set to 1 to make the enemies move right, and 
        the `enemy_move_down` method is called to move all enemies down by 2 pixels.
        """
        
        all_enemies = self.enemies.sprites()
        for enemy in all_enemies:
            if enemy.rect.right >= 720:
                self.enemy_direction = -1
                self.enemy_move_down(2)
            elif enemy.rect.left <= 0:
                self.enemy_direction = 1
                self.enemy_move_down(2)
    
    def enemy_shoot(self):
        """Shoots enemy bullets at random intervals.
        
        This method is responsible for shooting enemy bullets at a rate that increases with the game level. 
        It checks if there are any enemies on the screen, and if so, it randomly selects one of them to shoot a bullet.
        The bullet is then added to the `self.enemy_bullets` group. The `self.enemy_cooldown` variable is used to 
        control the rate of fire, and is reset to 0 after a bullet is fired.
        """
        self.enemy_cooldown += 1
        if self.enemies.sprites() and self.enemy_cooldown > (60/(self.level+1)): #* The second number is the lasers per second
            randEnemy = choice(self.enemies.sprites())
            bullet = randEnemy.shoot()
            self.enemy_bullets.add(bullet)
            self.enemy_cooldown = 0
            self.bullet_sound.play()
    
    def legendary_shoot(self):
        """Shoots a triple-shot from the legendary enemy.
        
        This method is called to shoot a triple-shot from the legendary enemy sprite. It randomly determines 
        whether to shoot the triple-shot, and if so, it creates three bullet sprites and adds them to the `self.enemy_bullets` group.
        """
        if self.legendary.sprites() != []:
            if randint(1,1000) <= 50:
                b1, b2, b3 = self.legendary.sprite.shoot()
                self.enemy_bullets.add(b1)
                self.enemy_bullets.add(b2)
                self.enemy_bullets.add(b3)
    
    def legendary_spawner(self):
        """Spawns a legendary enemy at random intervals.
        
        This method is responsible for spawning a legendary enemy sprite on the game screen. It decrements the 
        `self.legend_spawn_time` variable on each call, and when it reaches 0, a new legendary enemy is added to 
        the `self.legendary` group. The `self.legend_spawn_time` is then reset to a random value between 400 and 800,
        and the `self.legendary_count` is decremented. This method ensures that legendary enemies are spawned at
        irregular intervals to provide a challenging and unpredictable gameplay experience.
        """
        self.legend_spawn_time -= 1
        if self.legend_spawn_time <= 0 and self.legendary_count > 0:
            self.legendary.add(Legendary_Enemy(choice(["right", "left"])))
            self.legend_spawn_time = randint(400, 800)
            self.legendary_count -= 1
    
    def display_lives_score(self, screen):
        """Displays the current score and player's lives on the game screen.
        
        This method is responsible for rendering the score and player health information on the game screen. It uses
        the `self.font` object to render the text, and positions the score text in the top-left corner and the health 
        text in the top-right corner of the screen.
        """
        score = self.font.render("Score: " + str(self.score), False, 'white')
        score_rect = score.get_rect(topleft=(10,0))
        screen.blit(score, score_rect)
        score = self.font.render("Health: " + str(self.lives), False, 'white')
        score_rect = score.get_rect(topright=(710,0))
        screen.blit(score, score_rect)
    
    def check_collisions(self):
        """Checks for collisions between various game objects and updates the game state accordingly.
        
        This method handles the following collision detection and resolution:
        - Checks if the player's bullets collide with blocks, enemies, legendary enemies, or enemy bullets, 
          and updates the score and removes the colliding objects as appropriate.
        - Checks if enemies collide with blocks or the player, and updates the game over state if the player is hit.
        - Checks if enemy bullets collide with blocks or the player, and reduces the player's lives if hit.
        """
        if self.player.sprite.bullets:
            for bul in self.player.sprite.bullets:
                if pygame.sprite.spritecollide(bul, self.blocks, True):
                    bul.kill()
                enemy_hit_list = pygame.sprite.spritecollide(bul, self.enemies, False)
                if enemy_hit_list:
                    for enemy in enemy_hit_list:
                        enemy.health -= 1
                        self.score += enemy.value
                        bul.kill()
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
                    self.game_over = -1
                    self.lives = -1
        if self.enemy_bullets:
            for bul in self.enemy_bullets:
                if pygame.sprite.spritecollide(bul, self.blocks, True):
                    bul.kill()
                if pygame.sprite.spritecollide(bul, self.player, False):
                    bul.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = -1
    
    def victory_message(self, screen):
        """Checks if the player has defeated all enemies, and if so, sets the `game_over` flag to 1 to indicate a victory."""
        if not self.enemies.sprites():
            self.game_over = 1
    
    def update(self, screen):
        """Updates the game state and draws the game objects on the screen.
        
        This method is responsible for the following:
        - Updating the player's position and bullets
        - Updating the enemies' positions and shooting
        - Checking for collisions between various game objects
        - Checking if the player has won the game
        - Drawing the player, enemies, bullets, and blocks on the screen
        - Displaying the player's lives and score
        
        If the game is over, this method returns the next level, the player's score, and the player's lives.
        """
        if self.game_over == 0:
            self.player.update()
            self.enemies.update(self.enemy_direction)
            self.enemy_position_checker()
            self.enemy_shoot()
            self.enemy_bullets.update()
            self.enemy_bullets.draw(screen)
            self.legendary_spawner()
            self.legendary_shoot()
            self.legendary.draw(screen)
            self.legendary.update()
            
            self.check_collisions()
            self.victory_message(screen)
            
            self.player.sprite.bullets.draw(screen)
            self.player.draw(screen)
            self.display_lives_score(screen)
            
            self.blocks.draw(screen)
            self.enemies.draw(screen)
            return None, 0, None
        elif self.game_over == -1:
            self.music.stop()
            return self.level, self.score, -1
        elif self.game_over == 1:
            self.music.stop()
            return self.level+1, self.score, self.lives+1

class Spaceship(pygame.sprite.Sprite):
    """Represents the player's spaceship in the game. The spaceship can move left and right, and shoot bullets.
    
    Attributes:
        bullet_sound (pygame.mixer.Sound): The sound played when the player fires a bullet.
        image (pygame.Surface): The image of the spaceship.
        rect (pygame.Rect): The bounding box of the spaceship.
        speed (int): The speed at which the spaceship moves.
        can_shoot (bool): A flag indicating whether the player can shoot a bullet.
        bullet_time (int): The time since the last bullet was fired.
        bullet_cooldown (int): The minimum time between each bullet fired.
    """
    
    def __init__(self):
        """Initializes the player's spaceship in the game. [No Args]"""
        super().__init__()
        self.bullet_sound = pygame.mixer.Sound("Assets/bullet.wav")
        self.bullet_sound.set_volume(0.5)
        self.image = pygame.image.load("Assets\player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(360,680))
        self.speed = 8
        self.can_shoot = True
        self.bullet_time = 0
        self.bullet_cooldown = 450
        
        self.bullets = pygame.sprite.Group()
    
    def update(self):
        """Updates the player's spaceship movement and shooting.
        
        This method is responsible for handling the player's input to move the spaceship left and right, 
        and to shoot bullets. It checks for key presses and updates the spaceship's position and bullet 
        firing accordingly.
        """
        self.move_shoot()
        self.bullets.update()
    
    def move_shoot(self):
        """Handles the movement and shooting of the player's spaceship.
        
        This method is responsible for updating the position of the spaceship based on the player's input, and for 
        firing bullets when the player presses the spacebar.
        The spaceship can move left and right, but is constrained within the game window. The player can only fire
        a bullet if the `can_shoot` flag is set to `True`, which is controlled by a cooldown timer to limit the rate of fire.
        """
        
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
        """Shoots a new bullet from the player's spaceship.
        
        This method creates a new Bullet object and adds it to the player's bullets group. The bullet is positioned at the center of the player's spaceship's rectangle.
        """
        self.bullets.add(Bullet(self.rect.center))
    

class Fortification(pygame.sprite.Sprite):
    """Represents a fortification object in the game.
    
    The `Fortification` class is a sprite that represents a fortification or barrier in the game. It is used to create obstacles that can be destroyed by enemy fire.
    
    Attributes:
        image (pygame.Surface): The "image" of the fortification.
        rect (pygame.Rect): The rectangle that defines the position and size of the fortification.
    """
    
    def __init__(self, size, colour, x, y):
        """Initializes a new Bullet object with the specified size, color, and starting position.
        
        Args:
            size (int): The size of the fortification.
            colour (tuple/str): The RGB color of the bullet or the string name of the bullet.
            x (int): The x-coordinate of the bullet's starting position.
            y (int): The y-coordinate of the bullet's starting position.
        """
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(colour)
        self.rect = self.image.get_rect(topleft=(x,y))
    

class Enemy(pygame.sprite.Sprite):
    """Represents an abstract enemy in the game.
    
    The `Enemy` class is a sprite that represents an abstract enemy character in the game. It has attributes 
    for its image, position, health, and value. The class also includes methods for shooting a bullet and handling the enemy's death.
    
    Attributes:
        image (pygame.Surface): The image of the enemy character.
        rect (pygame.Rect): The rectangle that defines the position and size of the enemy character.
        value (int): The score value of the enemy character.
        health (int): The health of the enemy character.
        explosion_sound (pygame.mixer.Sound): The sound effect played when the enemy character is destroyed.
    """

    def __init__(self, type, x, y, health=1, val=10):
        """
        Initializes a new Enemy object with the specified type, starting position, health, and value.
        
        Args:
            type (str): The type of the enemy character (e.g. "Rare", "Epic", "Mythic").
            x (int): The x-coordinate of the enemy's starting position.
            y (int): The y-coordinate of the enemy's starting position.
            health (int, optional): The health of the enemy character. Defaults to 1.
            val (int, optional): The score value of the enemy character. Defaults to 10.
        """
        super().__init__()
        self.image = pygame.image.load("Assets/Alien_" + type + ".png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.value = val
        self.health = health
        self.explosion_sound = pygame.mixer.Sound("Assets/explosion.wav")
        self.explosion_sound.set_volume(0.3)
    
    def shoot(self):
        """Shoots a red bullet from the center of the enemy's rectangle.
        
        Returns:
            Bullet: A new bullet object with the specified properties.
        """
        bullet = Bullet(self.rect.center, -6, "red")
        return bullet
    
    def update(self, direction):
        """Updates the position of the enemy based on the given direction, and plays the explosion sound effect if the enemy's health is 0 or less, then removes the enemy from the game.
        
        Args:
            direction (int): The horizontal direction to move the enemy, where a positive value moves the enemy to the right and a negative value moves the enemy to the left.
        """
        self.rect.x += direction
        if self.health <= 0:
            self.explosion_sound.play()
            self.kill()
    

class Rare_Enemy(Enemy):
    """Represents a rare enemy in the Space Invaders game.
    
    The `Rare_Enemy` class inherits from the `Enemy` class and represents a rare enemy character. It has a unique shooting 
    behaviour, where it fires a bullet with a yellow-orange color.
    
    Attributes:
        All of the attributes are inherited from the Enemy class.
    """
        
    def __init__(self, x, y):
        """Initializes a new instance of the Rare_Enemy class.
        
        Args:
            x (int): The x-coordinate of the enemy's starting position.
            y (int): The y-coordinate of the enemy's starting position.
        """
        super().__init__("Rare", x, y)
    
    def shoot(self):
        """Shoots a yellow-orange bullet from the center of the enemy's rectangle.
        
        Returns:
            Bullet: A new bullet object with the specified properties.
        """
        bullet = Bullet(self.rect.center, -6, (255, 196, 0))
        return bullet
    

class Epic_Enemy(Enemy):
    """Represents a epic enemy in the Space Invaders game.
    
    The `Epic_Enemy` class inherits from the `Enemy` class and represents an epic enemy character. It has a unique shooting 
    behaviour, where it fires a bullet with an orange color.
    
    Attributes:
        All of the attributes are inherited from the Enemy class.
    """
    def __init__(self, x, y):
        """Initializes a new instance of the Epic_Enemy class.
        
        Args:
            x (int): The x-coordinate of the enemy's starting position.
            y (int): The y-coordinate of the enemy's starting position.
        """
        super().__init__("Epic", x, y, 2, 20)
    
    def shoot(self):
        """Shoots a yellow-orange bullet from the center of the enemy's rectangle.
        
        Returns:
            Bullet: A new bullet object with the specified properties.
        """
        bullet = Bullet(self.rect.center, -6, (255, 128, 0))
        return bullet
    


class Mythic_Enemy(Enemy):
    """Represents a mythic enemy in the Space Invaders game.
    
    The `Mythic_Enemy` class inherits from the `Enemy` class and represents a Mythic enemy character. It has a unique shooting 
    behaviour, where it fires a bullet with a red color.
    
    Attributes:
        All of the attributes are inherited from the Enemy class.
    """
    def __init__(self, x, y):
        """Initializes a new instance of the Mythic_Enemy class.
        
        Args:
            x (int): The x-coordinate of the enemy's starting position.
            y (int): The y-coordinate of the enemy's starting position.
        """
        super().__init__("Mythic", x, y, 3, 40)
    
    def shoot(self):
        """Shoots a yellow-orange bullet from the center of the enemy's rectangle.
        
        Returns:
            Bullet: A new bullet object with the specified properties.
        """
        bullet = Bullet(self.rect.center, -6, "red")
        return bullet
    

#* The behaviour of this enemy is so different to the normal enemies
#* that it is not worth inheriting from the base class.
class Legendary_Enemy(pygame.sprite.Sprite):
    """Represents a legendary enemy in the Space Invaders game.
    
    The `Legendary_Enemy` class is a sprite that represents a legendary enemy character in the Space Invaders game. 
    It has a unique movement and shooting behaviour, where it moves horizontally across the screen and shoots three red bullets at once.
    
    Attributes:
        image (pygame.Surface): The image of the legendary enemy.
        rect (pygame.Rect): The rectangle representing the legendary enemy's position and size.
        speed (int): The horizontal speed of the legendary enemy.
    """
    
    def __init__(self, side):
        """Initializes a new instance of the Legendary_Enemy class.
        
        Args:
            side (str): Specifies whether the enemy should start on the right or left side of the screen. Can be either "right" or "left".
        """
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
        """Updates the x-coordinate of the sprite's rectangle by the current speed value."""
        self.rect.x += self.speed
    
    def shoot(self):
        """Shoots three red bullets from the center of the enemy's rectangle.
        
        Returns:
            tuple (Bullet, Bullet, Bullet): A tuple of three new bullet objects with the specified properties.
        """
        x, y = self.rect.center
        bullet1 = Bullet((x-20, y), -6, "red")
        bullet2 = Bullet((x, y), -6, "red")
        bullet3 = Bullet((x+20, y), -6, "red")
        return bullet1, bullet2, bullet3

class Bullet(pygame.sprite.Sprite):
    """Represents a bullet in the Space Invaders game.
    
    The `Bullet` class is a sprite that represents a bullet fired by the player or an enemy in the Space Invaders game.
    It has a fixed size and color, and moves vertically at a specified speed.
    
    Attributes:
        image (pygame.Surface): The image of the bullet.
        rect (pygame.Rect): The rectangle representing the bullet's position and size.
        speed (int): The vertical speed of the bullet.
    """
    def __init__(self, position, speed=8, colour="yellow"):
        """Initializes a new instance of the Bullet class.
        
        Args:
            position (tuple): The initial position of the bullet as a (x, y) tuple.
            speed (int, optional): The vertical speed of the bullet. Defaults to 8.
            colour (str, optional): The color of the bullet. Defaults to "yellow".
        """
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image.fill(colour)
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
    
    def update(self):
        """Updates the y-coordinate of the bullet's rectangle by the current speed value. If the bullet goes off the top or bottom of the screen, it is removed from the game."""
        self.rect.y -= self.speed
        if self.rect.y <= -50 or self.rect.y >= 770:
            self.kill()
