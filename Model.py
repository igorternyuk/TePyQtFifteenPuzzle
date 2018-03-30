from enum import Enum
from collections import namedtuple
import random

Direction = namedtuple('Direction', ['dx', 'dy'])
ANIMATION_SPEED = 50

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

def get_opposite_direction( direction ):
    if( direction == Directions.LEFT ):
        return Directions.RIGHT
    elif( direction == Directions.RIGHT ):
        return Directions.LEFT
    elif( direction == Directions.UP ):
        return Directions.DOWN
    elif( direction == Directions.DOWN ):
        return Directions.UP

class Model:
    def __init__( self, width, height, tile_size ):
        self.field_width = width
        self.field_height = height
        self.tile_size = tile_size
        self.grid = self.__create_grid()
        #self.print_grid()
        if( not self.__is_solveable_( self.grid ) ):
            #print("Not solveable")
            self.__make_solveable_()
            #self.print_grid()
        self.zero_tile = self.grid[ len( self.grid ) - 1 ]
        self.selected_tile = None
        self.all_directions = [ Directions.LEFT, Directions.RIGHT,
         Directions.UP, Directions.DOWN]
        self.animation_direction = Directions.RIGHT
        self.move_count = 0
        self.is_game_over = False

    def __create_grid( self ):
        grid = []
        values = []
        max_index = self.field_width * self.field_height
        zero_index = 0
        for row in range( self.field_height ):
            for col in range( self.field_width ):
                value = random.choice( range( max_index ) )
                while value in values:
                    value = random.choice( range( max_index ) )
                values.append( value )
                if value == 0 :
                    zero_index = row * self.field_height + col
                grid.append( Tile( col * self.tile_size,
                 row * self.tile_size, value ) )
        self.__swap_tile_values_( grid, zero_index, max_index - 1 )
        return grid

    def __make_solveable_( self ):
        self.__swap_tile_values_( self.grid, len( self.grid ) - 2, len( self.grid ) - 3 )

    def reset( self ):
        self.grid = self.__create_grid()
        if( not self.__is_solveable_( self.grid ) ):
            self.__make_solveable_()
        self.zero_tile = self.grid[ len( self.grid ) - 1 ]
        self.move_count = 0
        self.is_game_over = False

    def __swap_tile_values_( self, grid, first_index, second_index ):
        tmp = grid[first_index].value
        grid[first_index].value = grid[second_index].value
        grid[second_index].value = tmp

    def __is_solveable_( self, grid ):
        chaos_number = 0
        for i in range( len( grid ) - 1):
            for j in range( i ):
                if(grid[j].value > grid[i].value):
                    chaos_number += 1
        #print("Chaos number = ", chaos_number)
        return chaos_number % 2 == 0

    def __is_solved_( self ):
        for tile in self.grid:
            value = tile.value
            if value != 0:
                x = ( int(value - 1) % self.field_width ) * self.tile_size
                y = int( int(value - 1) / self.field_width ) * self.tile_size
                if( tile.x != x or tile.y != y ):
                    return False
            else:
                if( tile.x != ( self.field_width - 1 ) * self.tile_size or tile.y != ( self.field_height - 1 ) * self.tile_size ):
                    return False
        return True

    def __find_tile_by_coords_( self, x, y ):
        for tile in self.grid:
            if(tile.x == x and tile.y == y):
                return tile
        return None

    def try_to_slide( self, x, y ):
        if not self.selected_tile is None:
            return
        self.selected_tile = self.__find_tile_by_coords_( x, y)
        if( not self.selected_tile is None ):
            for dir in self.all_directions:
                neighbour_x = x + dir.dx * self.tile_size
                neighbour_y = y + dir.dy * self.tile_size
                if self.zero_tile.x == neighbour_x and self.zero_tile.y == neighbour_y:
                    self.animation_direction = dir
                    #print(self.animation_direction)
                    self.selected_tile.destX = neighbour_x
                    self.selected_tile.destY = neighbour_y
                    self.zero_tile.x = self.selected_tile.x
                    self.zero_tile.y = self.selected_tile.y
                    self.move_count += 1
                    return
        self.selected_tile = None

    def try_to_slide_in_direction( self, direciton ):
        if self.selected_tile is None :
            opposit_dir = get_opposite_direction( direciton )
            neighbour_x = self.zero_tile.x + opposit_dir.dx * self.tile_size
            neighbour_y = self.zero_tile.y + opposit_dir.dy * self.tile_size
            self.selected_tile = self.__find_tile_by_coords_( neighbour_x, neighbour_y)
            if not self.selected_tile is None:
                self.animation_direction = direciton
                #print(self.animation_direction)
                self.selected_tile.destX = self.zero_tile.x
                self.selected_tile.destY = self.zero_tile.y
                self.zero_tile.x = neighbour_x
                self.zero_tile.y = neighbour_y
                self.move_count += 1

    def tick( self ):
        if( not self.selected_tile is None):
            self.selected_tile.x += ANIMATION_SPEED * self.animation_direction.dx
            self.selected_tile.y += ANIMATION_SPEED * self.animation_direction.dy
            if not self.selected_tile.is_moving() :
                self.selected_tile = None
                self.is_game_over = self.__is_solved_()

    def print_grid( self ):
        for i in range( self.field_height ):
            for j in range( self.field_width ):
                print( "(" + str(i) + "," + str(j) + ") -> "
                + str(self.grid[ i * self.field_width + j ].value) )


class Tile:
    def __init__( self, x, y, value ):
        self.x = x
        self.y = y
        self.value = value
        self.destX = self.x
        self.destY = self.y

    def is_moving( self ):
        return (self.x != self.destX) or (self.y != self.destY )
