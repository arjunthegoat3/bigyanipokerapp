import pygame
pygame.init()
import graphicsfunctions as grf

start = True

w = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
bigFont = pygame.font.Font("Oswald/Oswald-VariableFont_wght.ttf", 80)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    w.fill((255, 255, 255))

    if start:

        titleFont = bigFont.render("TEXAS HOLD EM APP", True, (0, 0, 0))
        w.blit(titleFont, (grf.getXToCenter(titleFont, w), 100))
    
    pygame.display.flip()

    clock.tick(60)
