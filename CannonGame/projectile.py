from kivy.uix.widget import Widget
from kivy.graphics.vertex_instructions import Rectangle, Ellipse
from kivy.graphics import PushMatrix, PopMatrix, Rotate
from kivy.clock import Clock
import math

# Base class for all projectiles
class Projectile(Widget):
    def __init__(self, pos, x_velocity, y_velocity, **kwargs):
        super().__init__(**kwargs)
        self.pos = pos # Initial position of the projectile
        self.x_velocity = float(x_velocity)  # X-axis velocity
        self.y_velocity = float(y_velocity)  # Y-axis velocity
        self.time_step= 1 / 60.0  # Time step for the clock to update
        self.pause = False  # To pause projectile movement when necessary

    # Method to update projectile position based on velocity and gravity
    def update_position(self, dt):
        if not self.parent: # If there's no parent, exit
            return
        if not self.pause: # Proceed only if not paused
            # Update position based on velocity and gravity
            self.x += float(self.x_velocity) * dt
            self.y += float(self.y_velocity) * dt + 0.5 * self.gravity * dt ** 2
            self.y_velocity += float(self.gravity) * dt  # Gravity affects y velocity

            # Calculate angle based on velocity direction
            angle = math.degrees(math.atan2(self.y_velocity, self.x_velocity))

            # Update the position of the projectile (ellipse shape)
            self.circle.pos = (self.x, self.y)
            
            if isinstance(self, Bombshell):
                # If projectile is a Bombshell, apply rotation
                with self.canvas:
                    self.canvas.clear()  # Pulisci il canvas precedente
                    PushMatrix()
                    Rotate(origin=(self.center_x, self.center_y), angle=angle, axis=(0, 0, 1)) # Apply rotation
                    Ellipse(pos=self.circle.pos, size=self.size, source=r"assets\images\objects\bomba.png") # Redraw
                    PopMatrix()


            if isinstance(self, Laser):
                # If projectile is a Laser, apply rotation
                with self.canvas:
                    self.canvas.clear()  # Clear previous canvas
                    PushMatrix()
                    Rotate(origin=(self.center_x, self.center_y), angle=angle, axis=(0, 0, 1)) # Apply rotation
                    # Disegna l'immagine del proiettile
                    Ellipse(pos=self.circle.pos, size=self.size, source=r"assets\images\objects\cerchio_rosso.png") # Redraw
                    PopMatrix()

            # Check if the projectile hits the ground, goes off-screen, or collides with terrain
            if (self.y <= 0 or self.x >= self.parent.width or self.x <= 0 or
                self.y >= self.parent.height or self.collide_widget(self.parent.ids["terrain"])):
                self.parent.projectiles.remove(self) # Remove from projectile list
                self.parent.remove_widget(self) # Remove from the screen



# Bullet class, inherits from Projectile
class Bullet(Projectile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (20, 20) # Bullet size
        self.gravity = -200 # Gravity affecting the bullet's y velocity

        # Draw the bullet as an ellipse
        with self.canvas:
            self.circle = Ellipse(pos = self.pos, size = self.size, source= r"assets\images\objects\bullet.png")

        # Schedule position updates using Kivy's clock
        Clock.schedule_interval(self.update_position, self.time_step)

# Bombshell class, inherits from Projectile
class Bombshell(Projectile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 2300x821
        self.size = (80,35)
        self.gravity = -100

        with self.canvas:
            self.circle = Rectangle(pos = self.pos, size = self.size, source= r"assets\images\objects\bomba.png")

        # Schedule position updates
        Clock.schedule_interval(self.update_position, self.time_step)

    # Method to spawn mini bullets after the bombshell explodes
    def mini_bullets(self, pos):
        # Create mini bullets in 8 directions (0 to 360 degrees)
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            r = 70 # Distance from the bombshell center
            new_x = pos[0] + r*math.cos(angle) # New x-coordinate
            new_y = pos[1] + r*math.sin(angle) # New y-coordinate
            
            speed = 200 # Speed of the mini bullets
            x_velocity = speed*math.cos(angle)
            y_velocity = speed*math.sin(angle)

            # Create a new Bullet instance for each mini bullet
            mini_bullet = Bullet(pos = (new_x,new_y) , x_velocity = x_velocity, y_velocity = y_velocity)
            self.parent.add_widget(mini_bullet)  # Add mini bullet to the parent
            self.parent.projectiles.append(mini_bullet) # Add to the projectiles list

# Laser class, inherits from Projectile
class Laser(Projectile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (80,8)
        self.gravity = 0 # Lasers are unaffected by gravity

        with self.canvas:
            self.circle = Ellipse(pos = self.pos, size = self.size, source = r"assets\images\objects\cerchio_rosso.png")

        # Schedule position updates
        Clock.schedule_interval(self.update_position, self.time_step)
                
    # Method to reflect the laser horizontally
    def reflect_laser1(self):
        self.x_velocity = - self.x_velocity

    # Method to reflect the laser vertically
    def reflect_laser2(self):
        self.y_velocity = - self.y_velocity
