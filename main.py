from SpaceInvaders import *
from button import Button
import pygame, sys, os

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
pygame.display.set_caption('Space Invaders')
pygame.display.set_icon(pygame.image.load('Assets/Icon.png'))
level, score, last_score, lives = 0, 0, 0, 1
dt = 0

def play():
    global level, score, last_score, lives
    game = Game(level=level, score=score, lives=lives)
    screen.fill((30,30,30))
    while True:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os.system('cls') #TODO: Remove in the final release
                sys.exit()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill((30,30,30))
        level, score, lives = game.update(screen)
        # flip() the display to put your work on screen
        pygame.display.flip()
        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
        if int(score) > last_score:
            #pygame.quit()
            last_score = score
            break
        elif lives == -1:
            print(level, score)
            #sys.exit()
            break
    if lives == -1:
        lives = 1
        defeat(level, score)
    elif last_score == score and score != 0:
        victory()

def main_menu():
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
    font = pygame.font.Font("Assets/Pixeled.ttf", 40)
    font2 = pygame.font.Font("Assets/Pixeled.ttf", 20)
    while True:
        defeat_mouse_position = pygame.mouse.get_pos()

        defeat_text = font.render("Level " + str(level) + " Failed!", False, "red")
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

while True:
    main_menu()
    if input("Yes: ") != "y":
        break
