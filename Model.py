from enum import Enum
from collections import namedtuple
import random

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

class Model:
    def __init__( self, width, height ):
        self.field_width = width
        self.field_height = height
        self.grid = self.__create_grid()
        self.selected_tile = None
        self.direction = Directions.RIGHT
        self.anim_start_coord = 0
        self.anim_end_coord = 0

    def __is_valid_tile_index( self, index ):
        return index >= 0 and index < self.field_width * self.field_height

    def __is_valid_coordinates( self, x, y ):
        return x >= 0 and x < self.field_width and y >= 0 and y < self.field_height

    def __create_grid( self ):
        grid = []
        values = []
        max_index = self.field_width * self.field_height
        for y in range( self.field_height ):
            #row = []
            for x in range( self.field_width ):
                if( x == self.field_width - 1 and y == self.field_height - 1):
                    grid.append( Tile( x, y, 0 ) )
                else:
                    value = random.choice( range( 1, max_index ) )
                    while value in values:
                        value = random.choice( range(1,  max_index ) )
                    values.append( value )
                    grid.append( Tile( x, y, value ) )
            #grid.append( row )
        grid.append( Tile( x, y, 0 ) )
        if( not self.__is_solveable( grid ) ):
            penultimate = len( grid ) - 2
            last = len( grid ) - 1
            self.__swap_tiles( last, penultimate )
        return grid

    def __swap_tiles( self, first, second ):
        if( self.__is_valid_tile_index( first ) and self.__is_valid_tile_index( second ) ):
            tmp = grid[first]
            grid[first].value = grid[second].value
            grid[second].value = tmp

    def reset( self ):
        self.__create_grid()

    def __is_solveable( self, grid ):
        chaos_number = 0
        for i in range( len( grid ) ):
            for j in range( i ):
                if(grid[j].value > i):
                    chaos_number += 1
        return chaos_number % 2 == 0

    def __is_solved( self ):
        pass

    def __get_index_by_coordinates():
        pass

    def try_to_slide( self, x, y ):
        if( x == 3 and y == 3):
            selected_tile = self.grid[ y * 4 + x ]
            self.anim_end_coord = 3

    def tick( self ):
        if( not self.selected_tile is None):
            self.selected_tile.x += self.direction.dx
            if( self.selected_tile.x >= self.anim_end_coord ) :
                self.selected_tile = None

class Tile:
    def __init__( self, x, y, value ):
        self.x = x
        self.y = y
        self.value = value
