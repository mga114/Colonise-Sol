import arcade  # Importing modules
import math
import time
import random


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
        self.planet_sprite_list = None  # This is used as an arcade.sprite() list and is used to change the sprites of objects
        self.planet_sprite = None  # Used as a placeholder during the transition phase for self.planet_sprite_list
        self.sprite_file_location = ""  # Where the sprites are in the directory
        self.grid = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Each planets grid system where each item is a tile
        self.draw_pos_on_planet = []  # Used to get data about a certain value in self.grid
        self.width = width  # Tile based width of the planet
        self.height = height  # Tile based height of the planet
        self.strt_wdth = strt_wdth  # Where the first tile is on the planet in terms of x
        self.strt_hght = strt_hght  # Where the first tile is on the planet in terms of y
        self.max_width = max_width  # Where the last tile is on the planet in terms of x
        self.max_hght = max_hght  # Where the last tile is on the planet in terms of y
        self.housing = [0, 0]  # Resources for each specific planet where item 0 is the gain and 1 is the amount required
        self.food = [0, 0]
        self.minerals = [0, 0]
        self.energy = [0, 0]
        self.water = [0, 0]
        self.pollution = [0, 0]
        self.population = [0, 0]
        if self.id == 2:  # This tests if the object is Terra, which already has buildings on
            self.grid = [0, 0, 0, 0, 0, 0, 0, 1, 4, 3, 2, 1, 0, 3, 2, 5, 3, 1, 0, 6, 5, 4, 2, 2, 0, 1, 6, 1, 5, 5]  # Sets Terras grid
            self.population[0] = 50  # Sets Terras appropriate resources
            self.population[1] = 50
            self.housing[0] = 50
            self.housing[1] = 50
            self.food[0] = 150
            self.food[1] = 150
            self.water[0] = 75
            self.water[1] = 70
            self.minerals[0] = 60
            self.minerals[1] = 58
            self.energy[0] = 40
            self.energy[1] = 39
            self.pollution[0] = 400
            self.pollution[1] = 460
        self.time = 0  # Used to time certain things such as Resettlement or research

    def setup(self):
        self.planet_sprite_list = arcade.SpriteList()  # Sets this pre-defined list to be a SpriteList so that sprites can be drawn easily

    def draw(self):
        if Ship.landed is None:  # Tests if the game state means the ship is orbiting
            arcade.draw_circle_outline(540, 360, self.distance, arcade.color.GRAY, 2)  # draws the orbit circle for the planet

            self.planet_sprite_list.draw()  # draws the sprites for the object
        else:
            arcade.draw_texture_rectangle(540, 425, 670, 500, arcade.load_texture("sprites/gui/" + Planet.name[Ship.landed.id] + "land.png"))  # Draws the planet in the landed state

    def update(self):
        if Ship.landed is None:  # Tests if the game state means the ship is orbiting
            self.planet_sprite_list = arcade.SpriteList()  # Sets this pre-defined list to be a SpriteList so that sprites can be drawn easily

            for i in self.planet_sprite_list:  # Loops through self.planet_sprite_list
                self.planet_sprite_list.pop()  # Deletes old items in list that aren't being used

            if Planet.theta[self.id] == 360:  # Tests to see if the value is above a certain point, and if it is, resets it
                Planet.theta[self.id] = 0

            Planet.theta[self.id] += self.orbit_speed  # Changes the theta value, which is what gets the planet drawn in the right position, by whatever the speed of the planet orbiting is
            Planet.angle[self.id] = math.radians(Planet.theta[self.id])  # Changes the value to radians so it can be used

            self.x = (math.sin(Planet.angle[self.id]) * self.distance) + 540  # Sets the x and y value to points relative to the center but offset by a certain degree to make the planets orbit
            self.y = (math.cos(Planet.angle[self.id]) * self.distance) + 360

            if Planet.costume_number[self.id] >= self.max_sprn:  # Tests if the sprite number is too high which would cause an error
                Planet.costume_number[self.id] = 0.5  # Resets the sprite number so the 'animation' can loop
            Planet.costume_number[self.id] += self.rot_spd  # Changes the costume number by a certain amount

            self.sprite_file_location = '{0}/{1}'.format(Planet.name[self.id], int(round(Planet.costume_number[self.id])))  # Finds where the sprites for this object is and which sprite should be drawn
            self.planet_sprite = arcade.Sprite('sprites/{0}.png'.format(self.sprite_file_location), 0.5)  # Sets most of the values for drawing the sprite into a variable
            self.planet_sprite.center_x = self.x  # Sets where the x and y of the sprite should be drawn
            self.planet_sprite.center_y = self.y
            self.planet_sprite_list.append(self.planet_sprite)  # Adds the info from earlier into the SpriteList

        if self.time <= time.time() and self.time != 0:  # Controls the timing for resettlements and research by using time module and the self.time value set in the MyGame class
            i = 0  # Creates a placeholder variable which finds which position in the list self.grid the tile needed is
            for item in self.grid:  # Loops for every item in the grid
                if item == 7.5:  # 7.5 is the value given for resettlements that are under contstruction
                    self.population[0] += 10  # Changes all of the resources as needed
                    self.housing[0] += 10
                    self.minerals[0] += 10
                    self.energy[0] += 10
                    self.food[0] += 30
                    self.food[1] += 30
                    self.housing[1] += 10
                    self.pollution[1] += 20
                    self.water[0] += 30
                    self.grid[i] = 7  # Changes the sprite for the resettlement to the complete structure
                elif item > 7.5:  # Anything greater that 7.5 is research
                    self.population[0] += 2  # Changes the resources accordingly
                    self.energy[0] += 1
                    self.grid[i] = 0  # Removes the research sprite from the tile
                i += 1  # changes the placeholder variable by 1
            self.time = 0  # resets the time so that other contstruction can take place

        if (self.pollution[0] - self.pollution[1]) >= 0:  # Tests if pollution is above what is needed
            if random.randrange(0.0,  200.0) < self.population[0]/50:  # Randomly chooses a number which gets larger as population increases to see if population breeds
                self.population[0] += 1  # changes resources becuase 1 population added
                self.pollution[1] += 2
                self.food[1] += 3
                self.housing[1] += 1
        elif (self.pollution[0] - self.pollution[1]) < 0:  # Tests if pollution is below what is needed
            if random.randrange(0.0, 150.0) < self.population[0]/50:  # # Randomly chooses a number which gets larger as population increases to see if population dies
                self.population[0] -= 1  # changes resources becuase 1 population dies
                self.food[1] -= 2
                self.housing[1] -= 1

        if self.housing[0] - self.housing[1] < 0:  # tests if housing is below required
            if random.randrange(0.0, 400.0) < self.housing[0] / 50:  # Randomly chooses a number which gets larger as population increases to see if population dies
                self.energy[1] += 1  # changes resources becuase 1 population dies
                self.pollution[1] += 2
                self.food[1] += 1
                self.population[0] -= 1

        if (self.food[0] - self.food[1]) >= 0:  # tests if food is above required
            if random.randrange(0.0, 200.0) < self.population[0] / 50:  # Randomly chooses a number which gets larger as population increases to see if population breeds
                self.population[0] += 1   # changes resources becuase 1 population added
                self.pollution[1] += 2
                self.food[1] += 3
                self.housing[1] += 1
        elif (self.food[0] - self.food[1]) < 0:  # tests if food is below required
            if random.randrange(0.0, 100.0) < self.population[0] / 50:  # Randomly chooses a number which gets larger as population increases to see if population dies
                self.population[0] -= 1  # changes resources because 1 population dies
                self.food[1] -= 2
                self.housing[1] -= 1
                self.pollution[1] -= 2


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

        self.dor_sprite = None  # creates variables for drawing sprites for Dor
        self.dor_list = None
        self.costume = 0.5

        self.planets = [skei, terra, morp, cronus, altzeira]  # creates a list of all planets to loop through all planet objects later
        self.planet_list = []  # creates a list of planets so that all objects can be updated and drawn
        self.planet_orbiting = 0  # This is what shows what planet is currently being orbited

        for item in self.planets:  # gets all of the planets into another list which can be used for another reason
            self.planet_list.append(item)

        self.tile_len = 0  # length of tile for use when landed on the planet to detect which tile has been clicked
        self.tile_hgt = 0  # height of tile for use when landed on the planet to detect which tile has been clicked
        self.tile_clicked_wid = 0  # variable used to see where the mouse has been clicked relative to the grid in terms of x
        self.tile_clicked_hgt = 0  # variable used to see where the mouse has been clicked relative to the grid in terms of y
        self.mousex = 0  # variable to check with x value for testing which tile is clicked
        self.mousey = 0  # variable to check with y value for testing which tile is clicked
        self.tempx = 0  # temp variable that checks the tile clicked for x
        self.tempy = 0  # temp variable that checks the tile clicked for y
        self.draw = ''  # used to see what needs to be drawn on the GUI

        self.housing = [0, 0]  # creating lists to hold global resources
        self.population = [0, 0]
        self.food = [0, 0]
        self.minerals = [0, 0]
        self.pollution = [0, 0]
        self.i = 0  # placeholder variable
        self.ph = 0  # placeholder variable
        self.resource = []  # list which contains all variables

    def setup(self):
        self.dor_list = arcade.SpriteList()  # turns self.dor_list into a SpriteList so sprites are easier to draw

    def update(self, delta_time):
        self.dor_list = arcade.SpriteList()  # turns self.dor_list into a SpriteList so sprites are easier to draw

        for i in self.dor_list:  # empties uneeded values from self.dor_list
            self.dor_list.pop()

        if self.costume >= 39.4:  # makes sure the costume for Dor is within range and resets it
            self.costume = 0.5

        self.costume += 0.025  # changes Dor sprite by small amount

        self.dor_sprite = arcade.Sprite("sprites/Dor/{0}.png".format(str(round(self.costume))), 0.5)  # sets Dor sprite file location and size
        self.dor_sprite.center_x = 544  # sets dor sprite x and y positions
        self.dor_sprite.center_y = 360
        self.dor_list.append(self.dor_sprite)  # adds dor sprite to the SpriteList to be drawn

        Planet.state = self.ship.state  # ensures all states of the game is equal to avoid errors
        for planet in self.planet_list:  # updates all planet objects
            planet.update()
        self.ship.update()  # updates the ship

        self.housing = [0, 0]  # resets global resources
        self.population = [0, 0]
        self.food = [0, 0]
        self.minerals = [0, 0]
        self.pollution = [0, 0]

        self.i = 0  # resets placeholder variable
        while self.i <= 1:  # calculates global resources
            for planet in Planet.names:
                self.housing[self.i] += planet.housing[self.i]
                self.population[self.i] += planet.population[self.i]
                self.food[self.i] += planet.food[self.i]
                self.minerals[self.i] += planet.minerals[self.i]
                self.pollution[self.i] += planet.pollution[self.i]
            self.i += 1
        if self.population[0] - self.population[1] < -75:  # tests for end game scenario
            self.win = False
        elif self.population[0] - self.population[1] > 75:
            self.win = True

    def on_draw(self):
        arcade.start_render()  # begins the rendering
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.load_texture("sprites/gui/background.png"))  # draws the background
        for planet in self.planet_list:  # updates all planet objects to draw
            planet.draw()
        self.ship.draw()  # runs the draw function in ship
        if Ship.landed is None:  # tests if the game is in state landed or orbit
            self.dor_list.draw()  # draws the sun
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

    def on_mouse_motion(self, x, y, dx, dy):  # checks for mouse movement which controls extended dropdown in build improvement and research
        if Ship.landed is not None and self.mousex != 0 and (self.mousex + 150) > x > self.mousex:  # sees where the mouse is and if the dropdown is still selected
            if (self.mousey - 50) < y < self.mousey:  # tests where mouse is and if in correct spot draw improve.png
                self.draw = 'sprites/gui/improve.png'  # gives self.draw a value which will be drawn in OnDraw method
            elif (self.mousey - 100) < y < (self.mousey - 50):  # tests where mouse is and if in correct spot draw learn.png
                self.draw = 'sprites/gui/learn.png'  # gives self.draw a value which will be drawn in OnDraw method
            else:
                self.draw = ''  # resets self.draw

    def on_mouse_press(self, x, y, button, modifiers):
        if Ship.landed is not None:  # makes sure game is in state landed
            if self.mousex != 0 and (self.mousex + 150) > x > self.mousex and (self.mousey - 200) < y < self.mousey:  # checks for the correct position of the mouse for the dropdown
                if (self.mousey - 150) <= y <= (self.mousey - 100) and Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] != 0:  # makes sure the tile is not empty (clearing tiles)
                    tile = Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid]  # sets a temporary variable to the tile info to save room
                    if tile < 7:  # makes sure the tile is only located in the 6 build improvement categories
                        if tile == 1:  # tests what the tile is and removes the correct amount of resource
                            Ship.landed.housing[0] -= 10
                        elif tile == 2:
                            Ship.landed.minerals[0] -= 15
                        elif tile == 3:
                            Ship.landed.water[0] -= 25
                        elif tile == 4:
                            Ship.landed.food[0] -= 75
                        elif tile == 5:
                            Ship.landed.energy[0] -= 10
                        elif tile == 6:
                            Ship.landed.pollution[0] -= 200
                        Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 0  # resets the tile to 0
                        Ship.landed.pollution[1] += 30  # adds pollution
                elif (self.mousey - 200) <= y <= (self.mousey - 150) and Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] == 0:  # tests if the mouse is within the range for building resettlement
                    result = False  # resets variabele
                    result = all(elem == Ship.landed.grid[0] for elem in Ship.landed.grid)  # tests if all values in grid are 0
                    if result:  # if all values are 0
                        Ship.landed.time = time.time() + 30  # sets a timer for 30 seconds
                        Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 7.5  # sets sprite for that tile to be the resettlement in construction
                    elif self.food[0] - self.food[1] >= 30 or Ship.landed.food[0] - Ship.landed.food[1] >= 30:  # if the planet is not empty test if the resources availabe are enough for resettlement
                        Ship.landed.time = time.time() + 30  # sets timer for 30 seconds
                        Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 7.5  # sets sprite for that tile to be the resettlement in construction
            else:
                if self.draw != '' and (self.mousex + 300) > x > (self.mousex + 150) and (self.mousey - 200) < y < self.mousey and Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] == 0 and Ship.landed.time == 0:  # check position and conditions for building
                    if self.draw == 'sprites/gui/improve.png':  # testing what menu the player has selected
                        if(self.minerals[0] - self.minerals[1] >= 2 or Ship.landed.minerals[0] - Ship.landed.minerals[1] >= 2) and Ship.landed.energy[0] - Ship.landed.energy[1] >= 0.5:  # testing resource conditions for buildings
                            if (self.mousex + 225) > x > (self.mousex + 150):  # testing what button has been pressed (x)
                                if (self.mousey - 66) < y < self.mousey:  # testing what button has been pressed (y)
                                    if Ship.landed.energy[0] - Ship.landed.energy[1] >= 3.5 and Ship.landed.water[0] - Ship.landed.water[1] >= 10:  # making sure resources are ok
                                        Ship.landed.energy[1] += 3.5  # changing resources accordingly
                                        Ship.landed.population[1] += 1
                                        Ship.landed.minerals[1] += 2
                                        Ship.landed.water[1] += 10
                                        Ship.landed.housing[0] += 10
                                        Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 1  # changing tile in grid (housing)
                                elif (self.mousey - 130) < y < (self.mousey - 66):
                                    if Ship.landed.energy[0] - Ship.landed.energy[1] >= 2.5:
                                        Ship.landed.population[1] += 6
                                        Ship.landed.energy[1] += 2.5
                                        Ship.landed.minerals[1] += 2
                                        Ship.landed.minerals[0] += 15
                                        Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 2  # minerals
                                elif(self.mousey - 198) < y < (self.mousey - 130):
                                    if (self.minerals[0] - self.minerals[1] >= 4 or Ship.landed.minerals[0] - Ship.landed.minerals[1] >= 4) and Ship.landed.energy[0] - Ship.landed.energy[1] >= 2.5:
                                        Ship.landed.minerals[1] += 4
                                        Ship.landed.energy[1] += 2.5
                                        Ship.landed.population[1] += 1
                                        Ship.landed.water[0] += 25
                                        Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 3  # water
                            else:
                                if (self.mousey - 66) < y < self.mousey:
                                    if self.minerals[0] - self.minerals[1] >= 5 or Ship.landed.minerals[0] - Ship.landed.minerals[1] >= 5:
                                        Ship.landed.minerals[1] += 5
                                        Ship.landed.population[1] += 1
                                        Ship.landed.energy[1] += 0.5
                                        Ship.landed.pollution[1] += 30
                                        Ship.landed.food[0] += 75
                                        Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 4  # food
                                elif (self.mousey - 130) < y < (self.mousey - 66):
                                    if Ship.landed.water[0] - Ship.landed.water[1] >= 5:
                                        Ship.landed.minerals[1] += 2
                                        Ship.landed.population[1] += 1
                                        Ship.landed.energy[1] += 0.5
                                        Ship.landed.water[1] += 5
                                        Ship.landed.pollution[1] += 75
                                        Ship.landed.energy[0] += 10
                                        Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 5  # energy
                                elif(self.mousey - 198) < y < (self.mousey - 130):
                                    if self.minerals[0] - self.minerals[1] >= 5 or Ship.landed.minerals[0] - Ship.landed.minerals[1] >= 5:
                                        Ship.landed.minerals[1] += 5
                                        Ship.landed.population[1] += 6
                                        Ship.landed.energy[1] += 0.5
                                        Ship.landed.pollution[0] += 200
                                        Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 6  # pollution
                    elif self.population[0] - self.population[1] >= 2 and Ship.landed.energy[0] - Ship.landed.energy[1] >= 1:  # testing resources for research
                        if (self.mousex + 225) > x > (self.mousex + 150):  # testing which button has been pressed (x)
                            if (self.mousey - 66) < y < self.mousey:  # testing which button has been pressed (y)
                                if self.minerals[0] - self.minerals[1] >= 50:  # testing to see if resource requirements are met
                                    Ship.landed.minerals[1] += 50  # reducing resources accordingly
                                    Ship.landed.population[1] += 2
                                    Ship.landed.energy[1] += 1
                                    Ship.landed.time = time.time() + 60  # start 60 second timer
                                    Ship.landed.housing[0] *= 1.15  # increase resource by 15%
                                    Ship.landed.housing[0] = math.ceil(Ship.landed.housing[0])  # round resource up to be displayed better
                                    Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 8  # change tile (housing)
                            elif (self.mousey - 130) < y < (self.mousey - 66):
                                Ship.landed.population[1] += 2
                                Ship.landed.energy[1] += 1
                                Ship.landed.pollution[1] += 200
                                Ship.landed.time = time.time() + 60
                                Ship.landed.minerals[0] *= 1.15
                                Ship.landed.minerals[0] = math.ceil(Ship.landed.minerals[0])
                                Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 9  # minerals
                            elif(self.mousey - 198) < y < (self.mousey - 130):
                                if Ship.landed.energy[0] - Ship.landed.energy[1] >= 51:
                                    Ship.landed.population[1] += 2
                                    Ship.landed.energy[1] += 51
                                    Ship.landed.time = time.time() + 60
                                    Ship.landed.water[0] *= 1.15
                                    Ship.landed.water[0] = math.ceil(Ship.landed.water[0])
                                    Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 10  # water
                        else:
                            if (self.mousey - 66) < y < self.mousey:
                                if Ship.landed.water[0] - Ship.landed.water[1] >= 100:
                                    Ship.landed.population[1] += 2
                                    Ship.landed.energy[1] += 1
                                    Ship.landed.water[1] += 100
                                    Ship.landed.time = time.time() + 60
                                    Ship.landed.food[0] *= 1.15
                                    Ship.landed.food[0] = math.ceil(Ship.landed.food[0])
                                    Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 11  # food
                            elif (self.mousey - 130) < y < (self.mousey - 66):
                                if self.housing[0] - self.housing[1] >= 10:
                                    Ship.landed.population[1] += 2
                                    Ship.landed.energy[1] += 1
                                    Ship.landed.housing[1] += 10
                                    Ship.landed.time = time.time() + 60
                                    Ship.landed.energy[0] *= 1.15
                                    Ship.landed.energy[0] = math.ceil(Ship.landed.energy[0])
                                    Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 12  # energy
                            elif(self.mousey - 198) < y < (self.mousey - 130):
                                if self.food[0] - self.food[1] >= 100:
                                    Ship.landed.population[1] += 2
                                    Ship.landed.energy[1] += 1
                                    Ship.landed.food[1] += 100
                                    Ship.landed.time = time.time() + 60
                                    Ship.landed.pollution[0] *= 1.15
                                    Ship.landed.pollution[0] = math.ceil(Ship.landed.pollution[0])
                                    Ship.landed.grid[(self.tile_clicked_hgt * 6) + self.tile_clicked_wid] = 13  # pollution
                else:
                    if Ship.landed.max_width > x > Ship.landed.strt_wdth and Ship.landed.max_hght < y < Ship.landed.strt_hght:  # testing if the mouse click is within the boundary of the grid
                        self.tile_len = (Ship.landed.max_width - Ship.landed.strt_wdth) / Ship.landed.width  # finding which tile has been clicked (x)
                        self.tile_hgt = (Ship.landed.max_hght - Ship.landed.strt_hght) / Ship.landed.height  # finding which tile has been clicked (y)

                        self.tile_clicked_wid = math.floor((x - 20) / self.tile_len) - 2  # using previous variable to pinpoint location of tile (x)
                        self.tile_clicked_hgt = math.floor((y + 40) / self.tile_hgt) + 8  # using previous variable to pinpoint location of tile (y)

                        self.mousex = x  # storing x and y into variables to be tested against later
                        self.mousey = y
                    else:
                        self.mousex = 0
                        self.draw = ''
            if 700 > x > 383 and 60 > y > 0:  # bottom button in land state return to solar system
                self.ship.orbiting = Ship.landed
                self.ship.target = Ship.landed
                Ship.landed = None
                self.ship.state = 'orbiting'
        if x >= 880 and self.mousex == 0:  # tests for buttons on right side of screen to be pressed
            self.ship.state = 'land'  # sets correct game state
            if 615 > y > 530:  # tests where the mouse click is and changes Ship.landed accordingly
                Ship.landed = skei
            elif 530 > y > 440:
                Ship.landed = terra
            elif 440 > y > 350:
                Ship.landed = morp
            elif 350 > y > 260:
                Ship.landed = cronus
            elif 255 > y > 170:
                Ship.landed = altzeira
            self.ship.orbiting = Ship.landed  # reset variables so no conflicting info
            self.ship.target = Ship.landed
            self.draw = ''


def draw_gui():  # draws most of the gui for the game
    arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.load_texture("sprites/gui/guimain.png"))  # draws main GUI (bars left and right)
    if Ship.landed is not None:  # tests if game state is landed
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.load_texture("sprites/gui/guiaddon.png"))  # adds bottom ui element
        dummy = 0  # resets dummy variable
        drawx = 0  # variables to store proper location for resource buildings
        drawy = 0
        for tile in Ship.landed.grid:  # loops through the entire grid list
            if tile != 0:  # tests if the tile should have something on it
                Ship.landed.draw_pos_on_planet.append(dummy % 6)  # tells draw_pos_on_planet what to draw
                Ship.landed.draw_pos_on_planet.append(math.floor(dummy / 6))  # tells draw_pos_on_planet what to draw
                drawx = ((dummy % 6) * 104) + 280  # converts position in a list into x position
                drawy = 545 - ((math.floor(dummy / 6)) * 80)  # converts position in a list into y position
                if tile == 1:  # tests for what time should be drawn and then draws them
                    arcade.draw_texture_rectangle(drawx, drawy, 75, 75, arcade.load_texture('sprites/gui/housing.png'))
                elif tile == 2:
                    arcade.draw_texture_rectangle(drawx, drawy, 75, 75, arcade.load_texture('sprites/gui/minerals.png'))
                elif tile == 3:
                    arcade.draw_texture_rectangle(drawx, drawy, 50, 75, arcade.load_texture('sprites/gui/water.png'))
                elif tile == 4:
                    arcade.draw_texture_rectangle(drawx, drawy, 75, 75, arcade.load_texture('sprites/gui/food.png'))
                elif tile == 5:
                    arcade.draw_texture_rectangle(drawx, drawy, 75, 75, arcade.load_texture('sprites/gui/energy.png'))
                elif tile == 6:
                    arcade.draw_texture_rectangle(drawx, drawy, 75, 75, arcade.load_texture('sprites/gui/pollution.png'))
                elif tile == 7:
                    arcade.draw_texture_rectangle(drawx, drawy, 75, 75, arcade.load_texture('sprites/gui/colony.png'))
                elif tile == 7.5:
                    arcade.draw_texture_rectangle(drawx, drawy, 75, 75, arcade.load_texture('sprites/gui/colonyconst.png'))
                elif tile > 7.5:  # all above 7.5 are research, which all have 1 sprite
                    arcade.draw_texture_rectangle(drawx, drawy, 50, 75, arcade.load_texture('sprites/gui/research.png'))
            dummy += 1  # increases dummy variable
   

def draw_dropdown(x, y, tempx, tempy):  # draws dropdown for GUI and selected box
    tempx = (math.ceil((x - 20) / 105) * 105) - 37.5  # rounds x to snap tile selected IE to the tile
    tempy = (math.floor((y + 50) / 80) * 80) - 15  # rounds y to snap tile selected IE to the tile
    arcade.draw_texture_rectangle(tempx, tempy, 100, 75, arcade.load_texture('sprites/gui/selecttile.png'))  # draws tile selected IE
    arcade.draw_texture_rectangle(x + 75, y - 100, 150, 200, arcade.load_texture('sprites/gui/uls.png'))  # draws basic dropdown


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
Planet.costume_number = [0, 0.5, 0.5, 0.5, 0.5, 0.5]  # stores object planet costumes to easily change them
Ship.landed = None  # sets main state for the game to orbiting


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, 'test')  # does magic or something honestly I'm not too sure

    arcade.run()  # runs arcade


main()  # Calls main...

