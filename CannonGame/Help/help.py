from kivy.uix.screenmanager import Screen

# Define a `help` class that inherits from `Screen`, used for creating a help screen in the app
class help(Screen):
    
    # This method is called when the screen is entered
    def on_enter(self):
        self.load_help_text()  # Call the method to load the help text
    
    # Method to load the help text from a file and display it in the app
    def load_help_text(self):
        # Open the help text file located in the assets folder and read its content
        with open("assets\\help_text\\Help_schermataHome.txt", "r") as file:
            contenuto = file.read()  # Store the file's content into the `contenuto` variable
        
        # Assign the file's content to the `text_help` label (assumed to exist in the screen's .kv file)
        self.ids.text_help.text = contenuto
        
        # Set custom font attributes for the `text_help` label
        self.ids.text_help.font_name = "assets/fonts/Unispace.ttf"  # Path to a custom font file
        self.ids.text_help.font_size = '15dp'  # Set font size to 15 device-independent pixels (dp)
        self.ids.text_help.color = (0, 0, 0, 1)  # Set the font color to black (R, G, B, Alpha)
        
        # Set the text alignment
        self.ids.text_help.halign = 'left'  # Horizontal alignment: left
        self.ids.text_help.valign = 'top'   # Vertical alignment: top
