import pygame

SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chrome Dino Runner")

Ico = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(Ico)

FONT_COLOR=(0,0,0)

GAME_SPEED = 15