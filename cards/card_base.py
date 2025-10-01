# cards/card_base.py
import pygame

class Card:
    def __init__(self, name, type_, image_path, description, text, cost, damage=0, heal=0, stamina=0, power=0):
        self.name = name
        self.type = type_
        self.image_path = image_path
        self.description = description
        self.text = text
        self.cost = cost
        self.damage = damage
        self.heal = heal
        self.stamina = stamina
        self.power = power

        self.image = pygame.image.load(image_path)

    def __repr__(self):
        return (f"<Card {self.name} ({self.type}) - Cost: {self.cost}, "
                f"Damage: {self.damage}, Heal: {self.heal}, "
                f"Stamina: {self.stamina}, Power: {self.power}>")
