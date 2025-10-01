# scenes/battle_scene.py
import pygame
import time
import random
from scene import Scene
from cards.deck import load_full_deck

class BattleScene(Scene):
    def __init__(self, engine, pet, image_path):
        super().__init__()
        self.engine = engine
        self.pet = pet
        self.font = pygame.font.SysFont(None, 36)

        # Bars
        self.max_health = 100
        self.health = 100
        self.max_stamina = 5
        self.stamina = 5
        self.enemy_max_health = 100
        self.enemy_max_stamina = 5

        # Load pet image
        self.pet_image = pygame.image.load(image_path)
        self.pet_image = pygame.transform.scale(self.pet_image, (100, 100))

        # Dice images
        die_size = 144  # Adjust to the size you want

        self.dice_images = [
            pygame.transform.scale(
                pygame.image.load(f"assets/images/dice/die{i}.png"),
                (die_size, die_size)
            )
            for i in range(1, 7)
        ]

        self.current_die_index = 0
        self.final_die_value = None
        self.rolling = False
        self.roll_start_time = 0

        self.instructions_shown = True

        self.last_dice_update = 0
        self.dice_cycle_interval = 0.1  # seconds

        self.awaiting_card_draw = False

        self.hand = []  # Will hold the 5 cards
        self.hand_loaded = False

        self.waiting_for_next_action = False

        self.player_message = ""
        self.player_message_time = 0

        # Automatically assign enemy as opposite of player pet
        from pets import Dog, Cat

        if isinstance(pet, Dog):
            self.enemy = Cat("EnemyCat", "Siamese")
            self.enemy_image = pygame.image.load("assets/images/cat.png")
        else:
            self.enemy = Dog("EnemyDog", "Bulldog")
            self.enemy_image = pygame.image.load("assets/images/dog.png")

        self.enemy_image = pygame.transform.scale(self.enemy_image, (100, 100))

        self.enemy.health = self.enemy_max_health
        self.enemy.stamina = self.enemy_max_stamina

        self.max_power = 6
        self.player_power = 0
        self.enemy_power = 0

        self.show_roll_result = False
        self.show_action_menu = False

        # Die message font size
        self.instruction_font = pygame.font.SysFont(None, 36)  # Try 36, 48, or even 60

        # Track menu option
        self.menu_options = ["Play a card", "Roll again", "Draw cards"]
        self.selected_option_index = 0

        self.deck = load_full_deck()

        self.selecting_card = False
        self.selected_card_index = 0  # Default to center (index 2 if 5 cards)

        self.first_roll_done = False

        self.opponent_turn = False
        self.turn_timer = 0  # optional timer if you want a pause
        self.enemy_action_pending = False  # Is an enemy action ready to go?

        # Enemy dice logic
        self.enemy_rolling = False
        self.enemy_die_index = 0
        self.enemy_final_die_value = None
        self.enemy_roll_start_time = 0
        self.enemy_last_dice_update = 0
        self.enemy_show_roll_result = False
        self.enemy_first_roll_done = False

        # Enemy cards logic
        self.enemy_hand = []
        self.enemy_draw_message = False

        # Enemy message
        self.opponent_action_message = ""
        self.opponent_message_time = 0  # timestamp for how long to show

    def update(self):
        if self.rolling:
            current_time = time.time()
            if current_time - self.roll_start_time < 1:
                if current_time - self.last_dice_update > self.dice_cycle_interval:
                    self.current_die_index = (self.current_die_index + 1) % 6
                    self.last_dice_update = current_time
            else:
                self.rolling = False
                self.final_die_value = random.randint(1, 6)

                # Add rolled value to power, cap at 6
                self.player_power += self.final_die_value
                if self.player_power > self.max_power:
                    self.player_power = self.max_power

                # Allow next prompt
                self.show_roll_result = True

                if not self.first_roll_done:
                    self.awaiting_card_draw = True
                    self.first_roll_done = True
                else:
                    self.show_action_menu = True

        if self.enemy_rolling:
            current_time = time.time()
            if current_time - self.enemy_roll_start_time < 1:
                if current_time - self.enemy_last_dice_update > self.dice_cycle_interval:
                    self.enemy_die_index = (self.enemy_die_index + 1) % 6
                    self.enemy_last_dice_update = current_time
            else:
                self.enemy_rolling = False
                self.enemy_final_die_value = random.randint(1, 6)
                self.enemy_power = min(self.max_power, self.enemy_power + self.enemy_final_die_value)
                print(f"Enemy rolled a {self.enemy_final_die_value}!")
                roll_result = self.enemy_final_die_value
                self.set_opponent_message(f"{self.enemy.species} rolls a {roll_result}!")
                self.enemy_show_roll_result = True

                # Draw cards only on first roll
                if not self.enemy_first_roll_done:
                    if len(self.deck) < 5:
                        self.deck = load_full_deck()
                    self.enemy_hand = [self.deck.pop() for _ in range(5)]
                    self.enemy_draw_message = True
                    self.enemy_first_roll_done = True

        if self.opponent_turn:
            if not self.enemy_action_pending:
                self.enemy_action_pending = True
                self.turn_timer = time.time()

            elif self.enemy_action_pending and time.time() - self.turn_timer > 2.5:
                self.opponent_take_action()
                self.enemy_action_pending = False

                if self.enemy.stamina == 0:
                    self.opponent_turn = False
                    self.stamina = self.max_stamina
                    self.show_action_menu = True

                    # Reset enemy roll state
                    self.enemy_rolling = False
                    self.enemy_final_die_value = None
                    self.enemy_show_roll_result = False

                    print("Your turn begins!")

    def draw(self, screen):
        screen.fill((20, 20, 20))

        # Enemy's turn text
        if self.opponent_turn:
            turn_text = self.font.render("Enemy Turn...", True, (255, 100, 100))
            screen.blit(turn_text, (screen.get_width() // 2 - 80, 20))

        # Enemy Dice
        die_x = 950  # adjust for placement under enemy
        die_y = 200  # below enemy image

        if self.enemy_rolling:
            image = self.dice_images[self.enemy_die_index]
            screen.blit(image, (die_x, die_y))
        elif self.enemy_final_die_value and self.enemy_show_roll_result:
            image = self.dice_images[self.enemy_final_die_value - 1]
            screen.blit(image, (die_x, die_y))

        # Draw pet image
        screen.blit(self.pet_image, (40, 30))

        # Health bar
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(150, 40, self.max_health, 20))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(150, 40, self.max_health - self.health, 20), width=0)

        # Stamina bar
        bar_width = 100
        bar_height = 15

        # Background
        pygame.draw.rect(screen, (0, 100, 0), pygame.Rect(150, 70, bar_width, bar_height))

        # Fill based on stamina value
        stamina_fill = int((self.stamina / self.max_stamina) * bar_width)
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(150, 70, stamina_fill, bar_height))

        # Player stat counters (next to bars)
        hp_text = self.font.render(f"HP: {self.health}/100", True, (255, 255, 255))
        st_text = self.font.render(f"ST: {self.stamina}/5", True, (255, 255, 255))

        # Position next to bars
        screen.blit(hp_text, (260, 40))  # right of HP bar
        screen.blit(st_text, (260, 70))  # right of ST bar

        # Enemy health bar above enemy image
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(910, 40, 100, 20))  # red background
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(910, 40, self.enemy.health, 20))  # green fill

        # Enemy stamina bar
        enemy_stamina_fill = int((self.enemy.stamina / self.max_stamina) * bar_width)

        pygame.draw.rect(screen, (0, 100, 0), pygame.Rect(910, 70, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(910, 70, enemy_stamina_fill, bar_height))

        # Enemy Power bar (above image, below stamina)
        for i in range(self.max_power):
            x = 910 + i * 20
            y = 100
            color = (255, 255, 0) if i < self.enemy_power else (60, 60, 60)
            pygame.draw.rect(screen, color, pygame.Rect(x, y, 15, 15))

        # Player Power bar
        for i in range(self.max_power):
            x = 150 + i * 20  # adjust spacing as needed
            y = 100
            color = (255, 255, 0) if i < self.player_power else (60, 60, 60)
            pygame.draw.rect(screen, color, pygame.Rect(x, y, 15, 15))

        # Dice instructions
        if self.instructions_shown:
            msg = self.instruction_font.render("Press SPACE to roll the die!", True, (255, 255, 255))
            screen.blit(msg, (80, 150))

        # Dice
        if self.rolling:
            image = self.dice_images[self.current_die_index]
            screen.blit(image, (80, 200))
        elif self.final_die_value:
            image = self.dice_images[self.final_die_value - 1]
            screen.blit(image, (80, 200))

        # Enemy image (left of health bar)
        enemy_image_x = 800  # 850 (HP bar) - 110 (image width + margin)
        enemy_image_y = 30
        screen.blit(self.enemy_image, (enemy_image_x, enemy_image_y))

        # Enemy HP text (right of HP bar)
        enemy_hp_text = self.font.render(f"HP: {self.enemy.health}/100", True, (255, 255, 255))
        screen.blit(enemy_hp_text, (1020, 40))  # right of the 850 HP bar

        # Enemy ST text (right of ST bar)
        enemy_st_text = self.font.render(f"ST: {self.enemy.stamina}/5", True, (255, 255, 255))
        screen.blit(enemy_st_text, (1020, 70))  # right of the 950 ST bar

        # Dice result
        if self.final_die_value:
            die_image = self.dice_images[self.final_die_value - 1]
            screen.blit(die_image, (80, 200))

        # Die message
        if self.final_die_value and not self.rolling:
            roll_result = self.final_die_value
            if roll_result == 6:
                message = "CRITICAL! You rolled a 6!"
            elif roll_result == 1:
                message = "Ouch... Just a 1."
            else:
                message = f"You rolled a {roll_result}!"

            result_text = self.font.render(message, True, (255, 255, 255))

            # Position: center it horizontally, just below the die
            text_rect = result_text.get_rect(center=(
                screen.get_width() // 2,
                screen.get_height() // 2 - 260  # 260 = die center + offset
            ))
            screen.blit(result_text, text_rect)

        # Player message (e.g. "No cards to play")
        if self.player_message and time.time() - self.player_message_time < 2:
            msg = self.player_message
            result_text = self.font.render(msg, True, (255, 255, 0))
            text_rect = result_text.get_rect(center=(
                screen.get_width() // 2,
                screen.get_height() // 2 - 360  # adjust position if needed
            ))
            screen.blit(result_text, text_rect)

        # Enemy message
        if self.opponent_action_message and time.time() - self.opponent_message_time < 2.5:
            result_text = self.font.render(self.opponent_action_message, True, (255, 200, 200))
            text_rect = result_text.get_rect(center=(
                screen.get_width() // 2,
                screen.get_height() // 2 - 60
            ))
            screen.blit(result_text, text_rect)

        # Prompt to draw cards
        if self.awaiting_card_draw and not self.rolling:
            text = "Press SPACE to draw 5 cards"
            prompt = self.font.render(text, True, (255, 255, 0))
            text_rect = prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() - 360))
            screen.blit(prompt, text_rect)

        if self.hand_loaded:
            card_width = 200
            card_height = 300
            spacing = 20
            start_x = 50
            y = screen.get_height() - card_height - 30  # 30px from bottom

            for i, card in enumerate(self.hand):
                x = start_x + i * (card_width + spacing)

                # Draw card outline
                pygame.draw.rect(screen, (255, 255, 255), (x, y, card_width, card_height), width=3)

                # Fonts
                title_font = pygame.font.SysFont(None, 28)
                cost_font = pygame.font.SysFont(None, 24)
                desc_font = pygame.font.SysFont(None, 24)
                flavor_font = pygame.font.SysFont(None, 22, italic=True)

                # Title
                title_text = title_font.render(f"{card.name}", True, (255, 255, 255))
                title_rect = title_text.get_rect(center=(x + card_width // 2, y + 20))
                screen.blit(title_text, title_rect)

                # Cost (yellow, below title)
                cost_text = cost_font.render(f"Cost: {card.cost}", True, (255, 255, 0))
                cost_rect = cost_text.get_rect(center=(x + card_width // 2, y + 45))
                screen.blit(cost_text, cost_rect)

                # Image
                image_max_width = 160
                image_max_height = 100

                image_rect = card.image.get_rect()
                scale_x = image_max_width / image_rect.width
                scale_y = image_max_height / image_rect.height
                scale = min(scale_x, scale_y)
                new_size = (int(image_rect.width * scale), int(image_rect.height * scale))
                scaled_image = pygame.transform.smoothscale(card.image, new_size)
                scaled_rect = scaled_image.get_rect(center=(x + card_width // 2, y + 110))
                screen.blit(scaled_image, scaled_rect)

                # Description
                render_wrapped_text_centered(
                    card.description,
                    desc_font,
                    (200, 200, 200),
                    card_width - 20,
                    x + card_width // 2,
                    y + 180,
                    screen
                )

                # Flavor text
                render_wrapped_text_centered(
                    f"\"{card.text}\"",
                    flavor_font,
                    (180, 180, 180),
                    card_width - 20,
                    x + card_width // 2,
                    y + 240,
                    screen
                )

                if self.selecting_card and i == self.selected_card_index:
                    outline_rect = pygame.Rect(x, y, card_width, card_height)
                    pygame.draw.rect(screen, (255, 255, 0), outline_rect.inflate(6, 6), width=3)

        if self.show_action_menu and not self.opponent_turn:
            # Draw the menu
            box_width = 500
            box_height =250
            box_x = screen.get_width() // 2 - box_width // 2
            box_y = screen.get_height() - 640

            pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height), width=3)

            title_font = pygame.font.SysFont(None, 32)
            option_font = pygame.font.SysFont(None, 28)

            title_text = title_font.render("What do you want to do?", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(box_x + box_width // 2, box_y + 25))
            screen.blit(title_text, title_rect)

            # Draw menu options with outline around selected
            for i, option in enumerate(self.menu_options):
                text = option_font.render(f"{i + 1}. {option}", True, (200, 200, 200))
                text_x = box_x + 20
                text_y = box_y + 60 + i * 30
                screen.blit(text, (text_x, text_y))

                if i == self.selected_option_index:
                    text_rect = text.get_rect(topleft=(text_x, text_y))
                    pygame.draw.rect(screen, (255, 255, 0), text_rect.inflate(10, 4), width=2)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.show_action_menu or self.selecting_card:
                    print("SPACE press ignored: menu is open or selecting card.")
                    return

                if self.awaiting_card_draw:
                    self.awaiting_card_draw = False
                    self.hand_loaded = True
                    self.show_roll_result = False
                    self.show_action_menu = True

                    if len(self.deck) < 5:
                        self.deck = load_full_deck()

                    self.hand = [self.deck.pop() for _ in range(5)]
                    self.waiting_for_next_action = True  # Prevents accidental reroll

                elif self.selecting_card:
                    print("SPACE ignored during card selection.")
                    return
                elif not self.rolling and not self.waiting_for_next_action:
                    self.instructions_shown = False
                    self.final_die_value = None
                    self.roll_start_time = time.time()
                    self.last_dice_update = time.time()
                    self.rolling = True

            if self.show_action_menu:
                if event.key == pygame.K_DOWN:
                    self.selected_option_index = (self.selected_option_index + 1) % len(self.menu_options)
                elif event.key == pygame.K_UP:
                    self.selected_option_index = (self.selected_option_index - 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN:
                    selected = self.menu_options[self.selected_option_index]
                    print(f"Selected: {selected}")
                    self.show_action_menu = False
                    self.waiting_for_next_action = False

                    if selected == "Roll again":
                        if self.stamina > 0:
                            self.stamina = max(0, self.stamina - 1)
                            self.instructions_shown = False
                            self.final_die_value = None
                            self.roll_start_time = time.time()
                            self.last_dice_update = time.time()
                            self.rolling = True
                        else:
                            print("Not enough stamina to roll again.")
                        self.show_action_menu = False  # Hide menu while rolling

                        if self.stamina == 0:
                            self.start_opponent_turn()

                    elif selected == "Play a card":
                        self.selecting_card = True

                        self.selected_card_index = len(self.hand) // 2

                        if self.stamina == 0:
                            self.start_opponent_turn()

                    elif selected == "Draw cards":
                        if len(self.hand) < 5 and self.stamina > 0:
                            needed = 5 - len(self.hand)
                            draw_count = min(needed, len(self.deck))  # prevent deck underflow
                            for _ in range(draw_count):
                                if self.deck:  # ✅ Prevent pop from empty deck
                                    self.hand.append(self.deck.pop())
                            self.stamina = max(0, self.stamina - 1)
                            print(f"Drew {draw_count} card(s).")
                        else:
                            print("Can't draw: either full hand or not enough stamina.")
                        self.show_action_menu = True

                        if self.stamina == 0:
                            self.start_opponent_turn()

            elif self.selecting_card:
                if event.key == pygame.K_SPACE:
                    print("SPACE is ignored during card selection.")

                elif event.key == pygame.K_RIGHT:
                    self.selected_card_index = (self.selected_card_index + 1) % len(self.hand)

                elif event.key == pygame.K_LEFT:
                    self.selected_card_index = (self.selected_card_index - 1) % len(self.hand)

                elif event.key == pygame.K_BACKSPACE:
                    print("Canceled card selection.")
                    self.selecting_card = False
                    self.show_action_menu = True

                elif event.key == pygame.K_RETURN:
                    if not self.hand:
                        print("No cards to play.")
                        self.set_player_message("No cards to play.")
                        self.selecting_card = False
                        self.show_action_menu = True
                        return  # Exit early to prevent crash
                    selected_card = self.hand[self.selected_card_index]
                    print(f"Played card: {selected_card.name}")

                    # Check if player can afford the card
                    if self.player_power >= selected_card.cost:
                        self.player_power -= selected_card.cost

                        # Apply card effects
                        if selected_card.damage > 0:
                            self.enemy.health = max(0, self.enemy.health - selected_card.damage)
                            print(f"Enemy takes {selected_card.damage} damage!")

                        if selected_card.heal > 0:
                            self.health = min(self.max_health, self.health + selected_card.heal)
                            print(f"You heal {selected_card.heal} HP!")

                        if selected_card.stamina > 0:
                            self.stamina = min(self.max_stamina, self.stamina + selected_card.stamina)
                            print(f"You gain {selected_card.stamina} stamina!")

                        # Power effect
                        if selected_card.power != 0:
                            if selected_card.power > 0:
                                self.player_power = min(self.max_power, self.player_power + selected_card.power)
                                print(f"You gain {selected_card.power} power!")
                            else:
                                # Remove power from enemy, but not below 0
                                self.enemy_power = max(0, self.enemy_power + selected_card.power)
                                print(f"Enemy loses {-selected_card.power} power!")

                        # Apply stamina cost for using a card
                        self.stamina = max(0, self.stamina - 1)

                        # Remove the card from hand
                        self.hand.pop(self.selected_card_index)

                        # Reset selection state
                        self.selecting_card = False
                        self.selected_card_index = 0

                        # Return to menu after playing
                        self.show_action_menu = True

                    else:
                        print("Not enough power to play this card.")

    def start_opponent_turn(self):
        print("Opponent's turn begins!")
        self.enemy.stamina = self.max_stamina  #refill enemy stamina
        self.opponent_turn = True
        self.show_action_menu = False
        self.selecting_card = False
        self.selected_card_index = 0
        self.turn_timer = time.time()

        if not self.enemy_first_roll_done:
            if len(self.deck) < 5:
                self.deck = load_full_deck()
            self.enemy_hand = [self.deck.pop() for _ in range(5)]
            print("Opponent initializes 5 cards to hand from the deck.")
            self.enemy_first_roll_done = True

    def opponent_take_action(self):
        # If no cards, try to draw
        if not self.enemy_hand:
            print("Enemy hand is empty — drawing new cards.")
            to_draw = min(5, len(self.deck))
            for _ in range(to_draw):
                if self.deck:
                    self.enemy_hand.append(self.deck.pop())
            self.enemy.stamina -= 1
            self.set_opponent_message(f"{self.enemy.species} draws.")

            # If still no cards after drawing, roll instead
            if not self.enemy_hand:
                print("Enemy has no cards even after drawing — rolling instead.")
                self.enemy_rolling = True
                self.enemy_final_die_value = None
                self.enemy_roll_start_time = time.time()
                self.enemy_last_dice_update = time.time()
                self.enemy_show_roll_result = False
            return

        player_hp = self.health
        player_power = self.player_power

        def can_play(the_card):
            return the_card.cost <= self.enemy_power

        # 1. Critical hit if player HP < 30
        if player_hp < 30:
            playable_attacks = [c for c in self.enemy_hand if c.damage > 0 and can_play(c)]
            if playable_attacks:
                card = max(playable_attacks, key=lambda c: c.damage)
                self._enemy_play_card(card)
                return

        # 2. Player HP > 50 → use strongest affordable attack
        if player_hp > 50:
            playable_attacks = [c for c in self.enemy_hand if c.damage > 0 and can_play(c)]
            if playable_attacks:
                card = max(playable_attacks, key=lambda c: c.damage)
                self._enemy_play_card(card)
                return

        # 3. Play all affordable attack cards
        attack_cards = [c for c in self.enemy_hand if c.damage > 0 and can_play(c)]
        if attack_cards and self.enemy.stamina > 0:
            card = max(attack_cards, key=lambda c: c.damage)
            self._enemy_play_card(card)
            return

        # 4. Play best support card to increase power
        if self.enemy_power < self.max_power:
            support = [c for c in self.enemy_hand if c.power > 0 and can_play(c)]
            if support:
                card = max(support, key=lambda c: c.power)
                self._enemy_play_card(card)
                return

        # 5. Heal if HP low
        if self.enemy.health < 65:
            heals = [c for c in self.enemy_hand if c.heal > 0 and can_play(c)]
            if heals:
                card = max(heals, key=lambda c: c.heal)
                self._enemy_play_card(card)
                return

        # 6. Reduce player power if it's high
        if player_power > 3:
            drainers = [c for c in self.enemy_hand if c.power < 0 and can_play(c)]
            if drainers:
                card = max(drainers, key=lambda c: c.power)  # negative number
                self._enemy_play_card(card)
                return

        # 7. Play any valid card
        any_card = [c for c in self.enemy_hand if can_play(c)]
        if any_card:
            card = any_card[0]
            self._enemy_play_card(card)
            return

        # 8. Draw more cards if fewer than 3 and no attacks
        if len(self.enemy_hand) < 3:
            has_damage = any(c.damage > 0 for c in self.enemy_hand)
            if not has_damage and len(self.deck) > 0:
                to_draw = min(5 - len(self.enemy_hand), len(self.deck))
                for _ in range(to_draw):
                    self.enemy_hand.append(self.deck.pop())
                self.enemy.stamina -= 1
                self.set_opponent_message(f"{self.enemy.species} draws.")
                print("Enemy draws to refill hand.")
                return

        # 9. Roll again as fallback
        if self.enemy.stamina > 0:
            print("Enemy has no good cards — rolling again.")
            self.enemy_rolling = True
            roll_result = self.enemy_final_die_value
            self.set_opponent_message(f"{self.enemy.species} rolls a {roll_result}!")
            self.enemy_final_die_value = None
            self.enemy_roll_start_time = time.time()
            self.enemy_last_dice_update = time.time()
            self.enemy_show_roll_result = False
            self.enemy.stamina -= 1
            return

    def _enemy_play_card(self, card):
        print(f"Enemy plays {card.name}")
        desc = card.description
        self.set_opponent_message(f"{self.enemy.species} plays {card.name}. {desc}")
        self.enemy_power -= card.cost
        self.enemy_hand.remove(card)
        self.enemy.stamina -= 1

        # Apply effects
        if card.damage:
            self.health = max(0, self.health - card.damage)
            print(f"You take {card.damage} damage!")
        if card.heal:
            self.enemy.health = min(100, self.enemy.health + card.heal)
            print(f"Enemy heals {card.heal} HP!")
        if card.power:
            if card.power > 0:
                self.enemy_power = min(self.max_power, self.enemy_power + card.power)
                print(f"Enemy gains {card.power} power!")
            else:
                self.player_power = max(0, self.player_power + card.power)
                print(f"Your power is reduced by {-card.power}!")

    def set_player_message(self, message):
        self.player_message = message
        self.player_message_time = time.time()

    def set_opponent_message(self, message):
        self.opponent_action_message = message
        self.opponent_message_time = time.time()

def render_wrapped_text_centered(text, font, color, max_width, center_x, start_y, surface, line_spacing=5):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())

    y = start_y
    for line in lines:
        rendered = font.render(line, True, color)
        line_width = rendered.get_width()
        line_x = center_x - line_width // 2
        surface.blit(rendered, (line_x, y))
        y += font.get_height() + line_spacing

