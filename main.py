import pygame
pygame.init()
import graphicsfunctions

w = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    w.fill((255, 255, 255))
    pygame.display.flip()


    clock.tick(60)
