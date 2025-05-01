# Importing necessary modules and properties from Kivy
from kivy.uix.widget import Widget
from kivy.graphics.vertex_instructions import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import PushMatrix, PopMatrix, Rotate
from numpy import sin, cos, radians, arccos, sqrt
from kivy.core.audio import SoundLoader

# Importing custom projectile classes (Bullet, Laser, Bombshell) from another module
from projectile import Bullet, Laser, Bombshell

# Tank class definition, which inherits from the Kivy `Widget`
class Tank(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = None  # Model for the tank's appearance, not set yet

        # Initial drawing of the tank as a rectangle
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size, source=self.model)
        
        # Bind the position and size of the tank widget to its rectangle, so it updates correctly
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        # This method updates the rectangle's position and size whenever the widget is updated
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_canvas(self):
        # Method to clear and redraw the canvas, useful when changing the tank's appearance
        with self.canvas:
            self.canvas.clear()  # Clear the canvas
            self.rect = Rectangle(pos=self.pos, size=self.size, source=self.model)  # Redraw the tank

# Part_tank class definition, responsible for handling tank movement, firing, and visuals
class Part_tank(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fusoliera = None  # Placeholder for the tank's fuselage image

        # Initialize variables for keypress handling, movement, rotation, etc.
        self.keysPressed = set()
        self.pause = True
        self.cooldown = 0  # Cooldown for firing
        self.rotation_angle = 0  # Rotation angle of the tank
        self.cannon_x = 0  # X-coordinate for cannon firing
        self.cannon_y = 0  # Y-coordinate for cannon firing
        self.munizioni = 20  # Number of available bullets
        self.current_bullet = 'bullet'  # Default bullet type

        # Rotation transformation to handle tank rotation during movement
        self.rotate = Rotate(angle=self.rotation_angle, axis=(0, 0, 1))

        # Loading sounds for explosions and laser fire
        self.explosion_sound = SoundLoader.load(r"assets/sounds/corto.wav")
        self.laser_sound = SoundLoader.load(r"assets/sounds/bullet_lungo.wav")

    def move_and_update_canvas(self, dt):
        # Method called during game loop to move the tank and update its appearance
        self.move_angle(dt)
        self.update_canvas()

    def move_angle(self, dt):
        # Handles changing the tank's rotation angle based on user input (keys 'a' and 'd')
        if not self.pause:  # Only rotate when not paused
            angle_change = 50 * dt  # Speed of rotation
            new_angle = self.rotation_angle

            # Change the angle based on the key pressed
            if "a" in self.keysPressed:
                new_angle += angle_change
            if "d" in self.keysPressed:
                new_angle -= angle_change

            # Normalize the angle to stay within 0-360 degrees and clamp it within certain bounds
            new_angle = new_angle % 360
            if 0 <= new_angle <= 100 or 340 <= new_angle < 360:
                self.rotation_angle = new_angle

    def update_canvas(self, *args):
        # Redraws the tank, applying any transformations (like rotation)
        if not self.pause:
            with self.canvas:
                PushMatrix()  # Push the current canvas transformation state

                # Apply rotation to the canvas based on the current angle
                self.rotate.origin = (self.x, self.center_y)
                self.rotate.angle = self.rotation_angle
                self.canvas.add(self.rotate)

                # Draw the fusoliera (the tank's fuselage) on the canvas
                with self.canvas:
                    self.rectangle = Rectangle(pos=self.pos, size=self.size, source=self.fusoliera)

                PopMatrix()  # Restore the previous transformation state

    def update_cooldown(self, *args):
        # Resets the cooldown after firing, allowing the tank to fire again
        self.cooldown = 0

    def fire(self):
        # Handles firing a projectile, adjusting based on the current bullet type
        if not self.pause:
            angle_rad = radians(self.rotation_angle)  # Convert angle to radians

            # Calculate the distance and angle for the cannon based on the tank's geometry
            d = sqrt(self.width**2 + (1/2) * self.height**2)
            theta = 0  # Default angle
            if self.current_bullet == 'laser':
                theta = arccos(self.width / d)

            # Determine cannon position based on rotation and tank dimensions
            self.cannon_x = self.x + int(d * cos(angle_rad + theta))
            self.cannon_y = self.y + int(d * sin(angle_rad + theta))

            # Fire the appropriate type of projectile based on current bullet selection
            if self.current_bullet == 'laser':
                self.fire_laser()
            if self.current_bullet == 'bullet':
                self.fire_bullet()
            if self.current_bullet == 'bombshell':
                self.fire_bombshell()
            
    def fire_bullet(self):
        # Fires a standard bullet with velocity based on tank's rotation
        bullet_velocity = 500
        angle_rad = radians(self.rotation_angle)
        velocity_x = bullet_velocity * cos(angle_rad)
        velocity_y = bullet_velocity * sin(angle_rad)

        if self.munizioni > 0:
            # Trigger explosion effect and launch the bullet
            self.explosion()
            bullet = Bullet(pos=(self.cannon_x, self.cannon_y), x_velocity=velocity_x, y_velocity=velocity_y)
            self.parent.add_widget(bullet)
            self.parent.projectiles.append(bullet)
            self.munizioni -= 1  # Decrease ammunition count
        else:
            print('munizioni terminate')  # Output message if out of ammo

    def fire_bombshell(self):
        # Fires a bombshell with slightly lower velocity
        bombshell_velocity = 400
        angle_rad = radians(self.rotation_angle)
        velocity_x = bombshell_velocity * cos(angle_rad)
        velocity_y = bombshell_velocity * sin(angle_rad)

        if self.munizioni > 0:
            self.explosion()
            bombshell = Bombshell(pos=(self.cannon_x, self.cannon_y), x_velocity=velocity_x, y_velocity=velocity_y)
            self.parent.add_widget(bombshell)
            self.parent.projectiles.append(bombshell)
            self.munizioni -= 1
        else:
            print('munizioni terminate')

    def fire_laser(self):
        # Fires a laser with higher velocity compared to bullets and bombshells
        laser_velocity = 700
        angle_rad = radians(self.rotation_angle)
        velocity_x = laser_velocity * cos(angle_rad)
        velocity_y = laser_velocity * sin(angle_rad)

        if self.munizioni > 0:
            if self.laser_sound:  # Play laser sound if available
                self.laser_sound.play()
            laser = Laser(pos=(self.cannon_x, self.cannon_y), x_velocity=velocity_x, y_velocity=velocity_y)
            self.parent.add_widget(laser)
            self.parent.projectiles.append(laser)
            self.munizioni -= 1  # Reduce ammo
        else:
            print('munizioni terminate')

    def explosion(self):
        # Handles visual and sound effects for firing (explosion)
        explosion_images = [
            r"assets\images\weapon_effect\muzzle1.png",
            r"assets\images\weapon_effect\muzzle2.png",
            r"assets\images\weapon_effect\muzzle3.png"
        ]
        explosion_index = 0
        explosion_duration = 0.1  # Duration for each frame of the explosion
        muzzle = Widget(pos=(self.cannon_x, self.cannon_y), size=(60, 60))

        if self.explosion_sound:
            self.explosion_sound.play()  # Play explosion sound

        # Function to update the explosion animation frame by frame
        def update_explosion(dt):
            nonlocal explosion_index
            if explosion_index < len(explosion_images):
                muzzle.canvas.clear()  # Clear the previous canvas
                with muzzle.canvas:
                    PushMatrix()
                    Rotate(origin=(muzzle.x, muzzle.center_y), angle=self.rotation_angle, axis=(0, 0, 1))
                    Rectangle(pos=muzzle.pos, size=muzzle.size, source=explosion_images[explosion_index])
                    PopMatrix()
                explosion_index += 1
            else:
                Clock.unschedule(update_event)  # Stop the animation when it's done
                self.parent.remove_widget(muzzle)  # Remove the muzzle effect

        # Schedule the explosion animation to run
        update_event = Clock.schedule_interval(update_explosion, explosion_duration)
        self.parent.add_widget(muzzle)  # Add the explosion to the parent widget

    def on_parent(self, widget, parent):
        # When the widget is added to a parent, set up keyboard input handling
        if parent:
            self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
            if self._keyboard:
                self._keyboard.bind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)
        else:
            # If the widget is removed, unbind keyboard events
            if self._keyboard:
                self._keyboard.unbind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)
                self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        # Handles key press events (movement and firing)
        key = keycode[1]
        if key == 'spacebar':  # Fire the cannon when the spacebar is pressed
            if self.cooldown == 0:
                self.fire()
                self.cooldown = 1
                Clock.schedule_once(self.update_cooldown, 1)  # Set cooldown before next fire
        
        # KEYS FOR BULLETS
        elif key == 'i':  # Change bullet type to standard bullet
            self.current_bullet = 'bullet'
        elif key == 'o':  # Change bullet type to bombshell
            self.current_bullet = 'bombshell'
        elif key == 'p':  # Change bullet type to laser
            self.current_bullet = 'laser'
        
        # KEYS FOR MOVEMENT
        elif key == 'd':  # Move right (rotate clockwise)
            self.keysPressed.add("d")
        elif key == 'a':  # Move left (rotate counterclockwise)
            self.keysPressed.add("a")
        return True

    def _on_key_up(self, keyboard, keycode):
        # Handles key release events (stopping movement)
        key = keycode[1]
        if key == 'd':
            self.keysPressed.discard("d")  # Stop moving right
        elif key == 'a':
            self.keysPressed.discard("a")  # Stop moving left
        return True

    def _on_keyboard_closed(self):
        # Cleanup when the keyboard input is closed
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)
            self._keyboard = None
