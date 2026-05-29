import pygame
import itertools
pygame.init()


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


# replaces grf.getXToCenter
def getXToCenter(surface):
    return (w.get_width() - surface.get_width()) // 2

# replaces grf.getCollisionStatus
def getCollisionStatus(surface, x, y, mouseDown, ignoreY=False):

    if not mouseDown:
        return False

    mx, my = pygame.mouse.get_pos()

    # pygame.Rect object
    if isinstance(surface, pygame.Rect):

        return surface.collidepoint(mx, my)

    # image / surface object
    rect = pygame.Rect(
        x,
        y,
        surface.get_width(),
        surface.get_height()
    )

    return rect.collidepoint(mx, my)

# ── Hand evaluation ───────────────────────────────────────────────────────────
VALUE_MAP = {
    "2":2,"3":3,"4":4,"5":5,"6":6,"7":7,
    "8":8,"9":9,"10":10,"J":11,"Q":12,"K":13,"A":14
}
HAND_RANKS = {
    "ROYAL FLUSH":10,"STRAIGHT FLUSH":9,"FOUR OF A KIND":8,
    "FULL HOUSE":7,"FLUSH":6,"STRAIGHT":5,
    "THREE OF A KIND":4,"TWO PAIR":3,"PAIR":2,"HIGH CARD":1
}

def evaluate5(cards):
    suits  = [c[0] for c in cards]
    values = [VALUE_MAP[c[1:]] for c in cards]
    counts = {v: values.count(v) for v in set(values)}
    flush  = len(set(suits)) == 1
    straight = False
    straight_high = 0
    sv = sorted(set(values))
    cv = ([1] + sv) if 14 in sv else sv
    for i in range(len(cv) - 4):
        win = cv[i:i+5]
        if win[-1] - win[0] == 4 and len(set(win)) == 5:
            straight = True
            straight_high = win[-1]
    pairs = [v for v,c in counts.items() if c == 2]
    trips = [v for v,c in counts.items() if c == 3]
    quads = [v for v,c in counts.items() if c >= 4]
    if flush and straight:
        return "ROYAL FLUSH" if straight_high == 14 else "STRAIGHT FLUSH"
    if quads:           return "FOUR OF A KIND"
    if trips and pairs: return "FULL HOUSE"
    if flush:           return "FLUSH"
    if straight:        return "STRAIGHT"
    if trips:           return "THREE OF A KIND"
    if len(pairs) >= 2: return "TWO PAIR"
    if len(pairs) == 1: return "PAIR"
    return "HIGH CARD"

def evaluateHand(cards):
    if len(cards) < 2:
        return "NOT ENOUGH CARDS"
    if len(cards) < 5:
        values = [VALUE_MAP[c[1:]] for c in cards]
        counts = {v: values.count(v) for v in set(values)}
        pairs = [v for v,c in counts.items() if c == 2]
        trips = [v for v,c in counts.items() if c == 3]
        quads = [v for v,c in counts.items() if c >= 4]
        if quads:           return "FOUR OF A KIND"
        if trips and pairs: return "FULL HOUSE"
        if trips:           return "THREE OF A KIND"
        if len(pairs) >= 2: return "TWO PAIR"
        if pairs:           return "PAIR"
        return "HIGH CARD"
    best = "HIGH CARD"
    for combo in itertools.combinations(cards, 5):
        result = evaluate5(list(combo))
        if HAND_RANKS[result] > HAND_RANKS[best]:
            best = result
    return best

def getAdvice(handName, stage):
    if handName == "ROYAL FLUSH":     return "ALL IN - Unbeatable hand!"
    if handName == "STRAIGHT FLUSH":  return "ALL IN - Near unbeatable!"
    if handName == "FOUR OF A KIND":  return "ALL IN - Four of a kind wins almost always."
    if handName == "FULL HOUSE":      return "RAISE - Full house is a dominant hand."
    if handName == "FLUSH":           return "RAISE - Flush is very strong."
    if handName == "STRAIGHT":        return "RAISE - Straight is a strong hand."
    if handName == "THREE OF A KIND": return "RAISE - Three of a kind, apply pressure."
    if handName == "TWO PAIR":
        return "RAISE - Two pair, protect your hand." if stage <= 1 else "CALL - Two pair, watch for better hands."
    if handName == "PAIR":
        if stage == 0: return "CALL - Pocket pair, see the flop."
        if stage == 1: return "CHECK / CALL - One pair, only call small bets."
        return "FOLD - One pair this late is weak."
    if handName == "HIGH CARD":
        return "CALL - Only if you have Ace, King, or Queen." if stage == 0 else "FOLD - High card only, not worth continuing."
    return "CHECK - Unclear situation."
# ── End hand evaluation ───────────────────────────────────────────────────────


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

    w.blit(nextButton, (getXToCenter(nextButton), 650))
    w.blit(font.render("CARD #", True, (0, 0, 0)), (numberDrawDownX + 30, 90))
    w.blit(font.render("SUIT", True, (0, 0, 0)), (suitDrawDownX + 30, 90))
    header = font.render("Input Cards - Card # " + str(len(cardList) + 1) + " of " + str(cardNumber), True, (0, 0, 0))
    w.blit(header, (getXToCenter(header), 50))

    if not numberDrawDownClicked:

        rect = pygame.Rect(numberDrawDownX, (drawDownY + 50), 100, 50)
        pygame.draw.rect(w, (220, 220, 220), rect)
        w.blit(font.render(nddPlaceholder, True, (0, 0, 0)), ((numberDrawDownX + 45), (drawDownY + 60)))

        if getCollisionStatus(rect, numberDrawDownX, drawDownY, mouseDown, True):
            mouseDown = False
            numberDrawDownClicked = True

    else:

        for i in range(0, len(allCardValues)):
            w.blit(font.render(nddPlaceholder, True, (0, 0, 0)), ((numberDrawDownX + 45), (drawDownY + 60)))
            rect = pygame.Rect(numberDrawDownX, (drawDownY + (50*(i + 1))), 100, 50)
            pygame.draw.rect(w, (200, 200, 200), rect)
            w.blit(font.render(allCardValues[i], True, (0, 0, 0)), ((numberDrawDownX + 45), (drawDownY + 10 + (50*(i + 1)))))

            if getCollisionStatus(rect, rect.x, drawDownY, mouseDown, True):
                nddValue = allCardValues[i]
                nddPlaceholder = allCardValues[i]
                numberDrawDownClicked = False
                pygame.time.wait(100)

    if not suitDrawDownClicked:

        rect = pygame.Rect(suitDrawDownX, (drawDownY + 50), 100, 50)
        pygame.draw.rect(w, (220, 220, 220), rect)
        w.blit(font.render(sddPlaceholder, True, (0, 0, 0)), ((suitDrawDownX + 45), (drawDownY + 60)))

        if getCollisionStatus(rect, suitDrawDownX, drawDownY, mouseDown, True):
            mouseDown = False
            suitDrawDownClicked = True

    else:

        for i in range(0, len(allSuitValues)):
            rect = pygame.Rect(suitDrawDownX, (drawDownY + (50*(i + 1))), 100, 50)
            pygame.draw.rect(w, (200, 200, 200), rect)
            w.blit(font.render(allSuitValues[i], True, (0, 0, 0)), ((suitDrawDownX + 45), (drawDownY + 10 + (50*(i + 1)))))

            if getCollisionStatus(rect, rect.x, drawDownY, mouseDown, True):
                sddValue = allSuitValues[i]
                sddPlaceholder = allSuitValues[i]
                suitDrawDownClicked = False
                pygame.time.wait(100)

    if getCollisionStatus(nextButton, getXToCenter(nextButton), 650, mouseDown) and sddPlaceholder != "-" and nddPlaceholder != "-":
        cardList.append(sddValue + nddValue)
        nddValue = None
        sddValue = None
        nddPlaceholder = "-"
        sddPlaceholder = "-"
        numberDrawDownClicked = False
        suitDrawDownClicked = False
        mouseDown = False

    return cardList



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

        titleFont = bigFont.render("TEXAS HOLD EM APP", True, (0, 0, 0))
        w.blit(titleFont, (getXToCenter(titleFont), 100))
        w.blit(texasPicture, (getXToCenter(texasPicture), 220))
        w.blit(beginButton, (getXToCenter(beginButton), 650))

        if getCollisionStatus(beginButton, getXToCenter(beginButton), 650, mouseDown):
            handInput = True
            start = False

    if handInput:

        try:
            if len(userHand) >= 2:
                viewHands = True
                handInput = False
                pygame.time.wait(150)
        except:
            None

        userHand = cardInputtingDropDowns(userHand, 2)

    if reveal3:

        try:
            if len(communityCards) >= 3:
                viewHands = True
                reveal3 = False
        except:
            None

        communityCards = cardInputtingDropDowns(communityCards, 3)

    if viewHands:

        header = bigFont.render("AVAILABLE CARDS", True, (0, 0, 0))
        w.blit(header, (getXToCenter(header), 60))

        w.blit(nextButton, (getXToCenter(nextButton), 650))

        for i in range(0, len(userHand)):
            w.blit(mediumFont.render("YOUR HAND", True, (0, 0, 0)), (30, 200))
            text = font.render(userHand[i], True, (0, 0, 0))
            w.blit(text, (85, 240 + (i*30)))

        if len(communityCards) > 0:
            for i in range(0, len(communityCards)):
                w.blit(mediumFont.render("COMMUNITY CARDS", True, (0, 0, 0)), (570, 200))
                text = font.render(communityCards[i], True, (0, 0, 0))
                w.blit(text, (675, 240 + (i*30)))

        # ── hand name + advice (new) ──
        if len(communityCards) == 0:   currentStage = 0
        elif len(communityCards) <= 3: currentStage = 1
        elif len(communityCards) == 4: currentStage = 2
        else:                          currentStage = 3

        handName = evaluateHand(userHand + communityCards)
        advice   = getAdvice(handName, currentStage)
        w.blit(font.render("HAND:   " + handName, True, (0, 0, 0)), (30, 380))
        w.blit(font.render("ADVICE: " + advice,   True, (0, 0, 0)), (30, 400))
        # ── end new ──────────────────

        if getCollisionStatus(nextButton, getXToCenter(nextButton), 650, mouseDown):

            if firstTurn:
                reveal3 = True
                firstTurn = False

            elif reveal3:
                fourthStreet = True
                reveal3 = False

            elif fourthStreet:
                fifthStreet = True
                fourthStreet = False

            viewHands = False

    pygame.display.flip()
    clock.tick(60)