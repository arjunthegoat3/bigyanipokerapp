import pygame
pygame.init()
import graphicsfunctions as grf

# screen states
start = True
handInput = False

# mouse
mouseDown = False

# dropdowns
numberDrawDownClicked = False
suitDropDownClicked = False

# card storage
userHand = []
communityCards = []

# card data
allCardSuits = ["Diamond", "Heart", "Spade", "Club"]
allCardValues = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

# dropdown placeholders
nddPlaceholder = "-"
sddPlaceholder = "-"

# currently selected card info
selectedValue = None
selectedSuit = None

# window
w = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

# fonts
bigFont = pygame.font.Font("Oswald/Oswald-VariableFont_wght.ttf", 80)
font = pygame.font.Font("Oswald/Oswald-VariableFont_wght.ttf", 20)

# images
texasPicture = pygame.image.load("randomPicturesAndStuff/texas.jpg")
texasPicture = pygame.transform.scale(texasPicture, (400, 400))

beginButton = pygame.image.load("randomPicturesAndStuff/beginButton.png")
beginButton = pygame.transform.scale(beginButton, (150, 75))

nextButton = pygame.image.load("randomPicturesAndStuff/nextButton.png")
nextButton = pygame.transform.scale(nextButton, (150, 75))


# poker decision helper
def getDecision(hand, community):

    values = []

    for card in hand:
        values.append(card[0])

    # pocket aces
    if values.count("A") == 2:
        return "RAISE"

    # any pair
    elif len(values) == 2 and values[0] == values[1]:
        return "CALL"

    # ace king
    elif "A" in values and "K" in values:
        return "CALL"

    else:
        return "FOLD"


running = True

while running:

    # reset mouse each frame
    mouseDown = False

    # events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True

    # background
    w.fill((255, 255, 255))

    # ================= START SCREEN =================

    if start:

        titleFont = bigFont.render("TEXAS HOLD EM APP", True, (0, 0, 0))

        w.blit(titleFont, (grf.getXToCenter(titleFont, w), 100))

        w.blit(texasPicture, (grf.getXToCenter(texasPicture, w), 220))

        w.blit(beginButton, (grf.getXToCenter(beginButton, w), 650))

        # start button collision
        if grf.getCollisionStatus(
            beginButton,
            grf.getXToCenter(beginButton, w),
            650,
            mouseDown
        ):

            handInput = True
            start = False

    # ================= HAND INPUT SCREEN =================

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


        # next button
        w.blit(nextButton, (grf.getXToCenter(nextButton, w), 650))

        # labels
        handLabel = font.render("Player Hand", True, (0, 0, 0))
        communityLabel = font.render("Community Cards", True, (0, 0, 0))

        w.blit(handLabel, (300, 150))
        w.blit(communityLabel, (500, 150))

        # ================= DISPLAY PLAYER HAND =================

        for i in range(len(userHand)):

            cardText = str(userHand[i])

            textSurface = font.render(cardText, True, (0, 0, 0))

            w.blit(textSurface, (300, 200 + (40 * i)))

        # ================= DISPLAY COMMUNITY CARDS =================

        for i in range(len(communityCards)):

            cardText = str(communityCards[i])

            textSurface = font.render(cardText, True, (0, 0, 0))

            w.blit(textSurface, (500, 200 + (40 * i)))

        # ================= VALUE DROPDOWN =================

        if not numberDrawDownClicked:


            #drawing a rect to be the dropdown menu placeholder
            rect = pygame.Rect(numberDrawDownX, (y + 50), 100, 50)

            pygame.draw.rect(w, (220, 220, 220), rect)

            w.blit(
                font.render(nddPlaceholder, True, (0, 0, 0)),
                (numberDrawDownX + 45, y + 60)
            )

            if grf.getCollisionStatus(rect, rect.x, rect.y, mouseDown, True):

                numberDrawDownClicked = True

        else:

            for i in range(len(allCardValues)):

                rect = pygame.Rect(
                    numberDrawDownX,
                    y + (50 * (i + 1)),
                    100,
                    50
                )


                
                #Drawing a rect for each of the values in the list
                
                rect = pygame.Rect(numberDrawDownX, (y + (50*(i + 1))), 100, 50)
                pygame.draw.rect(w, (200, 200, 200), rect)
                w.blit(font.render(allCardValues[i], True, (0, 0, 0)), ((numberDrawDownX + 45), (y + 10 + (50*(i + 1)))))
                
                #checking to see which input the user selects and then adding that to the list of cards
                #done for each of the rects in the dropdown menu

                w.blit(
                    font.render(allCardValues[i], True, (0, 0, 0)),
                    (numberDrawDownX + 40, y + 10 + (50 * (i + 1)))
                )

                if grf.getCollisionStatus(rect, rect.x, rect.y, mouseDown, True):

                    selectedValue = allCardValues[i]

                    nddPlaceholder = allCardValues[i]

                    numberDrawDownClicked = False


        #adding to the list and ending the program when neccesary
        if grf.getCollisionStatus(nextButton, grf.getXToCenter(nextButton, w), 650, mouseDown) and nddPlaceholder != "-":
        
            if len(userHand) >= 2:


                handInput = False


            nddValue = None
            nddPlaceholder = "-"
            numberDrawDownClicked = False


        if not suitDropDownClicked:

            rect = pygame.Rect(suitDrawDownX, y + 50, 100, 50)

            pygame.draw.rect(w, (220, 220, 220), rect)

            w.blit(
                font.render(sddPlaceholder, True, (0, 0, 0)),
                (suitDrawDownX + 20, y + 60)
            )

            if grf.getCollisionStatus(rect, rect.x, rect.y, mouseDown, True):

                suitDropDownClicked = True

        else:

            for i in range(len(allCardSuits)):

                rect = pygame.Rect(
                    suitDrawDownX,
                    y + (50 * (i + 1)),
                    100,
                    50
                )

                pygame.draw.rect(w, (200, 200, 200), rect)

                w.blit(
                    font.render(allCardSuits[i], True, (0, 0, 0)),
                    (suitDrawDownX + 10, y + 10 + (50 * (i + 1)))
                )

                if grf.getCollisionStatus(rect, rect.x, rect.y, mouseDown, True):

                    selectedSuit = allCardSuits[i]

                    sddPlaceholder = allCardSuits[i]

                    suitDropDownClicked = False

        # ================= CREATE CARD =================

        if selectedValue != None and selectedSuit != None:

            card = (selectedValue, selectedSuit)

            # first 2 cards = player hand
            if len(userHand) < 2:

                if card not in userHand:

                    userHand.append(card)

            # next 5 cards = community cards
            elif len(communityCards) < 5:

                if card not in communityCards and card not in userHand:

                    communityCards.append(card)

            # reset selections
            selectedValue = None
            selectedSuit = None

            nddPlaceholder = "-"
            sddPlaceholder = "-"

        # ================= DECISION =================

        if len(userHand) == 2:

            decision = getDecision(userHand, communityCards)

            decisionText = bigFont.render(decision, True, (255, 0, 0))

            w.blit(decisionText, (220, 500))

    # update screen
    pygame.display.flip()

    # fps
    clock.tick(60)

pygame.quit()