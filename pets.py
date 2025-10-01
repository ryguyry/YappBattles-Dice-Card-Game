# pets.py

class Pet:
    def __init__(self, name, species, breed):
        self.name = name
        self.species = species
        self.breed = breed
        self.health = 100
        self.stamina = 100

    def speak(self):
        print(f"{self.name} makes a sound.")

    def get_stats(self):
        return f"{self.name} the {self.breed} ({self.species}) — HP: {self.health}, ST: {self.stamina}"


class Dog(Pet):
    def __init__(self, name, breed):
        super().__init__(name, "Dog", breed)

    def speak(self):
        print(f"{self.name} says Woof!")


class Cat(Pet):
    def __init__(self, name, breed):
        super().__init__(name, "Cat", breed)

    def speak(self):
        print(f"{self.name} says Meow!")
