import arcade  # Importing modules
import math
import time
import random


# I started this before I knew we had to keep backups, so this is a reconstruction of what my code would have looked like at this point


SCREEN_WIDTH = 1080  # Setting constants
SCREEN_HEIGHT = 720


class Planet:  # Planet class is the class that handles what is happeneing on each planet eg death, breeding, orbiting, food loss etc.
    def __init__(self, orbit_speed, radius, distance, planet_id, max_sprn, rot_spd, width, height, strt_wdth, strt_hght, max_width, max_hght):
        self.orbit_speed = orbit_speed  # This is what controls how fast each Planet object is orbiting at
        self.radius = radius  # The radius of each Planet object
        self.distance = distance  # The distance from the center each planet is orbiting at
        self.id = planet_id  # The unique id for each object to be used for getting info specific for that planet
        self.max_sprn = max_sprn  # Max sprite number becuase each object has a different number of sprites
        self.rot_spd = rot_spd  # The speed at which the sprites are being changed
        self.x = 0  # X position of each object to be used for the ship
        self.y = 0  # Y position of each object to be used for the ship


    def draw(self):
        if Ship.landed is None:  # Tests if the game state means the ship is orbiting
            arcade.draw_circle_outline(540, 360, self.distance, arcade.color.GRAY, 2)  # draws the orbit circle for the planet

            arcade.draw_circle_filled(self.x, self.y, self.size, arcade.color.WHITE)
        else:
            arcade.draw_texture_rectangle(540, 425, 670, 500, arcade.load_texture("sprites/gui/" + Planet.name[Ship.landed.id] + "land.png"))  # Draws the planet in the landed state

    def update(self):
        if Ship.landed is None:  # Tests if the game state means the ship is orbiting
            Planet.theta[self.id] = 0

            Planet.theta[self.id] += self.orbit_speed  # Changes the theta value, which is what gets the planet drawn in the right position, by whatever the speed of the planet orbiting is
            Planet.angle[self.id] = math.radians(Planet.theta[self.id])  # Changes the value to radians so it can be used

            self.x = (math.sin(Planet.angle[self.id]) * self.distance) + 540  # Sets the x and y value to points relative to the center but offset by a certain degree to make the planets orbit
            self.y = (math.cos(Planet.angle[self.id]) * self.distance) + 360


class Ship:  # Class for the ship and handles the current planet that is landed
    def __init__(self, size, state, target, orbiting, x, y):
        self.size = size  # Sets the size of the ship so that it can get smaller when landing for cool animations
        self.state = state  # If the ship is orbiting, transit, or landed
        self.target = target  # Where the ship is going to
        self.orbiting = orbiting  # What is being orbited
        self.x = x  # x pos
        self.y = y  # y pos

    def draw(self):
        if Ship.landed is None:
            arcade.draw_circle_outline(self.orbiting.x, self.orbiting.y, self.orbiting.radius * 2.5, arcade.color.GRAY, 2)  # Draws outline for orbit circle
            if self.state == 'orbiting':
                arcade.draw_circle_filled(self.x, self.y, 10, arcade.color.GRAY)  # Draws ship
            elif self.state == "transit":
                if self.size > 0.7:  # if the ship is below a certain size
                    arcade.draw_circle_filled(self.x, self.y, self.size, arcade.color.GRAY)  # Draws ship
                else:
                    arcade.draw_line(self.orbiting.x, self.orbiting.y, self.target.x, self.target.y, arcade.color.WHITE)  # Draws transit line

    def update(self):
        if self.state != 'land':
            if self.state == "orbiting":
                if Planet.theta[0] == 360:
                    Planet.theta[0] = 0  # controls rotation

                Planet.theta[0] += 2  # changes speed of rotation
                Planet.angle[0] = math.radians(Planet.theta[0])  # Changes into radians to be used by arcade

            elif self.state == "transit":
                if self.size > 0.7:
                    self.size /= 1.25  # Changes size for cool animation when transiting
                else:
                    self.size = 10  # resets size
                    self.orbiting = self.target  # sets the orbiting to target to change state

            self.x = (math.sin(Planet.angle[0]) * (self.orbiting.radius * 2.5)) + self.orbiting.x  # sets x for orbit
            self.y = (math.cos(Planet.angle[0]) * (self.orbiting.radius * 2.5)) + self.orbiting.y  # sets y for orbit

            if self.orbiting != self.target:  # sees if the ship should be in transit or orbiting
                self.state = "transit"
            else:
                self.state = "orbiting"


class MyGame(arcade.Window):  # class built into arcade where THE MAGIC HAPPENS
    def __init__(self, width, height, title):
        super().__init__(width, height, title)  # opens window

        self.ship = Ship(10, 'orbiting', terra, terra, 0, 0)  # creates ship object


        self.planets = [skei, terra, morp, cronus, altzeira]  # creates a list of all planets to loop through all planet objects later
        self.planet_list = []  # creates a list of planets so that all objects can be updated and drawn
        self.planet_orbiting = 0  # This is what shows what planet is currently being orbited

        for item in self.planets:  # gets all of the planets into another list which can be used for another reason
            self.planet_list.append(item)

    def update(self, delta_time):

        Planet.state = self.ship.state  # ensures all states of the game is equal to avoid errors
        for planet in self.planet_list:  # updates all planet objects
            planet.update()
        self.ship.update()  # updates the ship


    def on_draw(self):
        arcade.start_render()  # begins the rendering
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.load_texture("sprites/gui/background.png"))  # draws the background
        for planet in self.planet_list:  # updates all planet objects to draw
            planet.draw()
        self.ship.draw()  # runs the draw function in ship
        draw_gui()  # draws the gui
        if self.draw != '':  # tests if any dropdown is already selected
            arcade.draw_texture_rectangle(self.mousex + 220, self.mousey - 100, 150, 200,arcade.load_texture(self.draw))  # draws the dropdown
        if self.mousex != 0:  # tests if the player has deselected the dropdown
            draw_dropdown(self.mousex, self.mousey, 0, 0)  # draws the dropdown at the location of players mouse
        self.resource = [self.housing, self.population, self.food, self.minerals, self.pollution]  # gathers all of the global resources into a list
            self.ph += 1  # changes the placeholder by one to change the position of the text being drawn

    def on_key_press(self, key, modifiers):  # testing all key presses for game
        if self.ship.state == 'orbiting':  # making sure the game is in the correct state
            if key == arcade.key.A or key == arcade.key.W:  # tests what key is pressed and changes what planet is being orbited by the ship
                self.planet_orbiting += 1

            if key == arcade.key.D or key == arcade.key.S:  # tests what key is pressed and changes what planet is being orbited by the ship
                self.planet_orbiting -= 1

            if self.planet_orbiting == 5:  # makes sure the planet orbiting is within range and if not changes it to within range
                self.planet_orbiting = 0
            elif self.planet_orbiting == -1:
                self.planet_orbiting = 4

            self.ship.target = self.planets[self.planet_orbiting]  # makes sure the ship is targeting the correct planet

        if key == arcade.key.SPACE:  # tests if the space key is down
            if self.ship.state == 'land':  # tests if the ship is in state land and if not goes into state land
                if self.mousex != 0:  # tests if dropdown is currently selected, and if it is, deselects dropdown, otherwise exists land state and goes back to orbiting
                    self.mousex = 0
                    self.draw = ''
                else:
                    self.ship.orbiting = Ship.landed
                    self.ship.target = Ship.landed
                    Ship.landed = None
                    self.ship.state = 'orbiting'
            else:
                Ship.landed = self.ship.orbiting
                self.ship.state = 'land'

        if Ship.landed is not None:  # if the landed state is current state
            if key == arcade.key.ESCAPE:  # if escape key down
                if self.mousex != 0:  # tests if dropdown active and if it is exits dropdown, otherwise exists land state
                    self.mousex = 0
                    self.draw = ''
                else:
                    Ship.landed = None
                    self.ship.state = 'orbiting'


def draw_gui():  # draws most of the gui for the game
    arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.load_texture("sprites/gui/guimain.png"))  # draws main GUI (bars left and right)
    if Ship.landed is not None:  # tests if game state is landed
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.load_texture("sprites/gui/guiaddon.png"))  # adds bottom ui element
   


# creates all planet objects
skei = Planet(0.35, 7.5, 100, 1, 19.4, 0.05, 4, 3, 330, 500, 750, 265)
terra = Planet(0.2, 15, 150, 2, 19.4, 0.1, 5, 4, 330, 500, 850, 190)
morp = Planet(0.3, 10, 225, 3, 19.4, 0.075, 4, 4, 330, 500, 750, 185)
cronus = Planet(0.15, 20, 275, 4, 29.4, 0.05, 6, 5, 225, 580, 850, 190)
altzeira = Planet(0.1, 6, 325, 5, 19.4, 0.075, 4, 3, 330, 500, 750, 265)


# creates Class variables
Planet.angle = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # creates an angle amount for each object to control speed of orbit
Planet.theta = [0, 0, 45, 90, 120, 200]  # uses Planet.angle to do the orbit of each object
Planet.name = ['', 'Skei', 'Terra', 'Morp', 'Cronus', 'Altzeira']  # stores names of planets for use in sprites and text
Planet.names = [skei, terra, morp, cronus, altzeira]  # stores all planet objects to use for calculating resources
Ship.landed = None  # sets main state for the game to orbiting


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, 'test')  # does magic or something honestly I'm not too sure

    arcade.run()  # runs arcade


main()  # Calls main...

