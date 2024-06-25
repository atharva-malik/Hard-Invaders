"""This is the main file of the Space Invaders game.

This file initialises everything and contains the loop that runs the game logic contained within the classes imported from the 'SpaceInvaders' file. 
"""

from SpaceInvaders import *
from button import Button
import pygame, sys

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
pygame.display.set_caption('Space Invaders')
pygame.display.set_icon(pygame.image.load('Assets/Icon.png'))
level, score, last_score, lives = 0, 0, 0, 1
dt = 0

def play():
    """
    The `play()` function is the main game loop that runs the Space Invaders game. It initializes a `Game`
    object with the current level, score, and lives, and then enters a game loop that handles user input, 
    updates the game state, and renders the game on the screen. The loop continues until the player either 
    wins the current level or loses all their lives. If the player wins, the function breaks out of the loop
    and returns to the main menu. If the player loses, the function calls the `defeat()` function to handle 
    the game over state.
    """
    global level, score, last_score, lives
    game = Game(level=level, score=score, lives=lives)
    screen.fill((30,30,30))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((30,30,30))
        level, score, lives = game.update(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        if int(score) > last_score:
            last_score = score
            break
        elif lives == -1:
            break
    if lives == -1:
        lives = 1
        l = level
        s = score
        level = 0
        score = 0
        defeat(l, s)
    elif last_score == score and score != 0:
        victory()

def main_menu():
    """
    The `main_menu()` function is responsible for displaying the main menu of the Space Invaders game. 
    It creates a window with a title, icon, and a background color. The function then creates two buttons,
    one for starting the game and one for quitting the game. The function enters a game loop that handles
    user input, updates the game state, and renders the game on the screen. The loop continues until the 
    player either starts the game or quits the application.
    """
    font = pygame.font.Font("Assets/Pixeled.ttf", 40)
    font2 = pygame.font.Font("Assets/Pixeled.ttf", 20)
    while True:
        menu_mouse_position = pygame.mouse.get_pos()

        menu_text = font.render("MAIN MENU", False, "white")
        menu_rect = menu_text.get_rect(center=(360, 100))

        play_button = Button(image=None, pos=(360, 300), 
                            text_input="PLAY", font=font2, base_color="lightgreen", hovering_color="White")
        quit_button = Button(image=None, pos=(360, 500), 
                            text_input="QUIT", font=font2, base_color="lightgreen", hovering_color="red")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, quit_button]:
            button.changeColor(menu_mouse_position)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_position):
                    play()
                if quit_button.checkForInput(menu_mouse_position):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def victory():
    """
    The `victory()` function is responsible for displaying the victory screen when the player completes
    a level in the Space Invaders game. It creates a window with a title, icon, and a background color. 
    The function then creates two buttons, one for continuing to the next level and one for quitting the
    game. The function enters a game loop that handles user input, updates the game state, and renders the
    game on the screen. The loop continues until the player either continues to the next level or quits the
    application.
    """
    font = pygame.font.Font("Assets/Pixeled.ttf", 40)
    font2 = pygame.font.Font("Assets/Pixeled.ttf", 20)
    while True:
        victory_mouse_position = pygame.mouse.get_pos()

        victory_text = font.render("Level " + str(level) + " Complete!", False, "green")
        victory_rect = victory_text.get_rect(center=(360, 100))

        play_button = Button(image=None, pos=(360, 300), 
                            text_input="CONTINUE", font=font2, base_color="lightgreen", hovering_color="White")
        quit_button = Button(image=None, pos=(360, 500), 
                            text_input="QUIT", font=font2, base_color="lightgreen", hovering_color="red")

        screen.blit(victory_text, victory_rect)

        for button in [play_button, quit_button]:
            button.changeColor(victory_mouse_position)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(victory_mouse_position):
                    play()
                if quit_button.checkForInput(victory_mouse_position):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def defeat(level, score):
    """
    The `defeat()` function is responsible for displaying the defeat screen when the player fails a level
    in the Space Invaders game. It creates a window with a title, icon, and a background color. The function
    then creates two buttons, one for playing the level again and one for quitting the game. The function 
    enters a game loop that handles user input, updates the game state, and renders the game on the screen.
    The loop continues until the player either plays the level again or quits the application.
    
    Args:
        level (int): The last level of the game.
        score (int): The last score of the player.
    """
    font = pygame.font.Font("Assets/Pixeled.ttf", 40)
    font2 = pygame.font.Font("Assets/Pixeled.ttf", 20)
    while True:
        defeat_mouse_position = pygame.mouse.get_pos()

        defeat_text = font.render("Level " + str(level+1) + " Failed!", False, "red")
        defeat_rect = defeat_text.get_rect(center=(360, 100))

        defeat2_text = font.render((f"Score: {score}"), False, "white")
        defeat2_rect = defeat2_text.get_rect(center=(360, 200))
        defeat3_text = font.render((f"Level: {level}"), False, "white")
        defeat3_rect = defeat2_text.get_rect(center=(360, 300))
        
        play_button = Button(image=None, pos=(360, 450), 
                            text_input="PLAY AGAIN?", font=font2, base_color="lightgreen", hovering_color="White")
        quit_button = Button(image=None, pos=(360, 550), 
                            text_input="QUIT", font=font2, base_color="lightgreen", hovering_color="red")

        screen.blit(defeat_text, defeat_rect)
        screen.blit(defeat2_text, defeat2_rect)

        for button in [play_button, quit_button]:
            button.changeColor(defeat_mouse_position)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(defeat_mouse_position):
                    play()
                if quit_button.checkForInput(defeat_mouse_position):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

main_menu()
