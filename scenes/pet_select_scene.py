import pygame
import time
from scene import Scene
from pets import Dog, Cat
from scenes.battle_scene import BattleScene

#from Subclasses import Dog, Cat

class PetSelectScene(Scene):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.font = pygame.font.SysFont(None, 40)

        # Load pet images
        raw_cat = pygame.image.load("assets/images/cat.png")
        raw_dog = pygame.image.load("assets/images/dog.png")

        self.cat_img = scale_to_box(raw_cat, 200, 220)
        self.dog_img = scale_to_box(raw_dog, 200, 220)

        self.selected_index = 0  # 0 = cat, 1 = dog
        self.confirming = False

        # Flash timer
        self.flash_visible = True
        self.last_flash_time = time.time()



    def update(self):
        if time.time() - self.last_flash_time > 0.4:
            self.flash_visible = not self.flash_visible
            self.last_flash_time = time.time()

    def draw(self, screen):
        screen.fill((30, 30, 30))

        # Get screen center
        screen_center_x = screen.get_width() // 2

        # Draw pet images (centered with spacing)
        cat_rect = self.cat_img.get_rect(center=(screen_center_x - 150, 240))
        dog_rect = self.dog_img.get_rect(center=(screen_center_x + 150, 240))
        screen.blit(self.cat_img, cat_rect.topleft)
        screen.blit(self.dog_img, dog_rect.topleft)

        # Draw selection outline
        if self.confirming:
            selected_rect = cat_rect if self.selected_index == 0 else dog_rect
            outline_rect = selected_rect.inflate(10, 10)  # Slight padding around image
            pygame.draw.rect(screen, (255, 255, 0), outline_rect, width=4)
        elif self.flash_visible:
            selected_rect = cat_rect if self.selected_index == 0 else dog_rect
            outline_rect = selected_rect.inflate(10, 10)  # Slight padding around image
            pygame.draw.rect(screen, (255, 255, 0), outline_rect, width=4)

        # Title text
        line1 = self.font.render("LEFT/RIGHT to choose", True, (200, 200, 200))
        line2 = self.font.render("Press ENTER to select", True, (200, 200, 200))
        screen.blit(line1, line1.get_rect(center=(screen_center_x, 80)))
        screen.blit(line2, line2.get_rect(center=(screen_center_x, 110)))

        # Confirmation UI
        if self.confirming:
            pet_name = "Cat" if self.selected_index == 0 else "Dog"
            confirm_text = self.font.render(f"You chose {pet_name}. Confirm?", True, (255, 255, 255))
            screen.blit(confirm_text, confirm_text.get_rect(center=(screen_center_x, 450)))

            # Flashing "Press ENTER again"
            if self.flash_visible:
                flashing = self.font.render("Press ENTER again to confirm", True, (255, 255, 0))
                screen.blit(flashing, flashing.get_rect(center=(screen_center_x, 500)))

            # Backspace note
            back_note = self.font.render("(Backspace to go select again)", True, (150, 150, 255))
            screen.blit(back_note, back_note.get_rect(center=(screen_center_x, 540)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.confirming:
                if event.key == pygame.K_LEFT:
                    self.selected_index = 0
                elif event.key == pygame.K_RIGHT:
                    self.selected_index = 1
                elif event.key == pygame.K_RETURN:
                    self.confirming = True
            else:
                if event.key == pygame.K_RETURN:
                    if self.selected_index == 0:
                        pet = Cat("YourCat", "Black")
                        image_path = "assets/images/cat.png"
                    else:
                        pet = Dog("YourDog", "Chihuahua")
                        image_path = "assets/images/dog.png"

                    self.engine.set_scene(BattleScene(self.engine, pet, image_path))

def scale_to_box(image, max_width, max_height):
    rect = image.get_rect()
    scale_x = max_width / rect.width
    scale_y = max_height / rect.height
    scale = min(scale_x, scale_y)
    new_size = (int(rect.width * scale), int(rect.height * scale))
    return pygame.transform.smoothscale(image, new_size)
