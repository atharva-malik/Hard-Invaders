from SpaceInvaders import *
import pygame, sys, os

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
dt = 0
game = Game()

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

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
    game.update(screen)
    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
