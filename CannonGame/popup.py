from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import json

# Base class for handling endgame popups
class EndGamePopUp(Popup):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.4)  # Size of the popup
        self.game = game 
        self.title = "Game Over"
        self.title_align = 'center'
        self.screen = game.parent # The screen the game is on
        self.manager = game.parent.manager # Reference to screen manager
        self.auto_dismiss=False # Prevent popup from dismissing automaticall
        self.layout = BoxLayout(orientation='vertical') # Layout for the popup

    # Method to save player data and return to the levels screen
    def return_and_saving_data(self, instance):
            nickname = self.manager.player['nickname']  # Get player's nickname
            user_exists = False 
            current_level = self.screen.name  # Get current level name
            # Extract the number from the level name (e.g., "level1_page" -> 1)
            level_number = int(current_level.replace('level', '').replace('_page', ''))

            try:
                with open ("record.json", "r") as file:
                    data = json.load(file) # Load existing records
            except FileNotFoundError:
                print("Il file non esiste")
                return
            
            # Update user data if they exist in the file
            for user_data in data:
                if user_data['nickname'] == nickname:
                    if user_data['last_level'] == level_number:
                        user_data['last_level'] = level_number + 1 # Unlock next level

                    if user_data['score'] < self.game.score:
                        user_data['score'] = self.game.score # Update score if higher
                    
                    user_exists = True
                    self.manager.player = user_data # Update player data   
                    break

        # Save updated data back to file
            if user_exists:
                try:
                    with open ("record.json", "w", encoding="utf-8") as file:
                        json.dump(data, file, indent = 4)
                except FileNotFoundError:
                    print("Il file non esiste")
            
            # Return to the levels page
            self.manager.goto_screen('levels_page')
            self.dismiss() # Close the popup
    
    # Method to exit without saving data
    def exit(self, instance):
        self.manager.goto_screen('levels_page')
        self.dismiss()

# Popup for when the player loses due to running out of ammo
class GameOverPopup(EndGamePopUp):
    def __init__(self, game, **kwargs):
        super().__init__(game,**kwargs)
        
        # Create the label
        game_over_label = Label(text = 'Game Over! You run out of ammo!')
        self.layout.add_widget(game_over_label)

        # Create the button
        return_button = Button(text = 'Return to Levels')
        return_button.bind(on_release=self.exit)

        self.layout.add_widget(return_button)
        self.add_widget(self.layout)

# Popup for when the city is destroyed (game over scenario)
class FinalGameOver(EndGamePopUp):
    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)
        
        # Create the label
        game_over_label = Label(text = 'Game Over! \n The city has been destroyed! :(')
        self.layout.add_widget(game_over_label)

        # Create the button
        return_button = Button(text = 'Return to Levels')
        return_button.bind(on_release=self.exit)

        self.layout.add_widget(return_button)
        self.add_widget(self.layout)

# Popup for when the player wins the game
class WinningPopup(EndGamePopUp):
    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)
        self.title = "Congratulations"
        self.title_align = 'center'
        
        # Create the label
        game_over_label = Label(text = 'Congratulations, you defeated the enemies')
        self.layout.add_widget(game_over_label)

        # Create the button
        return_button = Button(text = 'Return to Levels')
        return_button.bind(on_release = self.return_and_saving_data)
        self.layout.add_widget(return_button)
        self.add_widget(self.layout)

# Popup for when the player wins the final level and saves the city
class FinalWinning(EndGamePopUp):
    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)
        self.title = "YOU WIN!"
        self.title_align = 'center'
        n = game.score + 2000 # Bonus points added for final win
        
        # Create the label
        game_over_label = Label(text = f'Congratulations, you finally saved the city, your final score has been {n}.')
        self.layout.add_widget(game_over_label)

        # Create the button
        return_button = Button(text = 'Return to Levels')
        return_button.bind(on_release = self.return_and_saving_data)

        self.layout.add_widget(return_button)
        self.add_widget(self.layout)

