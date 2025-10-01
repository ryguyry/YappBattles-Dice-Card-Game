# scenes/menu_scene.py
import pygame
import time
from scene import Scene  # Base scene class



class MenuScene(Scene):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.font = pygame.font.SysFont(None, 48)
        self.start_time = time.time()
        self.flash = True

        self.logo = pygame.image.load("assets/images/menu_scene.png").convert_alpha()

    def update(self):
        current_time = time.time()
        if current_time - self.start_time > 0.25:
            self.flash = not self.flash
            self.start_time = current_time
        pass

    def draw(self, screen):
        # Draw the full-screen background image
        screen.blit(self.logo, (0, 0))

        # Optional overlay text (e.g., flashing "Press SPACE")
        if self.flash:
            prompt = self.font.render("Press SPACE to start", True, (0, 0, 0))
            screen.blit(prompt, (450, 700))  # Adjust Y as needed

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                from scenes.pet_select_scene import PetSelectScene
                self.engine.set_scene(PetSelectScene(self.engine))
        pass



