import pygame
pygame.init()


def getXToCenter(surface, window, isRect=False):

    if not isRect:
        rect = surface.get_rect()
    else:
        rect = surface

    return window.get_width()/2 - rect.width/2


def getCollisionStatus(surface, x, y, mouseDown=False, isRect=False):

    mouseCoordinate = pygame.mouse.get_pos()

    # make hitbox
    if not isRect:
        rect = surface.get_rect(topleft=(x, y))
    else:
        rect = surface.copy()
        rect.topleft = (x, y)

    return rect.collidepoint(mouseCoordinate) and mouseDown