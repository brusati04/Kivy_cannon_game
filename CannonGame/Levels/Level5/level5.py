from kivy.uix.widget import Widget
from kivy.graphics.vertex_instructions import Rectangle
import random
from kivy.clock import Clock

from Levels.levels import *  
from part_tank import * 
from projectile import *
from entities import *  

# Class definition for level5, inheriting from level_template
class level5(level_template):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass
    
    # Called when the level is entered
    def on_enter(self):
        self.add_widget(Level5_game())  # Adds the Level5_game widget to the level
        self.play()  # Starts the game logic for level 5
        # Displays a help popup for level 5 using text from a specific file
        popup = popupHelp(self, text_file="assets/help_text/level5_message.txt")
        popup.open()  # Opens the help popup

# Class for setting the background of level 5
class Background5(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Draws a background image on the widget's canvas
        with self.canvas:
            self.rect = Rectangle(source="assets/images/sfondo66.png", pos=self.pos, size=self.size)
        # Binds position and size to update the background image when the widget is resized or moved
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Method to update the rectangle's position and size when the widget's position or size changes
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# Class for the terrain (ground) of level 5
class Terrain5(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Draws the terrain image on the widget's canvas
        with self.canvas:
            self.rect = Rectangle(source="assets/images/ground/ground_level_4.png", pos=self.pos, size=self.size)
        # Binds position and size to update the terrain when the widget's position or size changes
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Method to update the terrain rectangle's position and size when the widget's position or size changes
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# Class for the main game logic of level 5
class Level5_game(Levels):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.boss_life = 1  # Tracks the boss's life (starts at 1)

        # Create a glass barrier and add it to the game
        glass = Glass(pos=(1400, 500), size=(30, 400))  # Glass barrier
        self.add_widget(glass)
        self.entities.append(glass)  # Track the glass object in the `entities` list for behavior management

        # Create a plane and add it to the game
        aereo = Plane(pos=(470, 700), size=(600, 270))  # Large plane object
        self.add_widget(aereo)
        self.entities.append(aereo)  # Track the plane in `entities`

        # Create a jet and add it to the game
        jet = Jet(pos=(275, 500), size=(100, 130))  # Jet enemy
        self.add_widget(jet)
        self.entities.append(jet)  # Track the jet in `entities`

        # Schedule the appearance of the final boss after 20 seconds
        Clock.schedule_once(self.spawn_ILBOSS, 20)
        # Schedule the spawning of regular enemies every 2 seconds
        Clock.schedule_interval(self.spawn_enemies, 2)
        # Schedule the spawning of help items (like ammo drops) every 8 seconds
        Clock.schedule_interval(self.spawn_help, 8)
        # Continuously update the game using the `update` method at intervals defined by `time_step`
        Clock.schedule_interval(self.update, self.time_step)

    # Method to spawn the final boss after 20 seconds
    def spawn_ILBOSS(self, dt):
        if not self.pause:  # Check if the game is not paused
            ilboss_finale = ILBOSS(pos=(900, 820), size=(180, 180))  # Create the final boss at a specific position
            self.add_widget(ilboss_finale)  # Add the boss to the game
            self.entities.append(ilboss_finale)  # Track the boss in `entities`

    # Method to spawn regular enemies at intervals
    def spawn_enemies(self, dt):
        if not self.pause:  # Check if the game is not paused
            enemies = Sky_enemy(pos=(random.randint(500, 1090), 525), size=(50, 50))  # Create a sky enemy at a random x-coordinate
            self.add_widget(enemies)  # Add the enemy to the game
            self.entities.append(enemies)  # Track the enemy in `entities`

    # Method to spawn help items (like ammo drops) at intervals
    def spawn_help(self, dt):
        part_tank = self.ids['part_tank']  # Access the tank part widget (e.g., for managing ammo)
        help = AmmoDrop(part_tank, pos=(1300, 250), size=(90, 120))  # Create an ammo drop at a specific position
        self.add_widget(help)  # Add the help item to the game
        self.entities.append(help)  # Track the help item in `entities`
