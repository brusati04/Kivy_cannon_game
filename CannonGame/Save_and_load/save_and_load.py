from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import json

# Class definition for a screen that handles saving and loading user data
class save_and_load(Screen):
    # Property that holds the text input value, which is bound to the text input widget in the UI
    text_input_str = StringProperty(" ")

    # Method triggered when the user presses 'Enter' or validates the text input
    def on_text_validate(self, widget):
        self.text_input_str = widget.text  # Update the property with the text input value

    # Method triggered when the user submits their nickname
    def on_submit(self):
        nickname = self.ids.player_name.text  # Retrieve the player's nickname from the text input widget with id `player_name`

        try:
            # Try to open and load the existing data from the 'record.json' file
            with open("record.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("File not found")  # If the file doesn't exist, print an error message
            return

        user_exists = False  # Flag to check if the user already exists

        # Loop through the data to check if the entered nickname already exists
        for user_data in data:
            if user_data["nickname"] == nickname:
                user_exists = True  # If the nickname is found, set the flag to True
                self.manager.player = user_data  # Set the player data in the screen manager
                break  # Stop searching once the user is found

        # If the user does not exist, create a new user
        if not user_exists:
            new_user = {
                "nickname": nickname,  # Store the entered nickname
                "score": 0,            # Initialize the score to 0
                "last_level": 1        # Initialize the last completed level to 1
            }
            data.append(new_user)  # Add the new user to the data list
            self.manager.player = new_user  # Set the new user data in the screen manager

            try:
                # Try to save the updated data back to the 'record.json' file
                with open("record.json", "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4)  # Save the JSON data with indentation for better readability
            except FileNotFoundError:
                print("File not found")  # If the file doesn't exist when writing, print an error message
                return
