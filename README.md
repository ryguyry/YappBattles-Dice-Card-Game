# yappbattles 🐱🐶🎲🃏
A turn-based **card + dice battle game** built with **Python and Pygame**, where cats and dogs battle using attacks, healing, and support cards.

> Status: **Work in Progress** — core gameplay is functional and playable, with ongoing development focused on content expansion, balance, and polish.

---

## Gameplay Overview
- Select a pet (cat or dog)
- Enter a turn-based battle
- Each turn:
  - Draw cards from a deck
  - Roll dice to influence outcomes
  - Play **Attack**, **Healing**, or **Support** cards
- Win by reducing the opponent’s HP to zero while managing resources and randomness

---

## Features
- Turn-based combat system
- Card-based mechanics:
  - Attack cards
  - Healing cards
  - Support/utility cards
- Dice rolling for randomness and variability
- Scene-based architecture (menu, pet selection, battle)
- Modular design for easily adding new cards, pets, and mechanics
- Built using **Pygame** for rendering, input handling, and the game loop

---

## Tech Stack
- **Language:** Python  
- **Game Library:** Pygame  
- **Architecture:** Modular, scene-based design  
- **Paradigms:** Object-oriented and data-oriented design principles

---

## Getting Started

### Requirements
- Python **3.10+**
- Pygame
- 
This project requires additional image assets.  
Download them here and place them in the `assets/` directory: https://drive.google.com/file/d/1XFqttKkuWj4WlNw-s6TOt1Q4N5Uj2STf/view?usp=sharing

### Install
Clone the repository and set up a virtual environment:

git clone https://github.com/<your-username>/yappbattles.git
cd yappbattles

python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS / Linux:
source .venv/bin/activate
