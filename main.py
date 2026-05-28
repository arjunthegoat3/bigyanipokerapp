import pygame
pygame.init()
import graphicsfunctions as grf

# ---------------- VARIABLES ----------------

start = True
handInput = False
viewCards = False

mouseDown = False

numberDrawDownClicked = False
suitDrawDownClicked = False

userHand = []
communityCards = []

allCardValues = [
    "ACE", "2", "3", "4", "5", "6",
    "7", "8", "9", "10", "Jack", "Queen", "King"
]

allSuitValues = [
    "Spades", "Clovers", "Diamonds", "Hearts"
]

nddPlaceholder = "-"
sddPlaceholder = "-"

nddValue = None
sddValue = None

# ---------------- WINDOW ----------------

w = pygame.display.set_mode((800, 800))

clock = pygame.time.Clock()

bigFont = pygame.font.Font("Oswald/Oswald-VariableFont_wght.ttf", 80)
<<<<<<< Updated upstream
font = pygame.font.Font("Oswald/Oswald-VariableFont_wght.ttf", 20)

# ---------------- IMAGES ----------------

=======
font = pygame.font.Font("Oswald/Oswald-VariableFont_wght.ttf", 15)
mediumFont = pygame.font.Font("Oswald/Oswald-VariableFont_wght.ttf", 30)
>>>>>>> Stashed changes
texasPicture = pygame.image.load("randomPicturesAndStuff/texas.jpg")
texasPicture = pygame.transform.scale(texasPicture, (400, 400))

beginButton = pygame.image.load("randomPicturesAndStuff/beginButton.png")
beginButton = pygame.transform.scale(beginButton, (150, 75))

nextButton = pygame.image.load("randomPicturesAndStuff/nextButton.png")
nextButton = pygame.transform.scale(nextButton, (150, 75))

# ---------------- POKER DECISION FUNCTION ----------------

def getDecision(hand, community):

    values = []

    for card in hand:

        values.append(card[0])

    # Pocket Aces
    if values.count("ACE") == 2:

        return "RAISE"

    # Any Pair
    elif len(values) == 2 and values[0] == values[1]:

        return "CALL"

    # Ace King
    elif "ACE" in values and "King" in values:

        return "CALL"

    # Ace Queen
    elif "ACE" in values and "Queen" in values:

        return "CALL"

    else:

        return "FOLD"

# ---------------- MAIN LOOP ----------------

running = True

while running:

    # RESET CLICK EACH FRAME
    mouseDown = False

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouseDown = True

    # BACKGROUND
    w.fill((255, 255, 255))

    # =====================================================
    # START SCREEN
    # =====================================================

    if start:

        titleFont = bigFont.render("TEXAS HOLD EM APP", True, (0, 0, 0))

        w.blit(titleFont, (grf.getXToCenter(titleFont, w), 100))

        w.blit(texasPicture, (grf.getXToCenter(texasPicture, w), 220))

        w.blit(beginButton, (grf.getXToCenter(beginButton, w), 650))

        # BEGIN BUTTON
        if grf.getCollisionStatus(
            beginButton,
            grf.getXToCenter(beginButton, w),
            650,
            mouseDown
        ):

            start = False
            handInput = True

    # =====================================================
    # HAND INPUT SCREEN
    # =====================================================

    if handInput:

        numberDrawDownX = 200
        suitDrawDownX = 500
        y = 80

        # NEXT BUTTON
        w.blit(nextButton, (grf.getXToCenter(nextButton, w), 650))

        # LABELS
        w.blit(font.render("CARD #", True, (0, 0, 0)),
               (numberDrawDownX + 20, 90))

        w.blit(font.render("SUIT", True, (0, 0, 0)),
               (suitDrawDownX + 20, 90))

        # HEADER TEXT
        if len(userHand) < 2:

            headerText = (
                "Input Player Card "
                + str(len(userHand) + 1)
                + " of 2"
            )

        else:

            headerText = (
                "Input Community Card "
                + str(len(communityCards) + 1)
                + " of 5"
            )

        header = font.render(headerText, True, (0, 0, 0))

        w.blit(header, (grf.getXToCenter(header, w), 50))

        # =================================================
        # VALUE DROPDOWN
        # =================================================

        if not numberDrawDownClicked:

            rect = pygame.Rect(numberDrawDownX, y + 50, 100, 50)

            pygame.draw.rect(w, (220, 220, 220), rect)

            valueText = font.render(nddPlaceholder, True, (0, 0, 0))

            w.blit(valueText, (numberDrawDownX + 35, y + 60))

            if grf.getCollisionStatus(
                rect,
                rect.x,
                rect.y,
                mouseDown,
                True
            ):

                numberDrawDownClicked = True

        else:

            for i in range(len(allCardValues)):

                rect = pygame.Rect(
                    numberDrawDownX,
                    y + (50 * (i + 1)),
                    100,
                    50
                )

                pygame.draw.rect(w, (200, 200, 200), rect)

                text = font.render(allCardValues[i], True, (0, 0, 0))

                w.blit(
                    text,
                    (numberDrawDownX + 20, y + 10 + (50 * (i + 1)))
                )

                if grf.getCollisionStatus(
                    rect,
                    rect.x,
                    rect.y,
                    mouseDown,
                    True
                ):

                    nddValue = allCardValues[i]
                    nddPlaceholder = allCardValues[i]

                    numberDrawDownClicked = False

        # =================================================
        # SUIT DROPDOWN
        # =================================================

        if not suitDrawDownClicked:

            rect = pygame.Rect(suitDrawDownX, y + 50, 100, 50)

            pygame.draw.rect(w, (220, 220, 220), rect)

            suitText = font.render(sddPlaceholder, True, (0, 0, 0))

            w.blit(suitText, (suitDrawDownX + 15, y + 60))

            if grf.getCollisionStatus(
                rect,
                rect.x,
                rect.y,
                mouseDown,
                True
            ):

                suitDrawDownClicked = True

        else:

            for i in range(len(allSuitValues)):

                rect = pygame.Rect(
                    suitDrawDownX,
                    y + (50 * (i + 1)),
                    100,
                    50
                )

                pygame.draw.rect(w, (200, 200, 200), rect)

                text = font.render(allSuitValues[i], True, (0, 0, 0))

                w.blit(
                    text,
                    (suitDrawDownX + 10, y + 10 + (50 * (i + 1)))
                )

                if grf.getCollisionStatus(
                    rect,
                    rect.x,
                    rect.y,
                    mouseDown,
                    True
                ):

                    sddValue = allSuitValues[i]
                    sddPlaceholder = allSuitValues[i]

                    suitDrawDownClicked = False

        # =================================================
        # NEXT BUTTON LOGIC
        # =================================================

        if grf.getCollisionStatus(
            nextButton,
            grf.getXToCenter(nextButton, w),
            650,
            mouseDown
        ):

            # Make sure dropdowns selected
            if nddValue != None and sddValue != None:

                card = (nddValue, sddValue)

                # PLAYER HAND
                if len(userHand) < 2:

                    if card not in userHand:

                        userHand.append(card)

                # COMMUNITY CARDS
                else:

                    if (
                        card not in userHand
                        and card not in communityCards
                    ):

                        communityCards.append(card)

                # RESET DROPDOWNS
                nddValue = None
                sddValue = None

                nddPlaceholder = "-"
                sddPlaceholder = "-"

                numberDrawDownClicked = False
                suitDrawDownClicked = False

                # MOVE TO RESULTS SCREEN
                if len(userHand) == 2 and len(communityCards) == 5:

                    handInput = False
                    viewCards = True

    # =====================================================
    # RESULTS SCREEN
    # =====================================================

    if viewCards:

        header = bigFont.render("AVAILABLE CARDS", True, (0, 0, 0))

        w.blit(header, (grf.getXToCenter(header, w), 50))

        # DECISION
        decision = getDecision(userHand, communityCards)

        decisionText = bigFont.render(decision, True, (255, 0, 0))

        w.blit(decisionText, (250, 600))

        # PLAYER HAND
        playerHeader = font.render("Player Hand", True, (0, 0, 0))

        w.blit(playerHeader, (100, 120))

        for i in range(len(userHand)):

<<<<<<< Updated upstream
            cardText = str(userHand[i])
=======
            w.blit(mediumFont.render("YOUR CARDS", True, (0, 0, 0)), (100, 210))
            card = font.render(userHand[i], True, (0, 0, 0))
            w.blit(card, (100, 250+(i*20)))
        
      
    pygame.display.flip()
>>>>>>> Stashed changes

            cardSurface = font.render(cardText, True, (0, 0, 0))

            w.blit(cardSurface, (100, 160 + (i * 40)))

        # COMMUNITY CARDS
        communityHeader = font.render(
            "Community Cards",
            True,
            (0, 0, 0)
        )

        w.blit(communityHeader, (400, 120))

        for i in range(len(communityCards)):

            cardText = str(communityCards[i])

            cardSurface = font.render(cardText, True, (0, 0, 0))

            w.blit(cardSurface, (400, 160 + (i * 40)))

    # UPDATE SCREEN
    pygame.display.flip()

    clock.tick(60)

pygame.quit()