import random
from cards.attack_cards import load_attack_cards
from cards.healing_cards import load_healing_cards
from cards.support_cards import load_support_cards

def load_full_deck():
    deck = []
    deck.extend(load_attack_cards())
    deck.extend(load_healing_cards())
    deck.extend(load_support_cards())
    random.shuffle(deck)
    return deck
