from kivy.uix.screenmanager import Screen  # Import the Screen class to manage different screens in the app
from kivy.uix.widget import Widget  # Import Widget as the base class for all UI components
from kivy.uix.image import Image  # Import Image to display images in the UI
from kivy.uix.popup import Popup  # Import Popup to create modal windows
from kivy.uix.label import Label  # Import Label to display text in the UI

# Importing custom classes from other modules, which handle different aspects of the game.
from part_tank import Part_tank, Tank  
from projectile import Bullet, Laser, Bombshell  
from entities import *  
from popup import *  


# The `levels` class represents a screen in the app where the user selects a game level.
class levels(Screen):  
    # Method to check if the user has access to a certain level.
    def check_level(self, n):  
        # If the player's last completed level is greater than or equal to the desired level, navigate to the corresponding level page.
        if self.manager.player['last_level'] >= n:
            self.manager.goto_screen(f"level{n}_page")
        else:
            # If the player does not have access, show a popup.
            popup = NoAccess()
            popup.open()


# The `NoAccess` class creates a popup window indicating the user cannot access the level yet.
class NoAccess(Popup):  
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "W-A-R---N-I-N-G"  # Title of the popup
        self.title_align = "center"  # Aligns the title in the center
        self.size_hint = (0.6, 0.4)  # Sets the popup size
        self.auto_dismiss = True  # Popup will auto-dismiss when clicked outside
        
        # Create the label with a warning message and set its properties like text, color, font, and alignment
        self.txt_noaccess = Label(
            text="You cannot access this level yet. Complete the previous levels",
            color=(1, 1, 1, 1),
            font_name="assets/fonts/Unispace.ttf",
            font_size="15dp",
            halign='center',  # Horizontally center the text
            valign='middle'  # Vertically align the text to the middle
        )
        self.content = self.txt_noaccess  # Add the label to the popup content


# The `level_template` class represents a generic template for game levels with methods to pause and play.
class level_template(Screen):
    def play(self):
        # Loop through the child widgets to resume gameplay.
        for current_level in self.children:
            if isinstance(current_level, Levels):
                current_level.pause = False  # Resume the level
            # Loop through each widget and resume game elements (e.g., tanks, projectiles)
            for widget in current_level.children:
                if isinstance(widget, Tank):
                    widget.model = self.manager.model
                if isinstance(widget, Part_tank):
                    widget.fusoliera = self.manager.fusoliera
                if isinstance(widget, (Part_tank, Bullet, Laser, Bombshell)):
                    widget.pause = False  # Resume projectiles

    def pause(self):
        # Loop through child widgets to pause gameplay.
        for current_level in self.children:
            if isinstance(current_level, Levels):
                current_level.pause = True  # Pause the level
            for widget in current_level.children:
                if isinstance(widget, (Part_tank, Bullet, Laser, Bombshell)):
                    widget.pause = True  # Pause projectiles


# The `Levels` class defines the core mechanics and gameplay logic for a level.
class Levels(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pause = True  # Pauses the game initially
        self.score = 0  # Initialize the score
        self.life = 1  # Initialize the player’s life
        
        # Lists to keep track of game entities and projectiles
        self.entities = []  
        self.projectiles = []  
        
        self.time_step = 1/60  # The time interval for updates (60 FPS)

    def exit(self):
        # Calls the parent to pause the game when exiting
        self.parent.pause()

    # Update method that runs every frame to check game status and update the level.
    def update(self, dt):
        if not self.pause:
            self.check_endgame()  # Check if game conditions are met (win/lose)
            part_tank = self.ids['part_tank']
            tank = self.ids['tank']
            tank.update_canvas()  # Update the tank's graphical representation
            part_tank.move_and_update_canvas(dt)  # Move and update tank parts

            # Update HUD elements (ammo, score, etc.)
            self.ids['current_bullet'].text = "CURRENT: " + part_tank.current_bullet
            self.ids['bullets_label'].text = "AMMO: " + str(part_tank.munizioni)
            self.ids['score_label'].text = "SCORE: " + str(self.score)

            # Loop through each entity and projectile for collision detection
            for entity in self.entities[:]:
                entity.move()
                for projectile in self.projectiles[:]:
                    if entity.check_collision(projectile):
                        match projectile.__class__.__name__:
                            # Handle different projectile types (Bullet, Bombshell, Laser)
                            case "Bullet":
                                self.remove_widget(projectile)
                                self.projectiles.remove(projectile)
                                entity.on_collision(projectile)
                                break

                            case "Bombshell":
                                projectile.mini_bullets(projectile.pos)  # Create mini bullets on collision
                                self.remove_widget(projectile)
                                self.projectiles.remove(projectile)
                                entity.on_collision(projectile)
                                break

                            case "Laser":
                                if entity.__class__.__name__ == "Glass":
                                    entity.on_collision(projectile)  # Lasers only affect glass
                                else:
                                    self.remove_widget(projectile)
                                    self.projectiles.remove(projectile)
                                    entity.on_collision(projectile)
                                break
    
    # Method to check if the game is over or the player has won.
    def check_endgame(self):
        if self.ids['part_tank'].munizioni == 0:
            self.show_popup('gameover')  # Show game over popup
            self.exit()  # Exit the level
        else:
            # Handle different endgame conditions based on the level
            match self.parent.name:
                case 'level1_page':
                    if self.entities == []:
                        self.exit()
                        self.show_popup('winning')
                
                case 'level2_page':
                    if self.score >= 150:
                        self.exit()
                        self.show_popup('winning')
                    if self.score <= -200:
                        self.exit()
                        self.show_popup('final_gameover')

                case 'level3_page':
                    if self.score >= 3:
                        self.exit()
                        self.show_popup('winning')

                case 'level4_page':
                    if self.score >= 1:
                        self.exit()
                        self.show_popup('winning')

                case 'level5_page':
                    if self.score <= -200:
                        self.exit()
                        self.show_popup('final_gameover')

                    if self.boss_life == 0:
                        self.exit()
                        self.show_popup('final_winning')

    # Method to display popups based on the game state (e.g., winning, game over)
    def show_popup(self, name):
        match name:
            case 'help':
                popup = Helping_you(self)
            case 'winning':
                popup = WinningPopup(self)
            case 'final_winning':
                popup = FinalWinning(self)
            case 'gameover':
                popup = GameOverPopup(self)
            case 'final_gameover':
                popup = FinalGameOver(self)
        popup.open()


# Helping_you class displays a help popup with instructions.
class Helping_you(Popup):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.title = "I'M GONNA HELP YOU"  # Popup title
        self.title_align = "center"  # Title alignment
        self.size_hint = (0.6, 0.4)  # Popup size
        self.auto_dismiss = True  # Auto-dismiss on click outside

        # Label to display help content
        self.txt_help = Label(
            text="",
            color=(1, 1, 1, 1),
            font_name="assets/fonts/Unispace.ttf",
            font_size="15dp",
            halign='center',  # Horizontally centered text
            valign='middle'  # Vertically centered text
        )
        self.content = self.txt_help

    # Method to pause the game and read help content from a file
    def on_open(self):
        self.game.parent.pause()
        with open("assets/help_text/help.txt", 'r') as file:
            content = file.read()
        self.txt_help.text = content
        self.txt_help.height = self.txt_help.texture_size[1]
        self.txt_help.text_size = (self.width * 0.9, None)

    # When popup is closed, resume the game
    def on_dismiss(self):
        self.game.parent.play()


# Popup to display a help message before starting the game
class popupHelp(Popup):
    def __init__(self, screen, text_file, **kwargs):
        super().__init__(**kwargs)
        self.title = "Before starting the game..."  # Popup title
        self.title_align = "center"  # Title alignment
        self.screen = screen
        self.size_hint = (0.7, 0.5)  # Popup size
        self.auto_dismiss = True  # Auto-dismiss on click outside

        # Label to display the help message
        self.level_message = Label(
            text="",
            color=(1, 1, 1, 1),
            font_name="assets/fonts/Unispace.ttf",
            font_size="15dp",
            halign='left',  # Left-aligned text
            valign='middle'  # Vertically centered text
        )
        self.content = self.level_message
        self.set_text(text_file)

    # Method to load text from a file into the label
    def set_text(self, text_file):
        with open(text_file, 'r') as file:
            content = file.read()
        self.level_message.text = content

    # Method to pause the game when the popup opens
    def on_open(self):
        self.screen.pause()
        self.level_message.height = self.level_message.texture_size[1]
        self.level_message.text_size = (self.width * 0.8, None)

    # When popup is dismissed, resume the game
    def on_dismiss(self):
        self.screen.play()


# LifeBar class to visually represent the enemy's life as an image.
class LifeBar(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos = (1180, 50)  # Position of the life bar
        self.size = (300, 100)  # Size of the life bar
        # Initialize the life bar image
        self.image = Image(source="assets\\images\\life\\100.png", size=self.size, pos=self.pos)
        self.add_widget(self.image)

    # Method to update the life bar image based on the remaining life
    def update_life_bar(self, n):
        match n:
            case 5:
                self.image.source = "assets\\images\\life\\100.png"
            case 4:
                self.image.source = "assets\\images\\life\\80.png"
            case 3:
                self.image.source = "assets\\images\\life\\60.png"
            case 2:
                self.image.source = "assets\\images\\life\\40.png"
            case 1:
                self.image.source = "assets\\images\\life\\20.png"
            case 0:
                self.image.source = "assets\\images\\life\\0.png"
