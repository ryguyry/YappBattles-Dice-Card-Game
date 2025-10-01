# cards/attack_cards.py
from cards.card_base import Card

def load_attack_cards():
    return [
        Card(
            name="Bite",
            type_="Attack",
            image_path="assets/images/cards/bite.png",
            description="A quick bite that deals 10 damage.",
            text="A fast and familiar pet move.",
            cost=2,
            damage=10
        ),
        Card(
            name="Scratch",
            type_="Attack",
            image_path="assets/images/cards/scratch.png",
            description="Claw at the enemy for 10 damage.",
            text="Sharp and swift.",
            cost=2,
            damage=10
        ),
        Card(
            name="Tail Whip",
            type_="Attack",
            image_path="assets/images/cards/tail_whip.png",
            description="A tail strike that deals 10 damage.",
            text="Surprisingly effective.",
            cost=2,
            damage=10
        ),
        Card(
            name="Nip",
            type_="Attack",
            image_path="assets/images/cards/nip.png",
            description="A small nip dealing 10 damage.",
            text="Doesn't look like much, but it hurts.",
            cost=1,
            damage=10
        ),
        Card(
            name="Paw Swipe",
            type_="Attack",
            image_path="assets/images/cards/paw_swipe.png",
            description="Swipe with paws for 5 damage.",
            text="Gentle but gets the job done.",
            cost=1,
            damage=5
        ),
        Card(
            name="Tail Flick",
            type_="Attack",
            image_path="assets/images/cards/tail_flick.png",
            description="A light flick dealing 5 damage.",
            text="Annoying and distracting.",
            cost=1,
            damage=5
        ),
        Card(
            name="Hard Bite",
            type_="Attack",
            image_path="assets/images/cards/hard_bite.png",
            description="A powerful bite that deals 15 damage.",
            text="Teeth sink deep!",
            cost=3,
            damage=15
        ),
        Card(
            name="Charge",
            type_="Attack",
            image_path="assets/images/cards/charge.png",
            description="Ram the enemy for 20 damage.",
            text="Builds up speed before impact.",
            cost=4,
            damage=20
        ),
        Card(
            name="Pounce",
            type_="Attack",
            image_path="assets/images/cards/pounce.png",
            description="Leap and strike for 25 damage.",
            text="Nothing is safe when you leap.",
            cost=4,
            damage=25
        ),
        Card(
            name="Savage Lunge",
            type_="Attack",
            image_path="assets/images/cards/savage_lunge.png",
            description="An all-out lunge that deals 30 damage.",
            text="Unleash full fury!",
            cost=5,
            damage=30
        ),
    ]
