import pygame
pygame.init()
import graphicsfunctions as grf
import pokeradvisor as advisor


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
smallFont = pygame.font.Font("Oswald/Oswald-VariableFont_wght.ttf", 18)
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

        rect = pygame.Rect(numberDrawDownX, (drawDownY + 50), 100, 50)
        pygame.draw.rect(w, (220, 220, 220), rect)
        w.blit(font.render(nddPlaceholder, True, (0, 0, 0)), ((numberDrawDownX + 45), (drawDownY + 60)))

        if grf.getCollisionStatus(rect, numberDrawDownX, drawDownY, mouseDown, True):
            mouseDown = False
            numberDrawDownClicked = True

    else:

        for i in range(0, len(allCardValues)):
            w.blit(font.render(nddPlaceholder, True, (0, 0, 0)), ((numberDrawDownX + 45), (drawDownY + 60)))
            rect = pygame.Rect(numberDrawDownX, (drawDownY + (50*(i + 1))), 100, 50)
            pygame.draw.rect(w, (200, 200, 200), rect)
            w.blit(font.render(allCardValues[i], True, (0, 0, 0)), ((numberDrawDownX + 45), (drawDownY + 10 + (50*(i + 1)))))

            if grf.getCollisionStatus(rect, rect.x, drawDownY, mouseDown, True):
                nddValue = allCardValues[i]
                nddPlaceholder = allCardValues[i]
                numberDrawDownClicked = False
                pygame.time.wait(100)

    if not suitDrawDownClicked:

        rect = pygame.Rect(suitDrawDownX, (drawDownY + 50), 100, 50)
        pygame.draw.rect(w, (220, 220, 220), rect)
        w.blit(font.render(sddPlaceholder, True, (0, 0, 0)), ((suitDrawDownX + 45), (drawDownY + 60)))

        if grf.getCollisionStatus(rect, suitDrawDownX, drawDownY, mouseDown, True):
            mouseDown = False
            suitDrawDownClicked = True

    else:

        for i in range(0, len(allSuitValues)):
            rect = pygame.Rect(suitDrawDownX, (drawDownY + (50*(i + 1))), 100, 50)
            pygame.draw.rect(w, (200, 200, 200), rect)
            w.blit(font.render(allSuitValues[i], True, (0, 0, 0)), ((suitDrawDownX + 45), (drawDownY + 10 + (50*(i + 1)))))

            if grf.getCollisionStatus(rect, rect.x, drawDownY, mouseDown, True):
                sddValue = allSuitValues[i]
                sddPlaceholder = allSuitValues[i]
                suitDrawDownClicked = False
                pygame.time.wait(100)

    if grf.getCollisionStatus(nextButton, grf.getXToCenter(nextButton, w), 650, mouseDown) and sddPlaceholder != "-" and nddPlaceholder != "-":

        cardList.append(sddValue + nddValue)
        inputtedCounter += 1

        nddValue = None
        sddValue = None
        nddPlaceholder = "-"
        sddPlaceholder = "-"
        numberDrawDownClicked = False
        suitDrawDownClicked = False
        mouseDown = False

    return cardList


def draw_advisor_panel(user_hand, community_cards):
    """
    Draws the advisor box in the centre of the viewHands screen.
    Occupies roughly x=220..580, y=330..620.
    """
    if len(user_hand) < 2:
        return

    advice = advisor.get_advice(user_hand, community_cards)

    panel_rect = pygame.Rect(210, 330, 380, 280)

    # Shadow
    shadow = pygame.Rect(panel_rect.x + 4, panel_rect.y + 4, panel_rect.w, panel_rect.h)
    pygame.draw.rect(w, (180, 180, 180), shadow, border_radius=12)

    # Panel background
    pygame.draw.rect(w, (30, 30, 40), panel_rect, border_radius=12)
    pygame.draw.rect(w, (100, 100, 120), panel_rect, width=2, border_radius=12)

    # ── Hand name ────────────────────────────────────────────────────────
    strength_color = advisor.get_strength_color(advice["strength"])
    hand_surf = mediumFont.render(advice["hand_name"], True, strength_color)
    w.blit(hand_surf, (panel_rect.centerx - hand_surf.get_width() // 2, panel_rect.y + 14))

    # ── Strength label ───────────────────────────────────────────────────
    strength_surf = smallFont.render("Strength: " + advice["strength"], True, strength_color)
    w.blit(strength_surf, (panel_rect.centerx - strength_surf.get_width() // 2, panel_rect.y + 52))

    # ── Divider ──────────────────────────────────────────────────────────
    pygame.draw.line(w, (100, 100, 120),
                     (panel_rect.x + 20, panel_rect.y + 78),
                     (panel_rect.right - 20, panel_rect.y + 78), 1)

    # ── Action recommendation ─────────────────────────────────────────────
    action_color = advisor.get_action_color(advice["action"])
    action_bg    = pygame.Rect(panel_rect.x + 30, panel_rect.y + 90, panel_rect.w - 60, 46)
    pygame.draw.rect(w, action_color, action_bg, border_radius=8)
    action_surf = mediumFont.render(advice["action"], True, (255, 255, 255))
    w.blit(action_surf, (action_bg.centerx - action_surf.get_width() // 2,
                          action_bg.centery - action_surf.get_height() // 2))

    # ── Reason (word-wrapped manually) ───────────────────────────────────
    reason = advice["reason"]
    words  = reason.split()
    lines  = []
    line   = ""
    for word in words:
        test = (line + " " + word).strip()
        if font.size(test)[0] <= panel_rect.w - 40:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)

    y_off = panel_rect.y + 150
    for ln in lines:
        surf = font.render(ln, True, (210, 210, 210))
        w.blit(surf, (panel_rect.centerx - surf.get_width() // 2, y_off))
        y_off += 22

    # ── Best cards used ──────────────────────────────────────────────────
    if len(community_cards) >= 3 and advice["best_cards"]:
        cards_label = font.render("Best hand: " + "  ".join(advice["best_cards"]), True, (160, 160, 200))
        w.blit(cards_label, (panel_rect.centerx - cards_label.get_width() // 2, panel_rect.bottom - 30))


# ── Main loop ─────────────────────────────────────────────────────────────────

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
        w.blit(titleFont, (grf.getXToCenter(titleFont, w), 100))
        w.blit(texasPicture, ((grf.getXToCenter(texasPicture, w)), 220))
        w.blit(beginButton, (grf.getXToCenter(beginButton, w), 650))

        if grf.getCollisionStatus(beginButton, grf.getXToCenter(beginButton, w), 650, mouseDown):
            handInput = True
            start = False

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

        header = bigFont.render("AVAILABLE CARDS", True, (0, 0, 0))
        w.blit(header, (grf.getXToCenter(header, w), 60))

        w.blit(nextButton, (grf.getXToCenter(nextButton, w), 700))

        # ── Your hand (left column) ───────────────────────────────────────
        for i in range(0, len(userHand)):
            w.blit(mediumFont.render("YOUR HAND", True, (0, 0, 0)), (30, 200))
            text = font.render(userHand[i], True, (0, 0, 0))
            w.blit(text, (85, 240 + (i * 30)))

        # ── Community cards (right column) ────────────────────────────────
        if len(communityCards) > 0:
            for i in range(0, len(communityCards)):
                w.blit(mediumFont.render("COMMUNITY", True, (0, 0, 0)), (580, 200))
                w.blit(mediumFont.render("CARDS", True, (0, 0, 0)), (610, 230))
                text = font.render(communityCards[i], True, (0, 0, 0))
                w.blit(text, (640, 270 + (i * 30)))

        # ── Advisor panel (centre) ────────────────────────────────────────
        draw_advisor_panel(userHand, communityCards)

        # ── Next button logic (unchanged) ─────────────────────────────────
        if grf.getCollisionStatus(nextButton, grf.getXToCenter(nextButton, w), 700, mouseDown):

            if len(communityCards) == 0:
                reveal3 = True
                firstTurn = False

            elif len(communityCards) == 3:
                fourthStreet = True
                reveal3 = False

            elif len(communityCards) == 4:
                fifthStreet = True
                fourthStreet = False

            viewHands = False

    pygame.display.flip()
    clock.tick(60)
