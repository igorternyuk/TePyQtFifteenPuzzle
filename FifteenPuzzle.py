from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QRectF
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
import sys, random
from Model import*

TITLE_OF_PROGRAM= "TePyQtFifteenPuzzle"
TILE_SIZE = 100
FIELD_WIDTH = 4
FIELD_HEIGHT = 4
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
        self.model = Model( 4, 4 )

    def keyPressEvent( self, event ):
        pass

    def mouseReleaseEvent( self, event ):
        x = int( event.x() / TILE_SIZE )
        y = int( event.y() / TILE_SIZE )
        print( x, y )

    def timerEvent( self, event ):
        pass

    def paintEvent( self, event ):
        painter = QPainter( self )
        color = QColor("#e74c3c")
        font = QFont( "Arial" )
        font.setPointSize( 40 )
        painter.setFont( font )
        for tile in self.model.grid:
            if( tile.value != 0):
                painter.setPen(QPen( QColor( 200, 200, 200 ), 5))
                painter.drawRect(tile.x * TILE_SIZE, tile.y * TILE_SIZE,
                TILE_SIZE, TILE_SIZE)
                painter.setBrush( color )
                painter.fillRect(tile.x * TILE_SIZE, tile.y * TILE_SIZE,
                TILE_SIZE, TILE_SIZE, color)
                painter.setPen(QPen( QColor( 0, 0, 0 ), 5))
                painter.drawText( QRectF( tile.x * TILE_SIZE, tile.y * TILE_SIZE,
                 TILE_SIZE, TILE_SIZE ), Qt.AlignCenter | Qt.AlignTop ,
                  str(tile.value))

"""
colors={
0:'#2c3e50',
2:'#1abc9c',
4:'#2ecc71',
8:'#27a60',
16:'#3498db',
32:'#9b59b6',
64:'#f1c40f',
128:'#f39c12',
256:'#e67e22',
512:'#d35400',
1024:'#e74c3c',
2048:'#c0392b'
}
"""

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    sys.exit(app.exec_())
