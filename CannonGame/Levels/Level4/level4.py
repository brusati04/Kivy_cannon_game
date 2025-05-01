from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics.vertex_instructions import Rectangle
from kivy.clock import Clock

from Levels.levels import *
from part_tank import *
from projectile import * 
from entities import *  

# Class definition for level4, inheriting from level_template
class level4(level_template):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass

    # This method is called when the level is entered
    def on_enter(self):
        self.add_widget(Level4_game())  # Adds the Level4_game widget to the level
        self.play()  # Starts playing the level
        # Displays a help popup for level 4, loading text from a specific file
        popup = popupHelp(self, text_file="assets/help_text/level4_message.txt")
        popup.open()  # Opens the help popup window

# Class for setting the background of level 4
class Background4(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Draws a background image on the widget's canvas
        with self.canvas:
            self.rect = Rectangle(source="assets/images/sfondo60.png", pos=self.pos, size=self.size)
        # Binds position and size so that it updates if the widget's position or size changes
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Method to update the rectangle's position and size based on the widget
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# Class for the terrain (ground) of level 4
class Terrain4(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Draws the terrain image
        with self.canvas:
            self.rect = Rectangle(source="assets/images/ground/ground_level_4.png", pos=self.pos, size=self.size)
        # Binds position and size to update when changed
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Method to update the terrain rectangle's position and size
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# Class for the main game logic of level 4
class Level4_game(Levels):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create obstacles and add them to the game
        obstacle1 = Ground(pos=(900, 150), size=(100, 450))  # Large vertical ground obstacle
        self.add_widget(obstacle1)  # Adds the obstacle to the game
        self.entities.append(obstacle1)  # Track the obstacle in `entities`
        
        obstacle2 = Block_horiz_2(pos=(1300, 750), size=(200, 75))  # Horizontal block obstacle
        self.add_widget(obstacle2)  # Adds the obstacle to the game
        self.entities.append(obstacle2)  # Track the obstacle in `entities`
        
        obstacle3 = Block_horiz_2(pos=(900, 600), size=(200, 75))  # Another horizontal block obstacle
        self.add_widget(obstacle3)  # Adds the obstacle to the game
        self.entities.append(obstacle3)  # Track the obstacle in `entities`
        
        # Add a large enemy character called "Capitan"
        general = Capitan(pos=(1200, 100), size=(200, 500))  # Large enemy
        self.add_widget(general)  # Adds the enemy to the game
        self.entities.append(general)  # Track the enemy in `entities`
        
        # Add jet enemies
        jet = Jet(pos=(400, 700), size=(90, 120))  # First jet enemy
        self.add_widget(jet)  # Adds the enemy to the game
        self.entities.append(jet)  # Track the enemy in `entities`
        
        jet2 = Jet(pos=(700, 350), size=(90, 120))  # Second jet enemy
        self.add_widget(jet2)  # Adds the enemy to the game
        self.entities.append(jet2)  # Track the enemy in `entities`
        
        # Schedule events to spawn help items at specific times
        Clock.schedule_once(self.spawn_help_falling, 4)  # Spawns help after 4 seconds
        Clock.schedule_once(self.spawn_help_falling, 15)  # Spawns help again after 15 seconds
        Clock.schedule_interval(self.update, self.time_step)  # Continuously updates the game

    # Method to spawn falling help items like ammo drops
    def spawn_help_falling(self, dt):
        part_tank = self.ids['part_tank']  # Access the tank part widget (for example, ammo management)
        x = 0  # Initial x-position for the first drop
        # Spawn two help items at different x-coordinates
        for i in range(2):
            if not self.pause:  # Check if the game is not paused
                falling_help = AmmoDrop_faling(part_tank, pos=(50 + x, self.height), size=(90, 130))  # Create falling help
                x += 100  # Adjust the position for the next drop
                self.add_widget(falling_help)  # Add the falling help item to the game
                self.entities.append(falling_help)  # Track the help item in `entities` for future management
