from collections import Counter
from enum import Enum
from operator import itemgetter
from typing import Callable


class HandType(list, Enum):
    FIVE = [5]
    FOUR = [4, 1]
    FULL_HOUSE = [3, 2]
    THREE = [3, 1, 1]
    TWO_PAIRS = [2, 2, 1]
    ONE_PAIR = [2, 1, 1, 1]
    HIGH_CARD = [1, 1, 1, 1, 1]

    @staticmethod
    def cards_to_type(cards: str):
        counter = Counter(cards)
        # Construction of HandType works because lists of numbers is nicely ordered
        return HandType(sorted(counter.values(), reverse=True))


hand_type_order = list(reversed([HandType.FIVE, HandType.FOUR, HandType.FULL_HOUSE, HandType.THREE, HandType.TWO_PAIRS,
                                 HandType.ONE_PAIR, HandType.HIGH_CARD]))

CardOrder = list[str]
# The increasing order of cards for Part One
standard_card_order = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
# The increasing order of cards for Part Two
joker_card_order = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
Hand = tuple[HandType, str, int]


def build_sort_key(card_order: CardOrder) -> Callable[[Hand], int]:
    """Creates a key-function used for sorting list of Hands, based on hand type and hand cards"""

    def sort_key(hand: Hand) -> int:
        hand_type, hand_cards, _ = hand
        # Convert each card to its ordering number
        indexed_hand_cards = list(map(lambda card: card_order.index(card), hand_cards))
        # Do the same, but for the hand type
        index_hand_type = hand_type_order.index(hand_type)
        # Treat the hand type order number and cards ordering numbers as one big number (key)
        indexed_elements = [index_hand_type, *indexed_hand_cards]
        # But watch out! In fact, we are in the 13-base system because we have 13 cards (not a decimal one!)
        # Construct a key number: order(hand_type) * 13^5 + order(cards[0]) * 13^4 + ... + order(cards[4]) * 13^0
        return sum(map(lambda t: t[0] * (13 ** t[1]), zip(indexed_elements, range(len(indexed_elements) - 1, -1, -1))))

    return sort_key


def parse_hand(hand_info: str) -> Hand:
    """Read cards and corresponding bid of each hand"""
    cards, bid = hand_info.strip().split()
    return HandType.cards_to_type(cards), cards, int(bid)


def convert_cards_with_jokers(hand: Hand) -> Hand:
    """Convert hand type considering all Jokers in cards"""
    hand_type, cards, bid = hand
    # No jokers means no changes; Five jokers is already the best hand type (the Five!)
    if "J" not in cards or cards == "JJJJJ":
        return hand
    counter = Counter(cards)
    counter.pop("J")
    highest_card = counter.most_common(1)[0][0]
    # Substitute joker for the highest card
    new_cards = cards.replace("J", highest_card)
    # Remember to return the old cards with jokers, as these are used for breaking ties
    return HandType.cards_to_type(new_cards), cards, bid


def count_total_winnings(hands: list[Hand]) -> int:
    return sum(map(lambda t: t[0] * t[1],  # Multiply rank * bid
                   enumerate(  # Rank them
                       map(itemgetter(2),  # Get bids
                           hands), start=1)))


with open("input") as f:
    hands = list(map(parse_hand, f.readlines()))
    print("----- Part one -----")
    new_hands = sorted(hands, key=build_sort_key(standard_card_order))
    print(f"Total winnings: {count_total_winnings(new_hands)}")
    print("----- Part two -----")
    new_hands = sorted(map(convert_cards_with_jokers, hands), key=build_sort_key(joker_card_order))
    print(f"Total winnings: {count_total_winnings(new_hands)}")
