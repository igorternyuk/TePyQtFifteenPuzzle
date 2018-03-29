#lista = [1,2,3,4,5,6,7,8,9]
#length(x in lista)
from enum import Enum
from collections import namedtuple

Direction = namedtuple('Direction', ['dx', 'dy'])

class Directions( Enum ):

    @property
    def dx( self ):
        return self.value.dx

    @property
    def dy( self ):
        return self.value.dy

    LEFT = Direction( -1, 0 )
    RIGHT = Direction( 1, 0 )
    UP = Direction( 0, -1 )
    DOWN = Direction( 0, 1 )

values = [ Directions.LEFT, Directions.RIGHT, Directions.UP, Directions.DOWN]
for dir in values:
    print(dir.dx, dir.dy)

lista = []

for i in range(0, 10, 1):
    lista.append(i + 1)

print(lista)
print(len([x for x in lista if (x % 2 == 0)]))
