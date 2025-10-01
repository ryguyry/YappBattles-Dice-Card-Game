#engine.py
import pygame
import sys

class GameEngine:
    def __init__(self, width=1200, height=800, title="YaPP!"):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = None

    def set_scene(self, scene):
        self.scene = scene

    def run(self):
        while self.running:
            self.handle_events()
            if self.scene:
                self.scene.update()
                self.scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.scene:
                self.scene.handle_event(event)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()