from SpaceInvaders import *
import pygame, sys, os

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
pygame.display.set_caption('Space Invaders')
pygame.display.set_icon(pygame.image.load('Assets/Icon.png'))
level, score = 0 
lives = 1
dt = 0

while True:
    game = Game(level=level, score=score, lives=lives)
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
    if input() != "Yes":
        break
