import pygame
pygame.init()
import graphicsfunctions as grf

start = True
handInput = False
mouseDown = False
numberDrawDownClicked = False
userHand = []
communityCards = []
allCardValues = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K"]
nddPlaceholder = "-"

w = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
bigFont = pygame.font.Font("Oswald/Oswald-VariableFont_wght.ttf", 80)
font = pygame.font.Font("Oswald/Oswald-VariableFont_wght.ttf", 15)
texasPicture = pygame.image.load("randomPicturesAndStuff/texas.jpg")
texasPicture = pygame.transform.scale(texasPicture, (400, 400))
beginButton = pygame.image.load("randomPicturesAndStuff/beginButton.png")
beginButton = pygame.transform.scale(beginButton, (150, 75))


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:

            mouseDown = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouseDown = True


    w.fill((255, 255, 255))

    if start:

        #adding the screen elements
        titleFont = bigFont.render("TEXAS HOLD EM APP", True, (0, 0, 0))
        w.blit(titleFont, (grf.getXToCenter(titleFont, w), 100))
        w.blit(texasPicture, ((grf.getXToCenter(texasPicture, w)), 220))
        w.blit(beginButton, (grf.getXToCenter(beginButton, w), 650))

        #checking to see if to move to the next screen

        if grf.getCollisionStatus(beginButton, grf.getXToCenter(beginButton, w), 650, mouseDown):

            handInput = True
            start = False

    #hand inputting section

    if handInput:

        numberDrawDownX = 200
        suitDrawDownx = 600
        y = 120
        

        
        #making input for the number of cards

        
        if not numberDrawDownClicked:

            rect = pygame.Rect(numberDrawDownX, (y + 50), 100, 50)
            pygame.draw.rect(w, (220, 220, 220), rect)

            w.blit(font.render(nddPlaceholder, True, (0, 0, 0)), ((numberDrawDownX + 45), (y + 60)))

            if grf.getCollisionStatus(rect, numberDrawDownX, y, mouseDown, True):

                mouseDown = False
                numberDrawDownClicked = True

        else:

            for i in range(0, len(allCardValues)):

                rect = pygame.Rect(numberDrawDownX, (y + (50*(i + 1))), 100, 50)
                pygame.draw.rect(w, (200, 200, 200), rect)
                w.blit(font.render(allCardValues[i], True, (0, 0, 0)), ((numberDrawDownX + 45), (y + 10 + (50*(i + 1)))))
                
                #checking to see which input the user selects and then adding that to the list of cards

                if grf.getCollisionStatus(rect, rect.x, y, mouseDown, True):

                    userHand.append(allCardValues[i])
                    nddPlaceholder = allCardValues[i]

                    numberDrawDownClicked = False

                    if len(userHand) >= 2:

                        handInput = False

                
        
    pygame.display.flip()

    clock.tick(60)
