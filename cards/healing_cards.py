# cards/healing_cards.py
from cards.card_base import Card

def load_healing_cards():
    return [
        Card(
            name="Quick Lick",
            type_="Heal",
            image_path="assets/images/cards/quick_lick.png",
            description="Restore 10 health.",
            text="A fast lick to patch small wounds.",
            cost=2,
            damage=0,
            heal=10,
            stamina=0,
            power=0
        ),
        Card(
            name="Gentle Rest",
            type_="Heal",
            image_path="assets/images/cards/gentle_rest.png",
            description="Restore 10 health.",
            text="Take a calm moment to recover.",
            cost=3,
            damage=0,
            heal=10,
            stamina=0,
            power=0
        ),
        Card(
            name="Nuzzle Nap",
            type_="Heal",
            image_path="assets/images/cards/nuzzle_nap.png",
            description="Restore 10 health.",
            text="A cozy nap next to your ally.",
            cost=3,
            damage=0,
            heal=10,
            stamina=0,
            power=0
        ),
        Card(
            name="Focused Breathing",
            type_="Heal",
            image_path="assets/images/cards/focused_breathing.png",
            description="Restore 20 health.",
            text="Center yourself for a burst of wellness.",
            cost=4,
            damage=0,
            heal=20,
            stamina=0,
            power=0
        ),
        Card(
            name="Rejuvenating Purr",
            type_="Heal",
            image_path="assets/images/cards/rejuvenating_purr.png",
            description="Restore 20 health.",
            text="The vibrations of a healing purr.",
            cost=4,
            damage=0,
            heal=20,
            stamina=0,
            power=0
        ),
        Card(
            name="Mega Lick",
            type_="Heal",
            image_path="assets/images/cards/mega_lick.png",
            description="Restore 25 health.",
            text="A mega dose of puppy love.",
            cost=4,
            damage=0,
            heal=25,
            stamina=0,
            power=0
        ),
        Card(
            name="Sacred Howl",
            type_="Heal",
            image_path="assets/images/cards/sacred_howl.png",
            description="Restore 30 health.",
            text="A call to the ancient spirits of healing.",
            cost=6,
            damage=0,
            heal=30,
            stamina=0,
            power=0
        ),
        Card(
            name="Healing Circle",
            type_="Heal",
            image_path="assets/images/cards/healing_circle.png",
            description="Restore 30 health.",
            text="All energies converge for deep healing.",
            cost=6,
            damage=0,
            heal=30,
            stamina=0,
            power=0
        ),
        Card(
            name="Last Hope",
            type_="Heal",
            image_path="assets/images/cards/last_hope.png",
            description="Restore 35 health.",
            text="One final surge of strength.",
            cost=6,
            damage=0,
            heal=35,
            stamina=0,
            power=0
        ),
    ]
