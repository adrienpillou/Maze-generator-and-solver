# # Author : Adrien Pillou
# Created : 26/10/2020

# Python Vector library
import math

class vector2():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return '{0}({1}, {2})'.format(
            self.__class__.__name__,
            self.x,
            self.y,
        )

    def __str__(self):
        return f"({self.x}, {self.y})"

    # Overloading + opertator
    def __add__(self, another_vector):
        if(isinstance(another_vector, vector2)):
            return vector2(self.x+another_vector.x, self.y+another_vector.y)
        else:
            raise TypeError

    # Overloading - opertator
    def __sub__(self, another_vector):
        if(isinstance(another_vector, vector2)):
            return vector2(self.x-another_vector.x, self.y-another_vector.y)
        else:
            raise TypeError

    # Overloading * opertator
    def __mul__(self, a):
        if(isinstance(a, int) or isinstance(a, float)):
            return(vector2(self.x*a, self.y*a))
    
    # Overloading == opertator
    def __eq__(self, another_vector):
        if(self.x==another_vector.x and self.y==another_vector.y):
            return True
        else:
            return False

    def __round__(self, n=None):
        if(n is not None):
            return(vector2(round(self.x, n), round(self.y, n)))
        else :
            return(vector2(round(self.x), round(self.y)))

    # Return the magnitude of a vector
    def magnitude(self):
        return math.sqrt(pow(self.x, 2), pow(self.y, 2))

    # Return a normalized vector
    def normalized(self):
        mag = self.magnitude()
        return vector2(self.x/mag, self.y/mag)

    def dot(self, another_vector):
        return self.x*another_vector.x + self.y*another_vector.y

    def zero(self):
        return(vector2(0, 0))
    
    def one(self):
        return(vector2(1, 1))
    
    def right(self):
        return(vector2(1, 0))

    def left(self):
        return(vector2(-1, 0))

    def up(self):
        return(vector2(0, 1))

    def down(self):
        return(vector2(0, -1))
    
    def to_list(self):
        return [self.x, self.y]

    def to_tuple(self):
        return (self.x, self.y)
    
    def from_list(self, list):
        if(len(list)!=2):
            raise AttributeError
        else:
            return vector2(list[0], list[1])

    def floored(self):
        return vector2(int(self.x), int(self.y))

    def distance(self, another_vector):
        distance = math.sqrt(math.pow(self.x - another_vector.x, 2) + math.pow(self.y - another_vector.y, 2)) 
        return distance
