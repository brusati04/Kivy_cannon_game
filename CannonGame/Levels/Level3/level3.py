from kivy.uix.widget import Widget
from kivy.graphics.vertex_instructions import Rectangle
from kivy.clock import Clock

from Levels.levels import *  # Import classes from the Levels module
from part_tank import *  # Import classes from part_tank module
from projectile import *  # Import classes from projectile module
from entities import *  # Import classes from entities module


# Class definition for level3, inheriting from level_template
class level3(level_template):
    def __init__(self, **kw):
        super().__init__(**kw)
        pass
    
    # This method is called when the level is entered
    def on_enter(self):
        self.add_widget(Level3_game())  # Adds Level3_game widget to the level
        self.play()  # Starts playing the level
        # Displays a help popup for level 3 with a specific text file
        popup = popupHelp(self, text_file="assets/help_text/level3_message.txt")
        popup.open()  # Opens the help popup window


# Class for setting the background of level 3
class Background3(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Draws a background image on the widget's canvas
        with self.canvas:
            self.rect = Rectangle(source="assets/images/sfondo4.png", pos=self.pos, size=self.size)
        # Binds position and size so that it updates if the widget's position or size changes
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Method to update the rectangle's position and size based on the widget
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# Class for the terrain (ground) of level 3
class Terrain3(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Draws the terrain image
        with self.canvas:
            self.rect = Rectangle(source="assets/images/ground/ground_level_2.png", pos=self.pos, size=self.size)
        # Binds position and size to update when changed
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Method to update the terrain rectangle's position and size
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# Class for the main game logic of level 3
class Level3_game(Levels):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Schedule the `update` method to run continuously at intervals defined by `time_step`
        Clock.schedule_interval(self.update, self.time_step)
        
        # Create glass barriers at specific positions and sizes
        self.glass1 = Glass(pos=(1400, 200), size=(30, 200))  # Right-side glass
        self.glass2 = Glass(pos=(500, 950), size=(600, 30))  # Top glass
        self.glass3 = Glass(pos=(25, 800), size=(30, 200))  # Left-side glass
        self.glass4 = Glass(pos=(500, 150), size=(800, 30))  # Bottom glass
        self.glass5 = Glass(pos=(1400, 700), size=(30, 200))  # Second right-side glass

        # Add the glass objects to the game
        self.add_widget(self.glass1)
        self.add_widget(self.glass2)
        self.add_widget(self.glass3)
        self.add_widget(self.glass4)
        self.add_widget(self.glass5)

        # Track the glass objects in the `entities` list for behavior management
        self.entities.append(self.glass1)
        self.entities.append(self.glass2)
        self.entities.append(self.glass3)
        self.entities.append(self.glass4)
        self.entities.append(self.glass5)

        # Create an obstacle on the ground
        self.obstacle1 = Ground(pos=(0, 500), size=(350, 80))  # Ground obstacle
        self.add_widget(self.obstacle1)  # Add the obstacle to the game
        self.entities.append(self.obstacle1)  # Track it in `entities`

        # Add horizontal and vertical blocks to the game
        blocks = Block_horiz(pos=(0, 750), size=(80, 30))  # Horizontal block
        self.add_widget(blocks)
        self.entities.append(blocks)

        block2 = Block_vert(pos=(1050, 1000), size=(30, 80))  # Vertical block
        self.add_widget(block2)
        self.entities.append(block2)

        # Add enemy soldiers to the game with specific positions and sizes
        enemy1 = Soldier1(pos=(25, 540), size=(100, 200))  # First enemy soldier
        self.add_widget(enemy1)  # Add the enemy to the game
        self.entities.append(enemy1)  # Track the enemy in `entities`

        enemy2 = Soldier2(pos=(125, 540), size=(100, 200))  # Second enemy soldier
        self.add_widget(enemy2)  # Add the enemy to the game
        self.entities.append(enemy2)  # Track the enemy in `entities`

        enemy3 = Soldier3(pos=(225, 540), size=(100, 200))  # Third enemy soldier
        self.add_widget(enemy3)  # Add the enemy to the game
        self.entities.append(enemy3)  # Track the enemy in `entities`
