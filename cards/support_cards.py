# cards/support_cards.py
from cards.card_base import Card

def load_support_cards():
    return [
        # Stamina gain
        Card(
            name="Stretch",
            type_="Support",
            image_path="assets/images/cards/stretch.png",
            description="Gain 1 stamina.",
            text="Loosen up those legs.",
            cost=0,
            damage=0,
            heal=0,
            stamina=1,
            power=0
        ),
        Card(
            name="Quick Breath",
            type_="Support",
            image_path="assets/images/cards/quick_breath.png",
            description="Gain 1 stamina.",
            text="Catch your breath quickly.",
            cost=0,
            damage=0,
            heal=0,
            stamina=1,
            power=0
        ),
        Card(
            name="Deep Breathing",
            type_="Support",
            image_path="assets/images/cards/deep_breathing.png",
            description="Gain 2 stamina.",
            text="Relax... and recharge.",
            cost=0,
            damage=0,
            heal=0,
            stamina=2,
            power=0
        ),
        # Power to max (assumed capped elsewhere)
        Card(
            name="Energize",
            type_="Support",
            image_path="assets/images/cards/energize.png",
            description="Gain 6 power.",
            text="Supercharge your next turn.",
            cost=0,
            damage=0,
            heal=0,
            stamina=0,
            power=6
        ),
        Card(
            name="Hype Up",
            type_="Support",
            image_path="assets/images/cards/hype_up.png",
            description="Gain 6 power.",
            text="Get amped for action!",
            cost=0,
            damage=0,
            heal=0,
            stamina=0,
            power=6
        ),
        Card(
            name="Full Focus",
            type_="Support",
            image_path="assets/images/cards/full_focus.png",
            description="Gain 6 power.",
            text="Eyes locked, spirit ready.",
            cost=0,
            damage=0,
            heal=0,
            stamina=0,
            power=6
        ),
        # Reduce opponent power
        Card(
            name="Intimidate",
            type_="Support",
            image_path="assets/images/cards/intimidate.png",
            description="Reduce opponent's power by 1.",
            text="A fierce glare breaks their focus.",
            cost=0,
            damage=0,
            heal=0,
            stamina=0,
            power=-1
        ),
        Card(
            name="Taunt",
            type_="Support",
            image_path="assets/images/cards/taunt.png",
            description="Reduce opponent's power by 1.",
            text="Get under their fur.",
            cost=0,
            damage=0,
            heal=0,
            stamina=0,
            power=-1
        ),
        Card(
            name="Sneer",
            type_="Support",
            image_path="assets/images/cards/sneer.png",
            description="Reduce opponent's power by 1.",
            text="Rattle them with one look.",
            cost=0,
            damage=0,
            heal=0,
            stamina=0,
            power=-1
        ),
        Card(
            name="Power Drain",
            type_="Support",
            image_path="assets/images/cards/power_drain.png",
            description="Reduce opponent's power by 1.",
            text="Absorb a little energy.",
            cost=0,
            damage=0,
            heal=0,
            stamina=0,
            power=-1
        ),
        Card(
            name="Energy Leech",
            type_="Support",
            image_path="assets/images/cards/energy_leech.png",
            description="Reduce opponent's power by 2.",
            text="Draw strength from their weakness.",
            cost=1,
            damage=0,
            heal=0,
            stamina=0,
            power=-2
        ),
        Card(
            name="Power Sap",
            type_="Support",
            image_path="assets/images/cards/power_sap.png",
            description="Reduce opponent's power by 2.",
            text="Dampen their energy.",
            cost=1,
            damage=0,
            heal=0,
            stamina=0,
            power=-2
        ),
        Card(
            name="Overwhelm",
            type_="Support",
            image_path="assets/images/cards/overwhelm.png",
            description="Reduce opponent's power by 3.",
            text="Push them to their limit.",
            cost=2,
            damage=0,
            heal=0,
            stamina=0,
            power=-3
        ),
        Card(
            name="Nullify",
            type_="Support",
            image_path="assets/images/cards/nullify.png",
            description="Reduce opponent's power to 0.",
            text="Drain them completely.",
            cost=6,
            damage=0,
            heal=0,
            stamina=0,
            power=-99  # Special case - should clamp to 0
        ),
    ]
