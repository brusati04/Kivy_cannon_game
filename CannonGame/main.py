from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

# Import modules related to different screens and functionalities
from Save_and_load import save_and_load
from Upgrade import upgrade
from Leaderboard import leaderboard
from Help import help

# Import level-specific screens
from Levels import levels
from Levels.Level1 import level1
from Levels.Level2 import level2
from Levels.Level3 import level3
from Levels.Level4 import level4
from Levels.Level5 import level5

# Screen dimensions
SCREEN_WIDTH =  1000
SCREEN_HEIGHT = 700

# Set the screen size 
Config.set('graphics', 'width', SCREEN_WIDTH)
Config.set('graphics', 'height', SCREEN_HEIGHT)
Config.write()

# Define the home screen clas
class home(Screen):
    pass

# Custom ScreenManager class to manage transitions and navigation
class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition() # Set transition type between screens
        self.model = None # Placeholder for a model
        self.fusoliera = None # Another placeholder for additional models
        self.player = None # To store player's nickname

    # Method to set the game model and fusoliera (could represent game elements like a ship or aircraft)
    def set_models(self, model, fusoliera):
        self.model = model
        self.fusoliera = fusoliera

    # Method to navigate to different screens based on the screen name passed
    def goto_screen(self, name):
        self.clear_widgets()  # Clear current screen widgets

        # Match-case for navigating to specific screen
        match name:
            case 'home_page':
                self.add_widget(home(name=name))
            case 'save_and_load_page':
                self.add_widget(save_and_load(name=name))
            case 'leaderboard_page':
                self.add_widget(leaderboard(name=name))
            case 'help_page':
                self.add_widget(help(name=name))
            case 'upgrade_page':
                self.add_widget(upgrade(name=name))
            case 'levels_page':
                self.add_widget(levels(name=name))
            case 'level1_page':
                self.add_widget(level1(name=name))
            case 'level2_page':
                self.add_widget(level2(name=name))
            case 'level3_page':
                self.add_widget(level3(name=name))
            case 'level4_page':
                self.add_widget(level4(name=name))
            case 'level5_page':
                self.add_widget(level5(name=name))
    
    # Method to set the player's nickname
    def set_player_nickname(self, nickname):
        self.player = nickname
    
# The main application class
class MyApp(App):
    def build(self): 
        Builder.load_file("main.kv")  # Load the Kivy file for UI layout
        sm = Manager() # Create an instance of the screen manager
        sm.add_widget(home(name="home_page"))  # Add the home screen as the default
        return sm

    # Method to close the app
    def close(self):
        self.get_running_app().stop()

# Run the application
if __name__ == "__main__":
    MyApp().run() 