from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

# Class definition for the 'upgrade' screen, which allows the user to upgrade their tank and cannon models
class upgrade(Screen):
    # StringProperty to store the current path of the tank image
    my_path_tank = StringProperty("assets/images/tanks/tank1.png")
    # List of available tank images (paths to the images)
    tanks = ["assets/images/tanks/tank1.png", "assets/images/tanks/tank2.png",
             "assets/images/tanks/tank3.png", "assets/images/tanks/tank4.png", 
             "assets/images/tanks/tank5.png"]

    # StringProperty to store the current path of the cannon image
    my_path = StringProperty("assets\\images\\tanks\\canna4_gialla.png")
    # List of available cannon images (paths to the images)
    cannons = ["assets\\images\\tanks\\canna4_gialla.png", "assets\\images\\tanks\\canna3_gialla.png", 
               "assets\\images\\tanks\\canna2_gialla.png", "assets\\images\\tanks\\canna1_gialla.png"]

    # Method to set the selected tank and cannon models for the game
    def set_model(self):
        model = self.my_path_tank  # Get the current tank path
        fusoliera = self.my_path  # Get the current cannon path
        # Call the screen manager's set_models method to apply the chosen tank and cannon
        self.manager.set_models(model, fusoliera)

    # Method to change to the next tank model
    def change_path_tank(self):
        try:
            # Get the index of the current tank, and set the next tank in the list (cyclically)
            self.my_path_tank = self.tanks[(self.tanks.index(self.my_path_tank) + 1) % len(self.tanks)]
            self.tank_instance = False  # Reset the tank instance (presumably used elsewhere in the app)
        except ValueError:
            # Handle the case where the current tank path is not found in the tanks list
            self.my_path_tank = self.tanks[0]  # Default to the first tank in the list

    # Method to change to the previous tank model
    def change_path_left_tank(self):
        try:
            # Get the index of the current tank, and set the previous tank in the list (cyclically)
            self.my_path_tank = self.tanks[(self.tanks.index(self.my_path_tank) - 1) % len(self.tanks)]
            self.tank_instance = False  # Reset the tank instance (presumably used elsewhere in the app)
        except ValueError:
            # Handle the case where the current tank path is not found in the tanks list
            self.my_path_tank = self.tanks[-1]  # Default to the last tank in the list

    # Method to change to the next cannon model
    def change_path(self):
        try:
            # Get the index of the current cannon, and set the next cannon in the list (cyclically)
            self.my_path = self.cannons[(self.cannons.index(self.my_path) + 1) % len(self.cannons)]
            self.tank_instance = False  # Reset the tank instance (presumably used elsewhere in the app)
        except ValueError:
            # Handle the case where the current cannon path is not found in the cannons list
            self.my_path = self.cannons[0]  # Default to the first cannon in the list

    # Method to change to the previous cannon model
    def change_path_left(self):
        try:
            # Get the index of the current cannon, and set the previous cannon in the list (cyclically)
            self.my_path = self.cannons[(self.cannons.index(self.my_path) - 1) % len(self.cannons)]
            self.tank_instance = False  # Reset the tank instance (presumably used elsewhere in the app)
        except ValueError:
            # Handle the case where the current cannon path is not found in the cannons list
            self.my_path = self.cannons[-1]  # Default to the last cannon in the list
