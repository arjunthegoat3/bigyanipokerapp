"""
pokeradvisor.py
Hand evaluator and strategy advisor for Texas Hold 'Em.

Cards are stored as strings like "SA" (Ace of Spades), "H10", "DK", etc.
Format: <Suit><Value>  e.g. S=Spades, C=Clubs, D=Diamonds, H=Hearts
Values: A 2 3 4 5 6 7 8 9 10 J Q K
"""

from itertools import combinations

# ── helpers ──────────────────────────────────────────────────────────────────

VALUE_ORDER = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
               "8": 8, "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

HAND_RANK_NAMES = {
    9: "ROYAL FLUSH",
    8: "STRAIGHT FLUSH",
    7: "FOUR OF A KIND",
    6: "FULL HOUSE",
    5: "FLUSH",
    4: "STRAIGHT",
    3: "THREE OF A KIND",
    2: "TWO PAIR",
    1: "ONE PAIR",
    0: "HIGH CARD",
}

def parse_card(card_str):
    """
    Parse a card string like 'SA', 'H10', 'DK'.
    Returns (suit, value_str, numeric_value).
    """
    suit = card_str[0]
    value = card_str[1:]
    return suit, value, VALUE_ORDER.get(value, 0)


def _rank_five(five_cards):
    """
    Given exactly 5 card strings, return an integer rank (0-9) and a
    tiebreaker tuple so hands can be compared with > / <.
    """
    parsed   = [parse_card(c) for c in five_cards]
    suits    = [p[0] for p in parsed]
    values   = sorted([p[2] for p in parsed], reverse=True)
    val_strs = [p[1] for p in parsed]

    is_flush    = len(set(suits)) == 1
    is_straight = (values == list(range(values[0], values[0] - 5, -1)))
    # Special case: A-2-3-4-5 wheel straight
    if set(values) == {14, 2, 3, 4, 5}:
        is_straight = True
        values = [5, 4, 3, 2, 1]          # treat Ace as low

    from collections import Counter
    counts = Counter(val_strs)
    freq   = sorted(counts.values(), reverse=True)   # e.g. [2,2,1] for two pair
    groups = sorted(counts.keys(), key=lambda v: (counts[v], VALUE_ORDER[v]), reverse=True)

    # Tiebreaker: order cards by group size then value
    tb = tuple(VALUE_ORDER[v] for v in groups)

    if is_straight and is_flush:
        if values[0] == 14 and not (set(values) == {14,2,3,4,5}):
            return 9, tb          # Royal flush
        return 8, tuple(values)   # Straight flush

    if freq == [4, 1]:  return 7, tb
    if freq == [3, 2]:  return 6, tb
    if is_flush:        return 5, tuple(values)
    if is_straight:     return 4, tuple(values)
    if freq[0] == 3:    return 3, tb
    if freq == [2, 2, 1]: return 2, tb
    if freq[0] == 2:    return 1, tb
    return 0, tuple(values)


def best_hand(cards):
    """
    Given 2–7 card strings, find the best 5-card combination.
    Returns (rank_int, rank_name, best_5_cards).
    """
    if len(cards) < 5:
        # Can't make a full 5-card hand yet — evaluate what we have
        rank, tb = _rank_partial(cards)
        return rank, HAND_RANK_NAMES.get(rank, "HIGH CARD"), list(cards)

    best_rank = -1
    best_tb   = ()
    best_five = []

    for combo in combinations(cards, 5):
        rank, tb = _rank_five(list(combo))
        if (rank, tb) > (best_rank, best_tb):
            best_rank = rank
            best_tb   = tb
            best_five = list(combo)

    return best_rank, HAND_RANK_NAMES[best_rank], best_five


def _rank_partial(cards):
    """Rough rank when fewer than 5 cards are available."""
    from collections import Counter
    parsed = [parse_card(c) for c in cards]
    vals   = [p[1] for p in parsed]
    suits  = [p[0] for p in parsed]
    counts = Counter(vals)
    freq   = sorted(counts.values(), reverse=True)
    groups = sorted(counts.keys(), key=lambda v: (counts[v], VALUE_ORDER[v]), reverse=True)
    tb     = tuple(VALUE_ORDER[v] for v in groups)

    if freq[0] == 4: return 7, tb
    if freq[0] == 3: return 3, tb
    if freq == [2, 2]:  return 2, tb
    if freq[0] == 2:    return 1, tb

    # Flush / straight potential when only 2 cards
    if len(set(suits)) == 1: return 5, tb   # suited (counts as flush potential)
    return 0, tb


# ── advisor ──────────────────────────────────────────────────────────────────

def _hole_card_strength(hand):
    """
    Pre-flop hole-card strength score 0–10.
    Used when no community cards are available yet.
    """
    if len(hand) < 2:
        return 5

    p1 = parse_card(hand[0])
    p2 = parse_card(hand[1])
    v1, v2 = p1[2], p2[2]
    suited  = p1[0] == p2[0]
    paired  = p1[1] == p2[1]
    gap     = abs(v1 - v2)
    high    = max(v1, v2)

    score = 0

    # Pocket pairs
    if paired:
        if high >= 10: score = 10       # TT+
        elif high >= 7: score = 8       # 77-99
        else:          score = 6       # 22-66

    else:
        # High card bonus
        score += min(high - 6, 4)      # up to +4 for A-high

        # Low card bonus
        low = min(v1, v2)
        score += max(0, low - 8)       # +1 for 9, +2 for T, etc.

        # Suitedness bonus
        if suited:   score += 2

        # Connectivity bonus (lower gap = better)
        score += max(0, 3 - gap)

    return min(score, 10)


def get_advice(user_hand, community_cards):
    """
    Main advisor function.

    Parameters
    ----------
    user_hand       : list of card strings, e.g. ["SA", "HK"]
    community_cards : list of card strings (0, 3, 4, or 5 cards)

    Returns
    -------
    dict with keys:
        hand_name   – e.g. "FLUSH"
        best_cards  – the 5 best cards
        action      – "FOLD" | "CHECK/CALL" | "RAISE" | "GO ALL-IN"
        reason      – plain-English explanation
        rank        – integer 0-9
        strength    – "Weak" | "Moderate" | "Strong" | "Monster"
    """
    all_cards = list(user_hand) + list(community_cards)
    rank, hand_name, best_five = best_hand(all_cards)

    street = len(community_cards)   # 0=preflop, 3=flop, 4=turn, 5=river

    # ── Determine action ──────────────────────────────────────────────────
    if street == 0:
        # Pre-flop: use hole card heuristic
        score = _hole_card_strength(user_hand)

        if score >= 9:
            action = "GO ALL-IN"
            reason = "Premium hole cards — dominate the table pre-flop."
            strength = "Monster"
        elif score >= 7:
            action = "RAISE"
            reason = "Strong hole cards — build the pot and apply pressure."
            strength = "Strong"
        elif score >= 4:
            action = "CHECK/CALL"
            reason = "Playable hand — see the flop before committing chips."
            strength = "Moderate"
        else:
            action = "FOLD"
            reason = "Weak hole cards — save your chips for a better spot."
            strength = "Weak"

    else:
        # Post-flop: use actual hand rank
        if rank == 9:
            action = "GO ALL-IN"
            reason = "You have a Royal Flush — the absolute best hand possible!"
            strength = "Monster"
        elif rank == 8:
            action = "GO ALL-IN"
            reason = "Straight Flush — nearly unbeatable. Max value."
            strength = "Monster"
        elif rank == 7:
            action = "GO ALL-IN"
            reason = "Four of a Kind — an almost certain winner."
            strength = "Monster"
        elif rank == 6:
            if street < 5:
                action = "RAISE"
                reason = "Full House is a monster hand. Raise to build the pot."
            else:
                action = "GO ALL-IN"
                reason = "Full House on the river — the board is set. All-in."
            strength = "Monster"
        elif rank == 5:
            action = "RAISE"
            reason = "Flush — a powerful hand. Apply pressure with a raise."
            strength = "Strong"
        elif rank == 4:
            action = "RAISE"
            reason = "Straight — strong made hand. Raise to get value."
            strength = "Strong"
        elif rank == 3:
            action = "RAISE"
            reason = "Three of a Kind — solid hand, raise to thin the field."
            strength = "Strong"
        elif rank == 2:
            action = "CHECK/CALL"
            reason = "Two Pair — decent hand, but be cautious of stronger draws."
            strength = "Moderate"
        elif rank == 1:
            # Pair — depends on which street
            if street == 5:
                action = "CHECK/CALL"
                reason = "One Pair on the river — marginal. Avoid big raises."
            else:
                action = "CHECK/CALL"
                reason = "One Pair — playable, but wait for improvement."
            strength = "Moderate"
        else:
            # High card
            if street == 5:
                action = "FOLD"
                reason = "High card only on the river — very likely beaten."
            elif street >= 3:
                action = "FOLD"
                reason = "No made hand yet on the flop/turn. Fold unless drawing cheap."
            else:
                action = "FOLD"
                reason = "Nothing yet — consider folding."
            strength = "Weak"

    return {
        "hand_name":  hand_name,
        "best_cards": best_five,
        "action":     action,
        "reason":     reason,
        "rank":       rank,
        "strength":   strength,
    }


# ── Colour helper for pygame ──────────────────────────────────────────────────

ACTION_COLORS = {
    "FOLD":        (200, 60,  60),    # Red
    "CHECK/CALL":  (60,  140, 200),   # Blue
    "RAISE":       (60,  180, 80),    # Green
    "GO ALL-IN":   (220, 160, 0),     # Gold
}

STRENGTH_COLORS = {
    "Weak":     (200, 60,  60),
    "Moderate": (200, 160, 40),
    "Strong":   (60,  180, 80),
    "Monster":  (180, 60,  220),
}

def get_action_color(action):
    return ACTION_COLORS.get(action, (180, 180, 180))

def get_strength_color(strength):
    return STRENGTH_COLORS.get(strength, (180, 180, 180))
