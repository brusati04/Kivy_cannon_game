from kivy.uix.widget import Widget
from kivy.graphics.vertex_instructions import Rectangle
from kivy.clock import Clock  
# Import custom classes from different modules to handle levels, tank parts, projectiles, and entities
from Levels.levels import *  
from part_tank import *  
from projectile import *  
from entities import *  


# The `level1` class is a specific implementation of `level_template`, representing the first level in the game.
class level1(level_template):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass  # No additional initialization is needed

    # Method that is called when the level screen is entered
    def on_enter(self):
        self.add_widget(Level1_game())  # Add the game logic (Level1_game) as a widget to the level
        self.play()  # Start the level gameplay
        # Show a popup with help instructions for level 1
        popup = popupHelp(self, text_file="assets/help_text/level1_message.txt")
        popup.open()  # Open the help popup


# The `Background1` class creates and manages the background for level 1
class Background1(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # Create a rectangle with an image as its source, representing the background
            self.rect = Rectangle(source="assets/images/sfondo.png", pos=self.pos, size=self.size)
        # Bind the rectangle's position and size to update with the widget's size and position
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Method to update the rectangle's position and size when the widget's properties change
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# The `Terrain` class creates and manages the terrain for level 1
class Terrain(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # Create a rectangle with an image as its source, representing the ground/terrain
            self.rect = Rectangle(source="assets/images/ground/ground_level_1.png", pos=self.pos, size=self.size)
        # Bind the rectangle's position and size to update with the widget's size and position
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Method to update the rectangle's position and size when the widget's properties change
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# The `Level1_game` class handles the game logic for level 1, inheriting from `Levels`
class Level1_game(Levels):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Schedule the `spawn` method to be called once after a delay
        Clock.schedule_once(self.spawn)
        # Schedule the `update` method to be called repeatedly at regular intervals (every frame)
        Clock.schedule_interval(self.update, self.time_step)

    # Method to spawn enemies on the game field
    def spawn(self, dt):
        x = 0  # Initial horizontal position for enemies
        for i in range(3):  # Loop to create 3 columns of enemies
            x += 300  # Increment the horizontal position for each column
            y = 0  # Reset the vertical position for each new column
            for enemy in range(3):  # Loop to create 3 enemies in each column
                # Create a `Training_Enemy` at the specified position
                enemy = Training_Enemy(pos=(300 + x, 150 + y))
                y += 300  # Increment the vertical position for the next enemy
                # Add the enemy widget to the game and store it in the `entities` list for tracking
                self.add_widget(enemy)
                self.entities.append(enemy)

        # Example code for spawning a single enemy (commented out):
        # enemy = Training_Enemy(pos = (300, 150))
        # self.add_widget(enemy)  # Add the enemy to the game
        # self.entities.append(enemy)  # Track the enemy in the entities list
