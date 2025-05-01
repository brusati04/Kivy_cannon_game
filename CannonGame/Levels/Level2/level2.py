from kivy.uix.widget import Widget
from kivy.graphics.vertex_instructions import Rectangle
import random
from kivy.clock import Clock

from Levels.levels import *  # Importing classes and functions from 'levels'
from part_tank import *  # Importing classes from 'part_tank'
from projectile import *  # Importing classes from 'projectile'
from entities import *  # Importing classes from 'entities'

# Class definition for level2, which is a subclass of level_template
class level2(level_template):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass

    # When the level is entered, this method is triggered
    def on_enter(self):
        self.add_widget(Level2_game())  # Adds the Level2_game widget to the screen
        self.play()  # Starts playing the level
        # Displays a help popup message for level 2, pulling text from an external file
        popup = popupHelp(self, text_file="assets/help_text/level2_message.txt")
        popup.open()  # Opens the help popup

# Class to handle the background of the level
class Background2(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Draws a rectangle with an image as a background
        with self.canvas:
            self.rect = Rectangle(source="assets/images/deserto.png", pos=self.pos, size=self.size)
        # Binds position and size to update when changed
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Method to update rectangle position and size when the widget is resized or moved
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# Class to handle the terrain (ground) of the level
class Terrain2(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Draws a rectangle with an image of the terrain
        with self.canvas:
            self.rect = Rectangle(source="assets/images/ground/ground_level_2.png", pos=self.pos, size=self.size)
        # Binds position and size to update when changed
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Method to update terrain position and size when the widget is resized or moved
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# Main class to define the gameplay for level 2
class Level2_game(Levels):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Schedule the `spawn_help` method to be called once after 4 seconds
        Clock.schedule_once(self.spawn_help, 4)
        # Schedule enemy spawning every 2 seconds
        Clock.schedule_interval(self.spawn_enemies, 2)
        # Schedule help item spawning every 10 seconds
        Clock.schedule_interval(self.spawn_help, 10)
        # Schedule the `update` method based on the time_step defined in the parent class
        Clock.schedule_interval(self.update, self.time_step)

    # Method to spawn enemies at random positions
    def spawn_enemies(self, dt):
        if not self.pause:  # Checks if the game is not paused
            # Creates an enemy at a random x-coordinate within certain bounds at the top of the screen (falling enemy)
            enemy = Training_falling(pos=(random.randint(self.width - 1200, self.width - 300), self.height))
            self.add_widget(enemy)  # Adds the enemy to the game
            self.entities.append(enemy)  # Keeps track of the enemy for behavior management

    # Method to spawn help items (like ammo drops) at regular intervals
    def spawn_help(self, dt):
        y = 0  # Initial y-position
        part_tank = self.ids['part_tank']  # Reference to a part tank object from the widget tree
        # Loop to create three help items at different heights (y-offset)
        for i in range(3):
            help = AmmoDrop(part_tank, pos=(1300, 250 + y), size=(90, 130))  # Creates an AmmoDrop object
            y += 300  # Increments y-position for the next drop
            self.add_widget(help)  # Adds the help item to the game
            self.entities.append(help)  # Keeps track of the help item for behavior management
