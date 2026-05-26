# Instructions
# The goal is to create a class that represents a simple circle.

# A Circle can be defined by either specifying the radius or the diameter - use a decorator for it.
# The user can query the circle for either its radius or diameter.



# Abilities of a Circle Instance
# Your Circle class should be able to:

# ✅ Compute the circle’s area.
# ✅ Print the attributes of the circle — use a dunder method (__str__ or __repr__).
# ✅ Add two circles together and return a new circle with the new radius — use a dunder method (__add__).
# ✅ Compare two circles to see which is bigger — use a dunder method (__gt__).
# ✅ Compare two circles to check if they are equal — use a dunder method (__eq__).
# ✅ Store multiple circles in a list and sort them — implement __lt__ or other comparison methods.


# Bonus Challenge (Optional)
# If you want an extra challenge:

# Install the Turtle module (pip install PythonTurtle)
# Draw the sorted circles visually on the screen!


# 💡 Tip:

# Test your implementation by creating several circles and printing comparisons, additions, and sorted results.
class Circle:
    def __init__(self, radius=None, diameter=None):
        if radius is None and diameter is None:
            raise ValueError("You must provide either radius or diameter")

        if radius is not None and diameter is not None:
            raise ValueError("Provide only radius or diameter, not both")

        if radius is not None:
            self.radius = radius
        else:
            self.radius = diameter / 2
    
    @property
    def diameter(self):
        return self.radius * 2
    
    @diameter.setter
    def diameter(self, value):
        self.radius = value / 2
        
    def area(self):
        return 3.14 * self.radius **2
    
    def __add__(self, other):
        if isinstance(other, Circle):
            return Circle(radius = self.radius + other.radius)
        
        raise TypeError("The second one is not a circle! cannot add!")
    
    def __str__(self):
        return f"a Circle with radius of {self.radius}"
    
    def __repr__(self):
        return f"Circle(radius={self.radius})"
    
    def __gt__(self, other):
        if isinstance(other, Circle):
            if self.radius > other.radius:
                return f"{self} is bigger than {other}"
            if self.radius < other.radius:
                return f"{other} is bigger than {self}"
            
            return f"{self} and {other} are the same size"
           
        raise TypeError("The second one is not a circle! cannot compare!")
    
    def __eq__(self, other):
        if isinstance(other, Circle):
            return f"{self} and {other} are {'' if self.radius == other.radius else 'not'} equal"
           
        raise TypeError("The second one is not a circle! cannot compare!")

    def __lt__(self, other):
        if isinstance(other, Circle):
            return self.radius < other.radius
        
        raise TypeError("The second one is not a circle! cannot compare!")

        
        
        
c1 = Circle(diameter=10)
print(c1.diameter)
c1.diameter = 24
print(c1.diameter)
print(c1.radius)
print(c1.area())
c2 = Circle(8)
print(c1.__add__(c2))
print(c1.__gt__(c2))
print(c1.__eq__(c2))

c3 = Circle(15)

circles = [c1, c2, c3]
circles.sort()
print(circles)


import turtle
def draw_circles(circles):
    screen = turtle.Screen()
    screen.title("Sorted. Circles")
    
    pen = turtle.Turtle()
    pen.speed(3)
    
    start_x = 0
    y = 0
    gap = 30
    x = start_x
    for circle in circles:
        radius = circle.radius
        
        pen.penup()
        pen.goto(x, y - radius)
        pen.down()
        pen.circle(radius)
        
        pen.penup()
        pen.goto(x - 20, y -  radius - 30)
        pen.write(f"r={radius}", font=("Arial", 12, "normal"))
        
        x += radius + gap
    
    turtle.done()
    

draw_circles(circles)