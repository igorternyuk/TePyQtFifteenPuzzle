from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QRectF
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
import sys, random
from Model import*

TITLE_OF_PROGRAM= "TePyQtFifteenPuzzle"
TILE_SIZE = 100
FIELD_WIDTH = 4
FIELD_HEIGHT = 4
TIMER_DELAY = 34 #ms
WINDOW_WIDTH = FIELD_WIDTH * TILE_SIZE
WINDOW_HEIGHT = FIELD_HEIGHT * TILE_SIZE

class Window( QMainWindow ):

    def __init__( self ):
        super().__init__()
        self.init_UI()

    def init_UI( self ):
        self.canvas = Canvas( self )
        self.setCentralWidget( self.canvas )
        self.setWindowTitle(TITLE_OF_PROGRAM)
        self.setFixedSize( WINDOW_WIDTH, WINDOW_HEIGHT )
        self.centralize()
        self.show()

    def centralize( self ):
        screen_rect = QDesktopWidget().screenGeometry()
        window_rect = self.geometry()
        dx = ( screen_rect.width() - window_rect.width() ) / 2
        dy = ( screen_rect.height() - window_rect.height() ) / 2
        self.move( dx, dy )


class Canvas( QFrame ):
    def __init__( self, parent = None):
        super().__init__( parent )
        self.setFocusPolicy( Qt.StrongFocus )
        self.model = Model( FIELD_WIDTH, FIELD_HEIGHT, TILE_SIZE )
        self.timer = QBasicTimer()
        self.timer.start( TIMER_DELAY, self )

    def keyPressEvent( self, event ):
        key = event.key()
        if key == Qt.Key_Space:
            self.model.reset()
            self.parent().setWindowTitle(TITLE_OF_PROGRAM)
            self.update()
        elif key == Qt.Key_Left or key == Qt.Key_A:
            self.model.try_to_slide_in_direction( Directions.LEFT )
        elif key == Qt.Key_Up or key == Qt.Key_W:
            self.model.try_to_slide_in_direction( Directions.UP )
        elif key == Qt.Key_Right or key == Qt.Key_D:
            self.model.try_to_slide_in_direction( Directions.RIGHT )
        elif key == Qt.Key_Down or key == Qt.Key_S:
            self.model.try_to_slide_in_direction( Directions.DOWN )

    def mouseReleaseEvent( self, event ):
        x = int(event.x() / TILE_SIZE) * TILE_SIZE
        y = int(event.y() / TILE_SIZE) * TILE_SIZE
        self.model.try_to_slide( x, y )

    def timerEvent( self, event ):
        if event.timerId() == self.timer.timerId():
            self.model.tick()
            self.parent().setWindowTitle(TITLE_OF_PROGRAM + ": "+ str(self.model.move_count))
            self.update()

    def paintEvent( self, event ):
        painter = QPainter( self )
        color = QColor("#e74c3c")
        font = QFont( "Arial" )
        font.setPointSize( 40 )
        painter.setFont( font )
        for tile in self.model.grid:
            if( tile.value != 0):
                painter.setBrush( color )
                painter.fillRect( tile.x + 2, tile.y + 2, TILE_SIZE - 2, TILE_SIZE - 2, color)
                painter.setPen(QPen( QColor( 0, 0, 0 ), 5))
                painter.drawText( QRectF( tile.x, tile.y, TILE_SIZE, TILE_SIZE ), Qt.AlignCenter | Qt.AlignTop ,
                  str(tile.value))
        if( self.model.is_game_over ):
            font = QFont( "Arial" )
            font.setPointSize( 80 )
            painter.setPen( QPen( QColor( 0, 190, 0 ), 20 ) )
            painter.drawText( QRectF( 0, 0, FIELD_WIDTH * TILE_SIZE, FIELD_HEIGHT * TILE_SIZE ), Qt.AlignCenter | Qt.AlignTop ,
              str("Puzzle solved!"))

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    sys.exit(app.exec_())
