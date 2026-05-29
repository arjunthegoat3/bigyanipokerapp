
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
firstTurn = True
secondTurn = False
thirdTurn = False
numberDrawDownX = 200
suitDrawDownX = 500
drawDownY = 80
reveal3 = False
fourthStreet = False
fifthStreet = False
inputtedCounter = 0

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

def cardInputtingDropDowns(cardList, cardNumber):

    global numberDrawDownClicked
    global suitDrawDownClicked
    global numberDrawDownX
    global suitDrawDownX
    global allCardValues
    global allSuitValues
    global nddPlaceholder
    global sddPlaceholder
    global nddValue
    global sddValue
    global mouseDown
    global inputtedCounter

    w.blit(nextButton, (grf.getXToCenter(nextButton, w), 650))
    w.blit(font.render("CARD #", True, (0, 0, 0)), (numberDrawDownX + 30, 90))
    w.blit(font.render("SUIT", True, (0, 0, 0)), (suitDrawDownX + 30, 90))  
    header = font.render("Input Cards - Card # " + str(inputtedCounter + 1) + " of " + str(cardNumber), True, (0, 0, 0))
    w.blit(header, (grf.getXToCenter(header, w), 50))

    if not numberDrawDownClicked:


        #drawing a rect to be the dropdown menu placeholder
        rect = pygame.Rect(numberDrawDownX, (drawDownY + 50), 100, 50)
        pygame.draw.rect(w, (220, 220, 220), rect)


        w.blit(font.render(nddPlaceholder, True, (0, 0, 0)), ((numberDrawDownX + 45), (drawDownY + 60)))


        if grf.getCollisionStatus(rect, numberDrawDownX, drawDownY, mouseDown, True):


            mouseDown = False
            numberDrawDownClicked = True


    else:


        for i in range(0, len(allCardValues)):


            
            #Drawing a rect for each of the values in the list
            w.blit(font.render(nddPlaceholder, True, (0, 0, 0)), ((numberDrawDownX + 45), (drawDownY + 60)))
            rect = pygame.Rect(numberDrawDownX, (drawDownY + (50*(i + 1))), 100, 50)
            pygame.draw.rect(w, (200, 200, 200), rect)
            w.blit(font.render(allCardValues[i], True, (0, 0, 0)), ((numberDrawDownX + 45), (drawDownY + 10 + (50*(i + 1)))))
            
            #checking to see which input the user selects and then adding that to the list of cards
            #done for each of the rects in the dropdown menu


            if grf.getCollisionStatus(rect, rect.x, drawDownY, mouseDown, True):


                nddValue = allCardValues[i]
                nddPlaceholder = allCardValues[i]


                
                numberDrawDownClicked = False
                #waiting so it does not automatically double click
                pygame.time.wait(100)

    if not suitDrawDownClicked:

        #drawing a rect to be the dropdown menu placeholder
        rect = pygame.Rect(suitDrawDownX, (drawDownY + 50), 100, 50)
        pygame.draw.rect(w, (220, 220, 220), rect)


        w.blit(font.render(sddPlaceholder, True, (0, 0, 0)), ((suitDrawDownX + 45), (drawDownY + 60)))


        if grf.getCollisionStatus(rect, suitDrawDownX, drawDownY, mouseDown, True):


            mouseDown = False
            suitDrawDownClicked = True

    else:

        for i in range(0, len(allSuitValues)):


            
            #Drawing a rect for each of the values in the list
            
            rect = pygame.Rect(suitDrawDownX, (drawDownY + (50*(i + 1))), 100, 50)
            pygame.draw.rect(w, (200, 200, 200), rect)
            w.blit(font.render(allSuitValues[i], True, (0, 0, 0)), ((suitDrawDownX + 45), (drawDownY + 10 + (50*(i + 1)))))
            
            #checking to see which input the user selects and then adding that to the list of cards
            #done for each of the rects in the dropdown menu


            if grf.getCollisionStatus(rect, rect.x, drawDownY, mouseDown, True):


                sddValue = allSuitValues[i]
                sddPlaceholder = allSuitValues[i]
                
                suitDrawDownClicked = False
                #waiting so it does not automatically double click
                pygame.time.wait(100)


    #adding to the list and ending the section when neccesary
    if grf.getCollisionStatus(nextButton, grf.getXToCenter(nextButton, w), 650, mouseDown) and sddPlaceholder != "-" and nddPlaceholder != "-":

        
        cardList.append(sddValue + nddValue)
        inputtedCounter += 1
        
        #resetting all variables to take input again
        nddValue = None
        sddValue = None
        nddPlaceholder = "-"
        sddPlaceholder = "-"
        numberDrawDownClicked = False
        suitDrawDownClicked = False
        mouseDown = False

    return cardList



cardRanks = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "10": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2
}

# =========================================================
# POKER HAND ANALYZER
# =========================================================

def getDecision(hand, community):

    allCards = hand + community

    values = []
    suits = []

    for card in allCards:

        values.append(card[0])
        suits.append(card[1])

    rankNumbers = []

    for value in values:

        rankNumbers.append(cardRanks[value])

    # -------------------------------------------------
    # COUNT PAIRS / TRIPS
    # -------------------------------------------------

    counts = {}

    for value in values:

        if value not in counts:

            counts[value] = 1

        else:

            counts[value] += 1

    pairCount = 0
    hasTrips = False
    hasQuads = False

    for value in counts:

        if counts[value] == 2:

            pairCount += 1

        elif counts[value] == 3:

            hasTrips = True

        elif counts[value] == 4:

            hasQuads = True

    # -------------------------------------------------
    # FLUSH CHECK
    # -------------------------------------------------

    flush = False

    for suit in allSuitValues:

        if suits.count(suit) >= 5:

            flush = True

    # -------------------------------------------------
    # STRAIGHT CHECK
    # -------------------------------------------------

    straight = False

    uniqueRanks = list(set(rankNumbers))

    uniqueRanks.sort()

    # ace low straight
    if 14 in uniqueRanks:

        uniqueRanks.insert(0, 1)

    streak = 1

    for i in range(len(uniqueRanks) - 1):

        if uniqueRanks[i + 1] == uniqueRanks[i] + 1:

            streak += 1

            if streak >= 5:

                straight = True

        else:

            streak = 1

    # -------------------------------------------------
    # HAND STRENGTH
    # -------------------------------------------------

    # Straight Flush
    if straight and flush:

        return "ALL IN"

    # Four of a Kind
    elif hasQuads:

        return "RAISE"

    # Full House
    elif hasTrips and pairCount >= 1:

        return "RAISE"

    # Flush
    elif flush:

        return "RAISE"

    # Straight
    elif straight:

        return "RAISE"

    # Three of a Kind
    elif hasTrips:

        return "CALL"

    # Two Pair
    elif pairCount >= 2:

        return "CALL"

    # One Pair
    elif pairCount == 1:

        return "CALL"

    # Strong High Cards
    elif (
        ("A" in values and "K" in values)
        or ("A" in values and "Q" in values)
        or ("K" in values and "Q" in values)
    ):

        return "CALL"

    else:

        return "FOLD"


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

        try:
            if len(userHand) >= 2:

                    inputtedCounter = 0
                    viewHands = True
                    handInput = False
                    pygame.time.wait(150)
        except:
            None

        userHand = cardInputtingDropDowns(userHand, 2)
        
      
        #making input for the number of cards

    if fifthStreet:

        try:
            if len(communityCards) >= 5:

                    inputtedCounter = 0
                    viewHands = True
                    fifthStreet = False
                    pygame.time.wait(150)
        except:
            None

        communityCards = cardInputtingDropDowns(communityCards, 1)

    
    if fourthStreet:

        try:
            if len(communityCards) >= 4:

                    inputtedCounter = 0
                    viewHands = True
                    fourthStreet = False
                    pygame.time.wait(150)
        except:
            None

        communityCards = cardInputtingDropDowns(communityCards, 1)

    elif reveal3:

        try:
            if len(communityCards) >= 3:

                    inputtedCounter = 0
                    viewHands = True
                    reveal3 = False
                    pygame.time.wait(150)

        except:
            None

        communityCards = cardInputtingDropDowns(communityCards, 3)
        

    if viewHands:

        #adding text elements
        header = bigFont.render("AVAILABLE CARDS", True, (0, 0, 0))
        w.blit(header, (grf.getXToCenter(header, w), 60))

        #making decision
        decision = getDecision(userHand, communityCards)
        decisionText = font.render(decision, True, (255, 0, 0))
        w.blit(decisionText, (grf.getXToCenter(decisionText, w), 400))

        w.blit(nextButton, (grf.getXToCenter(nextButton, w), 650))

        for i in range(0, len(userHand)):

            w.blit(mediumFont.render("YOUR HAND", True, (0, 0, 0)), (30, 200))
            text = font.render(userHand[i], True, (0, 0, 0))
            w.blit(text, (85, 240 + (i*30)))

        if len(communityCards) > 0:

            for i in range(0, len(communityCards)):

                w.blit(mediumFont.render("COMMUNITY CARDS", True, (0, 0, 0)), (570, 200))
                text = font.render(communityCards[i], True, (0, 0, 0))
                w.blit(text, (675, 240 + (i*30)))

        
        #going to the next input besed on the number of cards
        if grf.getCollisionStatus(nextButton, grf.getXToCenter(nextButton, w), 650, mouseDown):

            if len(communityCards) == 0:

                reveal3 = True
                firstTurn = False
            
            elif len(communityCards) == 3:

                fourthStreet = True
                reveal3 = False

            elif len(communityCards) == 4:

                fifthStreet = True
                fourthStreet = False

            elif len(communityCards) == 5:

                running = False

            viewHands = False

        
      
    pygame.display.flip()


    clock.tick(60)