
import pygame
pygame.init()
import graphicsfunctions as grf


start = True
handInput = False
mouseDown = False
numberDrawDownClicked = False
suitDrawDownClicked = False
userHand = []
communityCards = []
allCardValues = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
allSuitValues = ["S", "C", "D", "H"]
nddPlaceholder = "-"
nddValue = None
sddPlaceholder = "-"
sddValue = None
viewHands = False

w = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
bigFont = pygame.font.Font("Oswald/Oswald-VariableFont_wght.ttf", 80)
font = pygame.font.Font("Oswald/Oswald-VariableFont_wght.ttf", 15)
mediumFont = pygame.font.Font("Oswald/Oswald-VariableFont_wght.ttf", 30)
texasPicture = pygame.image.load("randomPicturesAndStuff/texas.jpg")
texasPicture = pygame.transform.scale(texasPicture, (400, 400))
beginButton = pygame.image.load("randomPicturesAndStuff/beginButton.png")
beginButton = pygame.transform.scale(beginButton, (150, 75))
nextButton = pygame.image.load("randomPicturesAndStuff/nextButton.png")
nextButton = pygame.transform.scale(nextButton, (150, 75))




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
        suitDrawDownX = 500
        y = 80
      
        w.blit(nextButton, (grf.getXToCenter(nextButton, w), 650))
        w.blit(font.render("CARD #", True, (0, 0, 0)), (numberDrawDownX + 30, 90))
        w.blit(font.render("SUIT", True, (0, 0, 0)), (suitDrawDownX + 30, 90))
        header = font.render("Input Cards - Card # " + str(len(userHand) + 1) + " of 2", True, (0, 0, 0))
        w.blit(header, (grf.getXToCenter(header, w), 50))
      
        #making input for the number of cards


      
        if not numberDrawDownClicked:


            #drawing a rect to be the dropdown menu placeholder
            rect = pygame.Rect(numberDrawDownX, (y + 50), 100, 50)
            pygame.draw.rect(w, (220, 220, 220), rect)


            w.blit(font.render(nddPlaceholder, True, (0, 0, 0)), ((numberDrawDownX + 45), (y + 60)))


            if grf.getCollisionStatus(rect, numberDrawDownX, y, mouseDown, True):


                mouseDown = False
                numberDrawDownClicked = True


        else:


            for i in range(0, len(allCardValues)):


              
                #Drawing a rect for each of the values in the list
                w.blit(font.render(nddPlaceholder, True, (0, 0, 0)), ((numberDrawDownX + 45), (y + 60)))
                rect = pygame.Rect(numberDrawDownX, (y + (50*(i + 1))), 100, 50)
                pygame.draw.rect(w, (200, 200, 200), rect)
                w.blit(font.render(allCardValues[i], True, (0, 0, 0)), ((numberDrawDownX + 45), (y + 10 + (50*(i + 1)))))
              
                #checking to see which input the user selects and then adding that to the list of cards
                #done for each of the rects in the dropdown menu


                if grf.getCollisionStatus(rect, rect.x, y, mouseDown, True):


                    nddValue = allCardValues[i]
                    nddPlaceholder = allCardValues[i]


                  
                    numberDrawDownClicked = False
                    #waiting so it does not automatically double click
                    pygame.time.wait(100)

        if not suitDrawDownClicked:

            #drawing a rect to be the dropdown menu placeholder
            rect = pygame.Rect(suitDrawDownX, (y + 50), 100, 50)
            pygame.draw.rect(w, (220, 220, 220), rect)


            w.blit(font.render(sddPlaceholder, True, (0, 0, 0)), ((suitDrawDownX + 45), (y + 60)))


            if grf.getCollisionStatus(rect, suitDrawDownX, y, mouseDown, True):


                mouseDown = False
                suitDrawDownClicked = True

        else:

            for i in range(0, len(allSuitValues)):


              
                #Drawing a rect for each of the values in the list
              
                rect = pygame.Rect(suitDrawDownX, (y + (50*(i + 1))), 100, 50)
                pygame.draw.rect(w, (200, 200, 200), rect)
                w.blit(font.render(allSuitValues[i], True, (0, 0, 0)), ((suitDrawDownX + 45), (y + 10 + (50*(i + 1)))))
              
                #checking to see which input the user selects and then adding that to the list of cards
                #done for each of the rects in the dropdown menu


                if grf.getCollisionStatus(rect, rect.x, y, mouseDown, True):


                    sddValue = allSuitValues[i]
                    sddPlaceholder = allSuitValues[i]


                  
                    suitDrawDownClicked = False
                    #waiting so it does not automatically double click
                    pygame.time.wait(100)


       #adding to the list and ending the section when neccesary
        if grf.getCollisionStatus(nextButton, grf.getXToCenter(nextButton, w), 650, mouseDown) and sddPlaceholder != "-" and nddPlaceholder != "-":

          
            userHand.append(sddValue + nddValue)

            if len(userHand) >= 2:

                viewHands = True
                handInput = False

            #resetting all variables to take input again
            nddValue = None
            sddValue = None
            nddPlaceholder = "-"
            sddPlaceholder = "-"
            numberDrawDownClicked = False
            suitDrawDownClicked = False

    if viewHands:

        header = bigFont.render("AVAILABLE CARDS", True, (0, 0, 0))
        w.blit(header, (grf.getXToCenter(header, w), 60))

        

        for i in range(0, len(userHand)):

            w.blit(mediumFont.render("YOUR HAND", True, (0, 0, 0)), (30, 200))
            text = font.render(userHand[i], True, (0, 0, 0))
            w.blit(text, (85, 240 + (i*30)))

        if len(communityCards) > 0:

            for i in range(0, len(userHand)):

                w.blit(mediumFont.render("COMMUNITY CARDS", True, (0, 0, 0)), (770, 200))
                text = font.render(communityCards[i], True, (0, 0, 0))
                w.blit(text, (715, 240 + (i*30)))


      
    pygame.display.flip()


    clock.tick(60)