
import pygame
pygame.init()

"""
getXToCenter({surface}, {window}, {isRect (default false)})
return type - int

gets the surface that you want to center and returns the value of the X coordinate that
can be used to center the surface by providing the correct coordinate
"""
def getXToCenter(surface, window, isRect=False):

    #gets the x value with which the text will be centered,
    #returns an int

    if not isRect:

        rect = surface.get_rect()

    elif isRect:

        rect = surface

    temp = (window.get_width()/2 - (rect.width/2))
    return temp

"""
getCollisionStatus({surface}, {x}, {y}, {mouseDown}, {isRect (default false)})

function to check for mouse collisions based of the surface, the coordinates and if the mouse is down.
returns if there is a collision between the mouse and a certain surface.
"""
def getCollisionStatus(surface, x=int, y=int, mouseDown=bool, isRect=False):

    #finds the coordinate of the mouse and checks if it collides with the
    #provided surface, returns a boolean

    mouseCoordinate = pygame.mouse.get_pos()

    #creating the hitbox used for collisions
    if not isRect:
        rect = surface.get_rect(topleft = (x, y))
    else:
        rect = surface

    if rect.collidepoint(mouseCoordinate) and mouseDown:
        return True
    else:
        return False
    
