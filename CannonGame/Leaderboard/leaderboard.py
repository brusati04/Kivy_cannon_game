from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
import json

# Class definition for the leaderboard screen, inheriting from `Screen`
class leaderboard(Screen):
    
    # This method is called before entering the screen (to prepare the data)
    def on_pre_enter(self, *args):
        self.load_leaderboard_data()  # Load the leaderboard data

    # Method to load and display the leaderboard data
    def load_leaderboard_data(self):
        # Load the player data from a JSON file
        with open('record.json', 'r') as f:
            players_data = json.load(f)  # Load data from the JSON file

        # Sort players by their score in descending order
        players_data.sort(key=lambda x: x['score'], reverse=True)

        # Reference the BoxLayout with id 'leaderboard_box' from the .kv file and clear any previous content
        leaderboard_box = self.ids.leaderboard_box
        leaderboard_box.clear_widgets()

        # Loop through the sorted player data and create rows in the leaderboard
        for index, player in enumerate(players_data):
            nickname = player['nickname'] or "Unknown"  # Use "Unknown" if nickname is empty
            score = str(player['score'])  # Convert the score to string for display

            # Create a GridLayout row with 2 columns: one for the nickname, one for the score
            row = GridLayout(cols=2, size_hint_y=None, height='30dp')

            # Customize the label for the top player (first index)
            if index == 0:
                # Create a nickname label for the top player with a gold color
                nickname_label = Label(
                    text=nickname,
                    font_name="assets/fonts/medieval_victoriana/medieval.ttf",  # Custom font
                    font_size="20dp",  # Set font size to 20dp
                    color=(1, 0.843, 0, 1)  # Gold color (RGB: 1, 0.843, 0)
                )
                # Create a score label for the top player with a gold color
                score_label = Label(
                    text=score,
                    font_name="assets/fonts/medieval_victoriana/medieval.ttf",  # Custom font
                    font_size="20dp",
                    color=(1, 0.843, 0, 1)  # Gold color (RGB: 1, 0.843, 0)
                )
            else:
                # Create a regular nickname label for other players (white color)
                nickname_label = Label(
                    text=nickname,
                    font_name="assets/fonts/medieval_victoriana/medieval.ttf",
                    font_size="20dp",
                    color=(1, 1, 1, 1)  # White color (RGB: 1, 1, 1)
                )
                # Create a regular score label for other players (white color)
                score_label = Label(
                    text=score,
                    font_name="assets/fonts/medieval_victoriana/medieval.ttf",
                    font_size="20dp",
                    color=(1, 1, 1, 1)  # White color (RGB: 1, 1, 1)
                )

            # Add a black background color to the nickname label
            with nickname_label.canvas.before:
                Color(0, 0, 0, 0.7)  # Set to black with 70% opacity
                nickname_label.rect = Rectangle(size=nickname_label.size, pos=nickname_label.pos)

            # Bind the nickname label's size and position to update its background rectangle
            nickname_label.bind(size=self.update_rect, pos=self.update_rect)

            # Add a black background color to the score label
            with score_label.canvas.before:
                Color(0, 0, 0, 0.7)  # Set to black with 70% opacity
                score_label.rect = Rectangle(size=score_label.size, pos=score_label.pos)

            # Bind the score label's size and position to update its background rectangle
            score_label.bind(size=self.update_rect, pos=self.update_rect)

            # Add the nickname and score labels to the GridLayout row
            row.add_widget(nickname_label)
            row.add_widget(score_label)

            # Add the row to the leaderboard's BoxLayout (to display each player)
            leaderboard_box.add_widget(row)

    # Method to update the size and position of the background rectangle when the label changes
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos  # Update the rectangle's position to match the label's position
        instance.rect.size = instance.size  # Update the rectangle's size to match the label's size
