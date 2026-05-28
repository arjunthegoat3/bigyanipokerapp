
import pygame
pygame.init()
import graphicsfunctions as grf

# =========================================================
# VARIABLES
# =========================================================

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
    "7", "8", "9", "10", "Jack",
    "Queen", "King"
]

allSuitValues = [
    "Spades", "Clovers", "Diamonds", "Hearts"
]

nddPlaceholder = "-"
sddPlaceholder = "-"

nddValue = None
sddValue = None

# =========================================================
# WINDOW
# =========================================================

w = pygame.display.set_mode((1100, 950))

clock = pygame.time.Clock()

bigFont = pygame.font.Font(
    "Oswald/Oswald-VariableFont_wght.ttf",
    55
)

font = pygame.font.Font(
    "Oswald/Oswald-VariableFont_wght.ttf",
    22
)

smallFont = pygame.font.Font(
    "Oswald/Oswald-VariableFont_wght.ttf",
    18
)

# =========================================================
# IMAGES
# =========================================================

texasPicture = pygame.image.load(
    "randomPicturesAndStuff/texas.jpg"
)

texasPicture = pygame.transform.scale(
    texasPicture,
    (400, 400)
)

beginButton = pygame.image.load(
    "randomPicturesAndStuff/beginButton.png"
)

beginButton = pygame.transform.scale(
    beginButton,
    (180, 90)
)

nextButton = pygame.image.load(
    "randomPicturesAndStuff/nextButton.png"
)

nextButton = pygame.transform.scale(
    nextButton,
    (180, 90)
)

# =========================================================
# CARD VALUES
# =========================================================

cardRanks = {
    "ACE": 14,
    "King": 13,
    "Queen": 12,
    "Jack": 11,
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
        ("ACE" in values and "King" in values)
        or ("ACE" in values and "Queen" in values)
        or ("King" in values and "Queen" in values)
    ):

        return "CALL"

    else:

        return "FOLD"

# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    mouseDown = False

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouseDown = True

    # BACKGROUND
    w.fill((240, 240, 240))

    # =====================================================
    # START SCREEN
    # =====================================================

    if start:

        titleFont = bigFont.render(
            "TEXAS HOLD EM HELPER",
            True,
            (0, 0, 0)
        )

        w.blit(
            titleFont,
            (grf.getXToCenter(titleFont, w), 60)
        )

        w.blit(
            texasPicture,
            (grf.getXToCenter(texasPicture, w), 180)
        )

        w.blit(
            beginButton,
            (grf.getXToCenter(beginButton, w), 700)
        )

        if grf.getCollisionStatus(
            beginButton,
            grf.getXToCenter(beginButton, w),
            700,
            mouseDown
        ):

            start = False
            handInput = True

    # =====================================================
    # HAND INPUT SCREEN
    # =====================================================

    if handInput:

        numberDrawDownX = 170
        suitDrawDownX = 700
        y = 130

        # TOP TITLE
        title = bigFont.render(
            "INPUT CARDS",
            True,
            (0, 0, 0)
        )

        w.blit(title, (350, 40))

        # DIVIDER
        pygame.draw.line(
            w,
            (0, 0, 0),
            (550, 100),
            (550, 850),
            3
        )

        # NEXT BUTTON
        w.blit(
            nextButton,
            (grf.getXToCenter(nextButton, w), 820)
        )

        # HEADERS
        cardHeader = font.render(
            "CARD VALUE",
            True,
            (0, 0, 0)
        )

        suitHeader = font.render(
            "CARD SUIT",
            True,
            (0, 0, 0)
        )

        w.blit(cardHeader, (190, 90))
        w.blit(suitHeader, (720, 90))

        # CURRENT INPUT
        if len(userHand) < 2:

            headerText = (
                "PLAYER CARD "
                + str(len(userHand) + 1)
                + " OF 2"
            )

        else:

            headerText = (
                "COMMUNITY CARD "
                + str(len(communityCards) + 1)
                + " OF 5"
            )

        header = font.render(
            headerText,
            True,
            (0, 0, 0)
        )

        w.blit(
            header,
            (grf.getXToCenter(header, w), 760)
        )

        # =================================================
        # VALUE DROPDOWN
        # =================================================

        if not numberDrawDownClicked:

            rect = pygame.Rect(
                numberDrawDownX,
                y,
                200,
                55
            )

            pygame.draw.rect(
                w,
                (220, 220, 220),
                rect,
                border_radius=10
            )

            valueText = font.render(
                nddPlaceholder,
                True,
                (0, 0, 0)
            )

            w.blit(
                valueText,
                (numberDrawDownX + 85, y + 12)
            )

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
                    y + (60 * (i + 1)),
                    200,
                    55
                )

                pygame.draw.rect(
                    w,
                    (200, 200, 200),
                    rect,
                    border_radius=10
                )

                text = smallFont.render(
                    allCardValues[i],
                    True,
                    (0, 0, 0)
                )

                w.blit(
                    text,
                    (
                        numberDrawDownX + 65,
                        y + 18 + (60 * (i + 1))
                    )
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

            rect = pygame.Rect(
                suitDrawDownX,
                y,
                200,
                55
            )

            pygame.draw.rect(
                w,
                (220, 220, 220),
                rect,
                border_radius=10
            )

            suitText = font.render(
                sddPlaceholder,
                True,
                (0, 0, 0)
            )

            w.blit(
                suitText,
                (suitDrawDownX + 70, y + 12)
            )

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
                    y + (60 * (i + 1)),
                    200,
                    55
                )

                pygame.draw.rect(
                    w,
                    (200, 200, 200),
                    rect,
                    border_radius=10
                )

                text = smallFont.render(
                    allSuitValues[i],
                    True,
                    (0, 0, 0)
                )

                w.blit(
                    text,
                    (
                        suitDrawDownX + 50,
                        y + 18 + (60 * (i + 1))
                    )
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
        # NEXT BUTTON
        # =================================================

        if grf.getCollisionStatus(
            nextButton,
            grf.getXToCenter(nextButton, w),
            820,
            mouseDown
        ):

            if nddValue != None and sddValue != None:

                card = (nddValue, sddValue)

                # PLAYER CARDS
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

                # RESET
                nddValue = None
                sddValue = None

                nddPlaceholder = "-"
                sddPlaceholder = "-"

                numberDrawDownClicked = False
                suitDrawDownClicked = False

                # FINISH
                if (
                    len(userHand) == 2
                    and len(communityCards) == 5
                ):

                    handInput = False
                    viewCards = True

    # =====================================================
    # RESULTS SCREEN
    # =====================================================

    if viewCards:

        header = bigFont.render(
            "POKER ANALYSIS",
            True,
            (0, 0, 0)
        )

        w.blit(
            header,
            (grf.getXToCenter(header, w), 40)
        )

        # DIVIDER
        pygame.draw.line(
            w,
            (0, 0, 0),
            (550, 120),
            (550, 800),
            3
        )

        # DECISION
        decision = getDecision(
            userHand,
            communityCards
        )

        if decision == "ALL IN":

            color = (150, 0, 200)

        elif decision == "RAISE":

            color = (0, 180, 0)

        elif decision == "CALL":

            color = (255, 165, 0)

        else:

            color = (220, 0, 0)

        decisionText = bigFont.render(
            decision,
            True,
            color
        )

        w.blit(
            decisionText,
            (grf.getXToCenter(decisionText, w), 760)
        )

        # PLAYER HAND
        playerHeader = font.render(
            "PLAYER HAND",
            True,
            (0, 0, 0)
        )

        w.blit(playerHeader, (170, 140))

        for i in range(len(userHand)):

            cardText = str(userHand[i])

            cardSurface = font.render(
                cardText,
                True,
                (0, 0, 0)
            )

            w.blit(
                cardSurface,
                (170, 190 + (i * 70))
            )

        # COMMUNITY
        communityHeader = font.render(
            "COMMUNITY CARDS",
            True,
            (0, 0, 0)
        )

        w.blit(communityHeader, (650, 140))

        for i in range(len(communityCards)):

            cardText = str(communityCards[i])

            cardSurface = font.render(
                cardText,
                True,
                (0, 0, 0)
            )

            w.blit(
                cardSurface,
                (650, 190 + (i * 70))
            )

    # =====================================================
    # UPDATE
    # =====================================================

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
```
