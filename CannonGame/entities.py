from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.graphics.vertex_instructions import Rectangle
from kivy.core.window import Window
import random
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

# Base class for all entities in the game
class Entities(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass

    # Method to handle movement, can be overridden by subclasses
    def move(self):
        pass

    # Method to check if an entity has collided with a bullet
    def check_collision(self, bullet):
        # Checks if bullet's position overlaps with the entity's position
        if (bullet.pos[0] + bullet.size[1] > self.pos[0]) and (bullet.pos[0] < self.pos[0] + self.size[0]) and (bullet.pos[1] < self.pos[1] + self.size[1]) and (bullet.pos[1] + bullet.size[1] > self.pos[1]):
            return True
        return False
    
    # Updates the position and size of the rectangle representing the entity
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size



# Glass entity which reflects laser projectiles
class Glass(Entities):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.rect = Rectangle(source="assets\\images\\bluebackground.jpg", pos=self.pos, size=self.size)
        # Update the rectangle whenever the entity's position or size changes
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    # Handles laser collision to reflect it in different directions
    def on_collision(self, bullet):
        if bullet.__class__.__name__ == "Laser":
            if self.size[0] > self.size[1]:
                bullet.reflect_laser2() # Horizontal reflection
            else:
                bullet.reflect_laser1() # Vertical reflection



# Base class for obstacles
class Obstacle(Entities):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pass
    
    # Placeholder for collision logic to be defined by subclasses
    def on_collision(self, bullet):
        pass

# Obstacle type: Plane
class Plane(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.rect = Rectangle(source=r"assets\images\objects\plane_boss.png", pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

# Ground obstacle entity
class Ground(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
                
        with self.canvas:
            self.rect = Rectangle(source="assets/images/ground/ground_level_2.png", pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

# Horizontal moving block entity
class Block_horiz(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set horizontal velocity for movement
        self.velocity = Vector(3, 0)

        with self.canvas:
            self.rect = Rectangle(source="assets/images/ground/ground_level_2.png", pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Moves the block and bounces it when hitting screen edges
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        # Invert velocity when hitting screen boundaries
        if self.pos[0] > Window.width - self.width:
            self.velocity[0] = -self.velocity[0]
        if self.pos[0] < 0:
            self.velocity[0] = -self.velocity[0]

# Another horizontal block, with different movement limits
class Block_horiz_2(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity = Vector(3, 0)
       
        with self.canvas:
            self.rect = Rectangle(source="assets/images/ground/ground_level_2.png", pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        # Invert velocity within specific horizontal limits
        if self.pos[0] > Window.width - self.width:
            self.velocity[0] = -self.velocity[0]
        if self.pos[0] < 900:
            self.velocity[0] = -self.velocity[0]

# Vertical moving block
class Block_vert(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity = Vector(0, 3)

        with self.canvas:
            self.rect = Rectangle(source="assets/images/ground/ground_level_2.png", pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Moves the block and bounces when hitting vertical screen edges
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        # Invert velocity when hitting screen boundaries
        if self.pos[1] > Window.height - 50:
            self.velocity[1] = -self.velocity[1]
        if self.pos[1] < 200:
            self.velocity[1] = -self.velocity[1]

# Jet entity (moves vertically)
class Jet(Obstacle):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity = Vector(0, 6)

        with self.canvas:
            self.rect = Rectangle(source=r"assets\images\characters\jet.png", pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Moves the jet vertically, bouncing at specific vertical limits
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

        if self.pos[1] > Window.height - 100:
            self.velocity[1] = -self.velocity[1]
        if self.pos[1] < 150:
            self.velocity[1] = -self.velocity[1]



# Base enemy class
class Enemy(Entities):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = 0 # Enemy's score value
        self.collide_terrain = False #  the tracks collision with terrain  
        self.explosion = None
        # Load explosion sound
        self.explosion_sound = SoundLoader.load("assets/sounds/explosion.wav")

    # Handles what happens on bullet collision
    def on_collision(self, bullet):
        self.create_explosion() # Show explosion animation
        self.explosion_sound.play() # Play explosion sound
        # Fades out the enemy and removes it
        fade_anim = Animation(opacity = 0, duration = 0.2)
        fade_anim.bind(on_complete = lambda *args: self.remove_enemy())
        fade_anim.start(self)

    # Creates an explosion graphic for the enemy
    def create_explosion(self):
        self.canvas.clear()
        with self.canvas:
            self.explosion = Rectangle(pos=self.pos, source = r"assets/images/explosion/explosion2.png")

    # Removes the enemy from the game and adjusts the score
    def remove_enemy(self, *args):
        if self.parent:
            if self.collide_terrain:
                self.parent.score -= int(1/2*self.value) # Penalty for terrain collision
            else:
                self.parent.score += self.value # Adds score for successful destruction
            self.parent.entities.remove(self)
            self.parent.remove_widget(self) 

# Sky enemy class, falls from the sky and collides with terrain
class Sky_enemy(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = 10 # Score value for sky enemies
        self.size = (100, 100)
        self.velocity = Vector(0 ,-random.uniform(1,2))  # Falls at random speed
        
        self.canvas.clear()
        with self.canvas:
            self.rect = Rectangle(source="assets/images/objects/bomb.png", pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
 
     # Moves the enemy downward and checks for terrain collision
    def move(self):
        self.pos = self.velocity + self.pos
        # Collision with terrain triggers explosion
        if self.collide_widget(self.parent.ids['terrain']):
            self.collide_terrain = True
            self.on_collision(bullet = None)


# Training mode enemy (falling object)
class Training_falling(Sky_enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 50) # Smaller size for training
        self.canvas.clear()
        with self.canvas:
            self.rect = Rectangle(source="assets/images/objects/crate.png", pos=self.pos, size=self.size)

# Capitan enemy with multiple lives
class Capitan(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.life = 5  # Multiple lives for this enemy
        self.value = 1 # Capitan's point value
    
        self.canvas.clear() # Clear previous graphics
        with self.canvas:
            self.rect = Rectangle(source="assets\images\characters\comandante_nemico.png", pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    # When hit by a bullet, decrease life and check for death
    def on_collision(self, bullet):
        self.life -= 1  # Decrease life
        self.parent.ids['life'].update_life_bar(self.life)  # Update the life bar on the screen
        self.explosion_sound.play() # Play explosion sound
        if self.life == 0: # If life reaches zero, remove the enemy
            self.remove_enemy()

    # Create explosion effect on collision
    def create_explosion(self):
        self.canvas.clear()
        with self.canvas:
            self.explosion = Rectangle(pos=self.pos, source = r"assets/images/explosion/explosion2.png")

# ILBOSS class, representing a powerful enemy with high point value
class ILBOSS(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.life = 1
        self.value = 2000 # High point value for this enemy

        with self.canvas:
            self.canvas.clear()
            self.rect = Rectangle(pos=self.pos, size=self.size, source=r"assets\images\characters\robot_verde.png")
        self.bind(pos=self.update_rect, size=self.update_rect)

    # Create explosion effect
    def create_explosion(self):
        self.canvas.clear()
        with self.canvas:
            self.explosion = Rectangle(pos=self.pos, source = r"assets/images/explosion/explosion2.png")

    # Handle collision with a bullet

    def on_collision(self, bullet):
        self.parent.boss_life -= 1 # Decrease the boss's life
        self.create_explosion()
        self.explosion_sound.play()

        # Fade out the enemy when hit
        fade_anim = Animation(opacity = 0, duration = 0.2)
        fade_anim.bind(on_complete = lambda *args: self.remove_enemy())
        fade_anim.start(self)

# A weaker enemy for training purposes
class Training_Enemy(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 130)

        self.canvas.clear()        
        with self.canvas:
            self.rect = Rectangle(source="assets\images\objects\enemy_prep.png", pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

# Soldier1 enemy class, representing a standard enemy with low point value
class Soldier1(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = 1 # Low point value
        
        self.canvas.clear()
        with self.canvas:
            self.rect = Rectangle(source="assets\\images\\characters\\soldier1.png", pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

# Soldier2 enemy class, similar to Soldier1 but with a different image
class Soldier2(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = 1

        self.canvas.clear()
        with self.canvas:
            self.rect = Rectangle(source="assets\\images\\characters\\soldier2.png", pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

# Soldier3 enemy class, similar to Soldier1 and Soldier2
class Soldier3(Enemy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = 1

        self.canvas.clear()
        with self.canvas:
            self.rect = Rectangle(source="assets\\images\\characters\\soldier3.png", pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)



# Base class for collectable items in the game
class Collectables(Entities):
    def __init__(self, part_tank, **kwargs):
        super().__init__(**kwargs)
        self.collided = False # Track collision state
        self.part_tank = part_tank # Reference to the tank part that collects ammo

    # Handle collision with a bullet
    def on_collision(self, bullet):
        self.part_tank.munizioni += 5  # Increase the tank's ammo count by 5
        fade_anim = Animation(opacity = 0, duration = 0.1) # Fade out the collectable item
        fade_anim.bind(on_complete = lambda *args: self.remove_collectable()) # Remove item after fade-out
        fade_anim.start(self)

    # Remove the collectable from the game
    def remove_collectable(self):
        if self.parent:
            self.parent.entities.remove(self) # Remove from parent entity list
            self.parent.remove_widget(self) # Remove the widget from the game

# AmmoDrop collectable that gives additional ammo to the player
class AmmoDrop(Collectables):
    def __init__(self, part_tank, **kwargs):
        super().__init__(part_tank, **kwargs)
        
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size, source = r"assets\\images\\objects\\ammodrop.png")
        self.bind(pos=self.update_rect, size=self.update_rect)

# AmmoDrop that falls from the sky, moves downward
class AmmoDrop_faling(AmmoDrop):
    def __init__(self, part_tank, **kwargs):
        super().__init__(part_tank, **kwargs)
        self.velocity = Vector(0, -1)  # Fall velocity (downward movement)
        
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos # Update position based on velocity