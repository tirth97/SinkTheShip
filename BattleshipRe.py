from rectanglebutton import *
import random


class Sea_spaces:

    

    def __init__(self, window, player):

        if player == 'human':
            # Create empty list
            self.sea_space_list = []
            # Store window
            self.win = window

            for i in range(27,37):

                for j in range(10):
                    self.sea_space = (RectangleButton(Point((i + 2), j + 2), \
                        1, 1, 'skyblue', False))
                    self.sea_space.draw(window)
                    self.sea_space.activate()
                    self.sea_space_list.append(self.sea_space)
        elif player == 'computer':
            # Create empty list
            self.sea_space_list = []
            # Store window
            self.win = window

            for i in range(10):

                for j in range(10):
                    # Create rectangle button object, draw it, activate it, 
                    #and append it to sea_space_list
                    self.sea_space = (RectangleButton(Point((i + 2), j + 2), \
                        1, 1, 'skyblue', False))
                    self.sea_space.draw(window)
                    self.sea_space.activate()
                    self.sea_space_list.append(self.sea_space)
                


    def get_sea_spaces(self):
        return self.sea_space_list


    def place_ship_computer(self):

        ship_list = []
        
        # Loop over length of ships
        for i in [1, 2, 2, 3, 4]:
            # Create text object
            text = Text(Point(19.5, 8), 'Draw ship of size: ' + str(i+1))
            text.setSize(30)
            text.draw(self.win)
            difference = 0
            first_click = False
            second_click = False

            while difference != i:
                while first_click == False:
                    # Generate random integers in range 2 - 11
                    x = random.randint(2,11)
                    y = random.randint(2,11)

                    p = Point(x, y)

                    first_click = True

                    rand = random.randint(1,2)
                    # If random integer is equal 1 execute if body
                    if rand == 1:

                        if p.getX() + i <= 11:
                            s = p.getX() + i
                            p2 = Point(s, p.getY())
                            second_click = True
                        else:
                            first_click = False
                    
                    # If random integer is not 1 execute else body    
                    else:

                        if p.getY() + i <= 11:
                            d = p.getY() + i
                            p2 = Point(p.getX(), d)
                            second_click = True
                        else:
                            first_click = False


                x1 = int(round(p.getX()))
                y1 = int(round(p.getY()))
                x2 = int(round(p2.getX()))
                y2 = int(round(p2.getY()))
                
                # Calculate difference between x and y coordinates
                difference_x = abs(x1 - x2)
                difference_y = abs(y1 - y2)


                if (difference_x == i) or (difference_y == i):
                    # Create empty list and set difference to be i
                    values = []
                    difference = i

                    if y1 - y2 == 0:
                        if x1 < x2:
                            for x_value in range(x1, x2 + 1):
                                for space in self.sea_space_list:
                                    if space.clicked(Point(x_value, y1)):
                                        values.append(space.get_ship_status())
                            if True in values:
                                difference = 0
                                first_click = False
                                second_click = False
                            else:
                                for x_value in range(x1, x2 + 1):
                                    for space in self.sea_space_list:
                                        if space.clicked(Point(x_value, y1)):
                                            space.update_ship()
                        else:
                            for x_value in range(x2, x1 + 1):
                                for space in self.sea_space_list:
                                    if space.clicked(Point(x_value, y1)):
                                        values.append(space.get_ship_status())
                            if True in values:
                                difference = 0
                                first_click = False
                                second_click = False
                            else:
                                for x_value in range(x2, x1 + 1):
                                    for space in self.sea_space_list:
                                        if space.clicked(Point(x_value, y1)):
                                            space.update_ship()
                    elif x1 - x2 == 0:
                        if y1 < y2:
                            for y_value in range(y1, y2 + 1):
                                for space in self.sea_space_list:
                                    if space.clicked(Point(x1, y_value)):
                                        values.append(space.get_ship_status())
                            if True in values:
                                difference = 0
                                first_click = False
                                second_click = False
                            else:
                                for y_value in range(y1, y2 + 1):
                                    for space in self.sea_space_list:
                                        if space.clicked(Point(x1, y_value)):
                                            space.update_ship()
                        else:
                            for y_value in range(y2, y1 + 1):
                                for space in self.sea_space_list:
                                    if space.clicked(Point(x1, y_value)):
                                        values.append(space.get_ship_status())
                            if True in values:
                                difference = 0
                                first_click = False
                                second_click = False
                            else:
                                for y_value in range(y2, y1 + 1):
                                    for space in self.sea_space_list:
                                        if space.clicked(Point(x1, y_value)):
                                            space.update_ship()
                    else:
                        # Set difference to 0
                        difference = 0
                        first_click = False
                        second_click = False
                
                #If difference between coordinates is not i, execute else body
                else:
                    # Set difference to 0
                    difference = 0
                    first_click = False
                    second_click = False

            text.undraw()                  



    def place_ship(self):
        
        # Create empty list
        ship_list = []
        # Loop over ship sizes
        for i in [1, 2, 2, 3, 4]:
            # Create text object
            text = (Text(Point(19.5, 8), 'Draw ship of size: ' + str(i + 1) + \
                (' (right side)')))
            # Set size of text to 30
            text.setSize(30)
            # Draw text
            text.draw(self.win)
            # Set difference to 0
            difference = 0
            # Set first and second click variables to False
            first_click = False
            second_click = False
            # While loop to be executed as long as difference does not equal
            #to i
            while difference != i:
                # Run while loop while first_click is False
                while first_click == False:
                    # Get mouse click
                    p = self.win.getMouse()
                    # If mouse click is within the boarders of the board set
                    #first_click to True
                    if 26.5 <= p.getX() <= 38.5 and 1.5 <= p.getY() <= 11.5:
                        first_click = True
                # Run while loop while second_click is False
                while second_click == False:
                    # Get mouse click
                    p2 = self.win.getMouse()
                    # If mouse click is within the boarders of the board set
                    #second_click to True
                    if 26.5 <= p2.getX() <= 38.5 and 1.5 <= p2.getY() <= 11.5:
                        second_click = True
                # Round x and y coordinates gotten from mouse clicks
                x1 = int(round(p.getX()))
                y1 = int(round(p.getY()))
                x2 = int(round(p2.getX()))
                y2 = int(round(p2.getY()))
                # Calculate difference between the x's and y's of the
                #coordinates
                difference_x = abs(x1 - x2)
                difference_y = abs(y1 - y2)
                # If difference between x's or y's is equal to length of ship
                #execute if body
                if (difference_x == i) or (difference_y == i):
                    # Create empty list
                    values = []
                    # Set difference to i
                    difference = i
                    # If y coordinates are the same execute if body
                    if y1 - y2 == 0:
                        # If first x coordinate is smaller than the second
                        #execute if body
                        if x1 < x2:
                            # Loop over coordinates in x1 to x2 + 1 range
                            for x_value in range(x1, x2 + 1):
                                # Loop over spaces in sea_space_list
                                for space in self.sea_space_list:
                                    #If space at Point(x_value, y1) clicked
                                    #execute if body
                                    if space.clicked(Point(x_value, y1)):
                                        # Append ship status at space to values
                                        #list
                                        values.append(space.get_ship_status())
                            # If True in values list execute if body
                            if True in values:
                                # Set difference to 0
                                difference = 0
                                # Set first and second click variables to False
                                first_click = False
                                second_click = False
                            # If True not in values list execute else body
                            else:
                                # Set difference to i
                                difference = i
                                # Loop over coordinates in x1 to x2 + 1 range
                                for x_value in range(x1, x2 + 1):
                                    # Loop over spaces in sea_space_list
                                    for space in self.sea_space_list:
                                        #If space at Point(x_value, y1) clicked
                                        #execute if body
                                        if space.clicked(Point(x_value, y1)):
                                            # Update ship
                                            space.update_ship()
                                # Create ship object
                                ship = (Ship(x1 - 0.5, y1 - 0.5, x2 + 0.5, \
                                    y2 + 0.5))
                                # Append ship to ship_list
                                ship_list.append(ship)
                                # Draw ship
                                ship.draw_ships(self.win)
                                
                        # If x2 smaller than x1 execute else body
                        else:
                            # Loop over coordinates in x2 to x1 + 1 range
                            for x_value in range(x2, x1 + 1):
                                # Loop over spaces in sea_space_list
                                for space in self.sea_space_list:
                                    # If space clicked append ship status to
                                    # values list
                                    if space.clicked(Point(x_value, y1)):
                                        values.append(space.get_ship_status())
                            # If True in values list set difference to 0 and
                            #first and second click variables False
                            if True in values:
                                difference = 0
                                first_click = False
                                second_click = False
                            # If True not in values list
                            else:
                                # Set difference to i
                                difference = i
                                # Loop over coordinates in x2 to x1 + 1 range
                                for x_value in range(x2, x1 + 1):
                                    # Loop over sea_space_list
                                    for space in self.sea_space_list:
                                        # If space clicked update ship
                                        if space.clicked(Point(x_value, y1)):
                                            space.update_ship()
                                # Create ship object, append it to ship_list
                                #and draw it
                                ship = (Ship(x1 + 0.5, y1 - 0.5, x2 - 0.5, \
                                    y2 + 0.5))
                                ship_list.append(ship)
                                ship.draw_ships(self.win)
                    # If x coordinates are the same execute elif body
                    elif x1 - x2 == 0:
                        # If y1 less than y2 execute if body
                        if y1 < y2:
                            # Loop over coordinates in y1 to y2 + 1 range
                            for y_value in range(y1, y2 + 1):
                                # Loop over sea_space_list
                                for space in self.sea_space_list:
                                    # If space clicked append ship status to
                                    #values list
                                    if space.clicked(Point(x1, y_value)):
                                        values.append(space.get_ship_status())
                            # If True in values list set difference to 0 and 
                            #first and second click variables False
                            if True in values:
                                difference = 0
                                first_click = False
                                second_click = False
                            # If True not in values list execute else body
                            else:
                                # Set difference to i
                                difference = i
                                # Loop over coordinates in y1 to y2 + 1 range
                                for y_value in range(y1, y2 + 1):
                                    # Loop over sea_space_list
                                    for space in self.sea_space_list:
                                        # If space clicked update ship
                                        if space.clicked(Point(x1, y_value)):
                                            space.update_ship()
                                # Create ship object, append it to ship_list,
                                #and draw it
                                ship = (Ship(x1 - 0.5, y1 - 0.5, x2 + 0.5, \
                                    y2 + 0.5))
                                ship_list.append(ship)
                                ship.draw_ships(self.win)
                        # If y2 less than y1 execute else body
                        else:
                            # Loop over coordinates in y2 to y1 + 1 range
                            for y_value in range(y2, y1 + 1):
                                # Loop over sea_space_list
                                for space in self.sea_space_list:
                                    # If space clicked append ship status to
                                    #values list
                                    if space.clicked(Point(x1, y_value)):
                                        values.append(space.get_ship_status())
                            # If True in values list set difference to 0 and
                            #first and second click variables False
                            if True in values:
                                difference = 0
                                first_click = False
                                second_click = False
                            # If True not in values list execute else body
                            else:
                                # Set difference to i
                                difference = i
                                # Loop over coordinates in y2 to y1 + 1 range
                                for y_value in range(y2, y1 + 1):
                                    # Loop over sea_space_list
                                    for space in self.sea_space_list:
                                        # If space clicked update ship
                                        if space.clicked(Point(x1, y_value)):
                                            space.update_ship()
                                # Create ship object, append it to ship_list,
                                #and draw it
                                ship = (Ship(x1 - 0.5, y1 + 0.5, x2 + 0.5, \
                                    y2 - 0.5))
                                ship_list.append(ship)
                                ship.draw_ships(self.win)
                    #If neither x or y coordinates are the same set difference
                    #to 0 and first and second click variables False
                    else:
                        difference = 0
                        first_click = False
                        second_click = False
                # If difference is not equal to i set first and second click
                #variables False
                else:
                    first_click = False
                    second_click = False
            #Undraw text
            text.undraw()
        for i in ship_list:
            i.undraw_ship()
                 

# Define Ship class. Takes self, x1, y1, x2, and y2 as parameters. Creates ship
# Methods include draw_ships and undraw(ship
class Ship:


    # Define constructor. Takes self, x1, y1, x2, and y2 as parameters. Creates
    #oval to be ship and fills it with black color
    def __init__(self, x1, y1, x2, y2):
        
        self.ship = Oval(Point(x1, y1), Point(x2, y2))
        self.ship.setFill('black')

    
    # Define draw_ships method. Takes self and window as parameters. Draws ship
    #in window
    def draw_ships(self, window):
        
        self.ship.draw(window)

    
    # Define undraw_ship method. Takes self as parameter. Undraws ship
    def undraw_ship(self):
        
        self.ship.undraw()


# Define Player class. Takes self and window as parameters. Creates player
#object. Methods include shoot and hit_count.
class Player:


    # Define constructor. Takes self and window as parameters. Sets up
    #board and places ships.
    def __init__(self, window):
        
        self.win = window
        # Create board
        self.sea = Sea_spaces(self.win, 'human')
        # Place ships
        self.sea.place_ship()
        # Set self.hits to 0
        self.hits = 0

    
    # Define shoot method. Takes self and opponent_list as parameters.
    # Ask for mouse click and updates that space accordingly depending on
    #whether it contains a ship or not
    def shoot(self, opponent_list):
        
        # Set j to 0
        j = 0
        # While loop to be executed as long as j is 0
        while j == 0:
            # Get mouse click
            p = self.win.getMouse()
            # Loop over opponent_list
            for i in opponent_list:
                # If i clicked execute if body
                if i.clicked(p):
                    # Get ship status of i
                    status = i.get_ship_status()
                    # If i has a ship in it execute if body
                    if status == True:
                        # If i is active (not shot before) execute if body
                        if i.active_button():
                            # Call hit method
                            i.hit()
                            # Increment self.hits
                            self.hits += 1
                            # Set j to 1
                            j = 1
                    # If i does not have ship in it execute else body
                    else:
                        # If i is active (not shot before) execute if body
                        if i.active_button():
                            # Deactivate button
                            i.deactivate()
                            # Set j to 1
                            j = 1
    
    
    # Define hit_count method. Takes self as parameter. Returns self.hits
    def hit_count(self):
        
        # Return self.hits
        return self.hits


# Define Computer class. Takes self and window as parameter. Sets up computer
#player. Methods include shoot and hit_count.
class Computer:


    # Define constructor. Takes self and window as parameters. Sets up board
    # and places ships
    def __init__(self, window):
        
        self.win = window
        # Set up board
        self.sea = Sea_spaces(self.win, 'computer')
        # Place ships
        self.sea.place_ship_computer()
        # Set self.hits and self.int to 0
        self.hits = 0
        self.int = 0
        # Set last_point, last_hit, and first_hit to Point(5, 5)
        self.last_point = (Point(5, 5))
        self.last_hit = Point(5, 5)
        self.first_hit = Point(5, 5)

    
    # Define shoot method. Takes self and opponent_list as parameters.
    #Shoots a space depending on whether it hit or did not hit the last time.
    def shoot(self, opponent_list):
        o_p = opponent_list
        j = 0
        while j == 0:
        #begins by creating a random point and shooting it
            x = random.randint(27,40)
            y = random.randint(2,13)
            p = Point(x, y)
            if self.int <= 0:
                empty = []
                #checks if point is clicking an active space in the opponent 
                #list
                for i in opponent_list:
                    empty.append(i.clicked(p))
                    if i.clicked(p):
                        status = i.get_ship_status()
                        #checks if button had a ship
                        #if it had a ship, it hits it, deactivates it
                        #and sets self.int to 4, so that it doesn't pick a 
                        #random point, but shoots an adjacent point
                        if status == True:
                            #keeps track of last point hit
                            #so that if it misses, it can keep shooting
                            #around the last made point, not the last shot
                            if i.active_button():
                                i.hit()
                                self.hits += 1
                                self.int = 4
                                self.last_point = p
                                self.last_hit = p
                                self.first_hit = p
                                j = 1
                            else:
                                self.int -= 1
                        #if no ship, it lowers self.int so that it picks
                        #a different point next shot
                        #deactivates shot at space
                        else:
                            if i.active_button():
                                i.deactivate()
                                self.int -= 1
                                self.last_point = p
                                j = 1
                            else:
                                self.int -= 1
                                self.last_hit = self.first_hit
                #makes it get a different point, if the point it randomly
                #picked was already shot at
                if True not in empty:
                    self.int -= 1   
                    self.last_hit = self.first_hit     
            #if self.int was 4, it will shoot to a point to the right
            #self.int is made 4 everytime a shot is made
            #it also checks if the point would be within the board
            elif self.int == 4 and 27 <= self.last_hit.getX() + 1 <= 39:
                x_1 = self.last_hit.getX() + 1
                p = Point(x_1, self.last_hit.getY())
                empty = []
                for i in opponent_list:
                    empty.append(i.clicked(p))
                    if i.clicked(p):
                        status = i.get_ship_status()
                        if status == True:
                            #keeps track of last point hit
                            #so that if it misses, it can keep shooting
                            #around the last made point, not the last shot
                            if i.active_button():
                                i.hit()
                                self.hits += 1
                                self.int = 4
                                self.last_point = p
                                self.last_hit = p
                                j = 1
                            else:
                                self.int -= 1
                        #if no ship, it lowers self.int so that it picks
                        #a different point next shot
                        #deactivates shot at space
                        else:
                            if i.active_button():
                                i.deactivate()
                                self.int -= 1
                                self.last_hit = self.first_hit
                                j = 1
                            else:
                                self.int -= 1
                                self.last_hit = self.first_hit
                #makes it get a different point, if the point it randomly
                #picked was already shot at
                if True not in empty:
                    self.int -= 1
                    self.last_hit = self.first_hit       
            #if self.int was 3, it will shoot to a point to the left
            #it also checks if the point would be within the board
            elif self.int == 3 and 27 <= self.last_hit.getX() - 1 <= 39:
                x_1 = self.last_hit.getX() - 1
                p = Point(x_1, self.last_hit.getY())
                empty = []
                for i in opponent_list:
                    empty.append(i.clicked(p))
                    if i.clicked(p):
                        status = i.get_ship_status()
                        if status == True:
                            #keeps track of last point hit
                            #so that if it misses, it can keep shooting
                            #around the last made point, not the last shot
                            if i.active_button():
                                i.hit()
                                self.hits += 1
                                self.int = 3
                                self.last_point = p
                                self.last_hit = p
                                j = 1
                            else:
                                self.int -= 1
                        #if no ship, it lowers self.int so that it picks
                        #a different point next shot
                        #deactivates shot at space
                        else:
                            if i.active_button():
                                i.deactivate()
                                self.int -= 1
                                self.last_hit = self.first_hit
                                j = 1
                            else:
                                self.int -= 1
                                self.last_hit = self.first_hit
                #makes it get a different point, if the point it randomly
                #picked was already shot at
                if True not in empty:
                    self.int -= 1
                    self.last_hit = self.first_hit     
            #if self.int was 2, it will shoot to a point above the last hit
            #it also checks if the point would be within the board
            elif self.int == 2 and 2 <= self.last_hit.getY() + 1 <= 12:
                y_1 = self.last_hit.getY() + 1
                p = Point(self.last_hit.getX(), y_1)
                empty = []
                for i in opponent_list:
                    empty.append(i.clicked(p))
                    if i.clicked(p):
                        status = i.get_ship_status()
                        if status == True:
                            #keeps track of last point hit
                            #so that if it misses, it can keep shooting
                            #around the last made point, not the last shot
                            if i.active_button():
                                i.hit()
                                self.hits += 1
                                self.int = 2
                                self.last_point = p
                                self.last_hit = p
                                j = 1
                            else:
                                self.int -= 1
                        #if no ship, it lowers self.int so that it picks
                        #a different point next shot
                        #deactivates shot at space
                        else:
                            if i.active_button():
                                i.deactivate()
                                self.int -= 1
                                self.last_hit = self.first_hit
                                j = 1
                            else:
                                self.int -= 1
                                self.last_hit = self.first_hit
                #makes it get a different point, if the point it randomly
                #picked was already shot at
                if True not in empty:
                    self.int -= 1
                    self.last_hit = self.first_hit     
            #if self.int was 1, it will shoot to a point below the last hit
            #it also checks if the point would be within the board
            elif self.int == 1 and 2 <= self.last_hit.getY() - 1 <= 12:
                y_1 = self.last_hit.getY() - 1
                p = Point(self.last_hit.getX(), y_1)
                empty = []
                for i in opponent_list:
                    empty.append(i.clicked(p))
                    if i.clicked(p):
                        status = i.get_ship_status()
                        if status == True:
                            #keeps track of last point hit
                            #so that if it misses, it can keep shooting
                            #around the last made point, not the last shot
                            if i.active_button():
                                i.hit()
                                self.hits += 1
                                self.int = 1
                                self.last_point = p
                                self.last_hit = p
                                j = 1
                        #if no ship, it lowers self.int so that it picks
                        #a different point next shot
                        #deactivates shot at space
                        else:
                            if i.active_button():
                                i.deactivate()
                                self.int -= 1
                                self.last_hit = self.first_hit
                                j = 1

                            else:
                                self.last_hit = self.first_hit
                                self.int -= 1
                #makes it get a different point, if the point it randomly
                #picked was already shot at
                if True not in empty:
                    self.int -= 1
                    self.last_hit = self.first_hit

                    
            #if there is no possible point around the last made
            #lowers self int to force the computer to take a random shot
            #avoids getting stuck if no point around a hit point was available                    
            else:
                self.int -= 1


    # Define hit_count method. Takes self as parameter. Returns self.hits
    def hit_count(self):
        
        # Return self.hits
        return self.hits


# Define BattleshipGame class. Takes self as parameter. Sets up graphic window,
#and creates players
class BattleshipGame:

    
    # Define constructor. Takes self as parameter. Sets up graphic window, and
    # creates players.
    def __init__(self):

        # Set width and height to be used to create window
        width = 1350
        height = 750
        # Create graphic window and set background to blue
        self.win = GraphWin('Battleship', width, height)
        self.win.setBackground('blue')
        # Set coordinates of graphic window
        self.win.setCoords(0, 0, 40, 15)
        # Create text objects and set size to 30
        player_str1 = Text(Point(20, 13), 'Human, place your ships')
        player_str1.setSize(30)
        # Draw text object
        player_str1.draw(self.win)
        # Create player (human)
        self.player1 = Player(self.win)
        # Undraw text object
        player_str1.undraw()
        # Create computer player
        self.player2 = Computer(self.win)
        # Get sea spaces for each player
        self.x = self.player1.sea.get_sea_spaces()
        self.y = self.player2.sea.get_sea_spaces()

    
    # Define close method. Takes self as parameter. Closes window
    def close(self):
        
        # Waits for user to click mouse before closing graphic window
        x = self.win.getMouse()
        self.win.close()


    # Define play method. Takes self as parameter. Runs the Battleship game
    def play(self):

        # Create text objects and set size to 20
        player1 = Text(Point(20,13), "Human, shoot on the left board!")
        player1.setSize(30)
        # Draw text
        player1.draw(self.win)
        # Set count to 1
        count = 1
        # Create infinite loop
        while True:
            # If count is even execute if body
            if count % 2 == 0:
                # Call shoot method
                self.player1.shoot(self.y)
                # Get hit count
                hits = self.player1.hit_count()
                # If hit count is 17 announce a winner
                if int(hits) == 17:
                    # Undraw text
                    player1.undraw()
                    # Create strings
                    s = 'Man is still the most extraordinary computer of all! '
                    d = '(Click to exit)'
                    # Create text object, set size to 30, and draw the text
                    winner = (Text(Point(20, 13), s + d))
                    winner.setSize(30)
                    winner.draw(self.win)
                    # Close window
                    self.close()
                    return
            # If count is odd execute else body
            else:
                # call shoot method
                self.player2.shoot(self.x)
                # Get hit count
                hits = self.player2.hit_count()
                # Create strings
                s = 'The age of Men is over, the time of Computer has come! '
                d = '(Click to exit)'
                # If hit count is 17 announce a winner
                if int(hits) == 17:
                    # Undraw text
                    player1.undraw()
                    # Create text object, set size to 30, and draw text
                    winner = (Text(Point(20, 13), s + d))
                    winner.setSize(30)
                    winner.draw(self.win)
                    # Close window
                    self.close()
                    return
            # Increment count by 1
            count += 1



# Define main function. Takes no parameters. Creates Battleship game and plays
#it
def main():

    # Create Battleship game
    game = BattleshipGame()
    # Play game
    game.play()


if __name__ == '__main__':
    main()
