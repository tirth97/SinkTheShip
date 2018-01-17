from graphics import *

class RectangleButton:

    #Method to initiliase buttons
    def __init__(self, center, width, height, color, ship):
        
        w = width/2.0
        h = height/2.0

        self.xmin = center.getX() - w
        self.xmax = center.getX() + w
        self.ymin = center.getY() - h
        self.ymax = center.getY() + h

        self.rect = Rectangle(Point(self.xmin, self.ymin), 
                                Point(self.xmax, self.ymax))

        self.center = center
        self.sea_space_ship = ship

        self.rect.setFill(color)
        self.activate()


    def draw(self, window):
        self.rect.draw(window)

    def undraw(self):
        self.rect.undraw()

    #method to handle click events by user
    def clicked(self, point):
        if (self.active and self.xmin <= point.getX() <= self.xmax and
                self.ymin <= point.getY() <= self.ymax):
            return True

    #method to deactivate a clicked cell
    def deactivate(self):
        self.rect.setFill('yellow')

    #method to activate a cell
    def activate(self):
        self.rect.setWidth(2)
        self.active = True


    #method to check for hits
    def hit(self):
        if self.active:
            self.rect.setWidth(2)
            self.deactivate()
            self.rect.setFill('red')
        self.active = False


    def outline(self, color):
        self.rect.setOutline(color)

    def get_center(self):
        return self.center

    #method which returns the status of aligned ship
    def get_ship_status(self):
        return self.sea_space_ship

    #method to update the ships
    def update_ship(self):
        self.sea_space_ship = True

    #method to activate the button
    def active_button(self):
        return self.active
