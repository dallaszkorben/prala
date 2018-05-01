import sys
from prala.accessories import _
#from PyQt5.QtWidgets import QToolTip, QMainWindow, QPushButton, QApplication, QMessageBox, QDesktopWidget, QAction, QMenu
#from PyQt5.QtGui import QFont    

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QGridLayout, 
    QLabel, QPushButton, QLineEdit, QApplication, QHBoxLayout )
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon, QPalette
from PyQt5.QtWidgets import QAbstractButton
from pkg_resources import resource_string, resource_filename

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):        
                
        # --------------------
        # Fields
        # --------------------
        #
        question_title=QLabel(_("TITLE_QUESTION") + ":")
        question_field=QLabel("here is the question")
        question_field.setStyleSheet('color: brown')

        self.result_field=ResultWidget(result=None)

        answer_title=QLabel(_("TITLE_ANSWER") + ":")      
        self.answer_field=AnswerField(["hej", "Hello", "World", "ez pedig egy kicsit hosszabb"])

        #print(self.palette().color(QPalette.Base).name())
        #myFont = self.answer_field.font()  
        #myFont=QtGui.QFont()
        #myFont.setBold(True)
        #self.answer_field.setFont(myFont)
        #self.answer_field.setStyleSheet('color: blue; font: 30 pt bold; size:18')

        self.good_answer_field=GoodAnswerField(["hej", "Hello", "World", "ez pedig egy kicsit hosszabb"], self.palette().color(QPalette.Background))

        ok_button_pixmap = QPixmap(resource_filename(__name__, "/".join(("images", "ok-button.png"))))        
        ok_button_hover_pixmap = QPixmap(resource_filename(__name__, "/".join(("images", "ok-button-hover.png"))))        
        ok_button_pressed_pixmap = QPixmap(resource_filename(__name__, "/".join(("images", "ok-button-pressed.png"))))        

        #pixmap = pixmap.scaled(42, 42, Qt.KeepAspectRatio, Qt.FastTransformation)
        ok_button = PicButton(ok_button_pixmap, ok_button_hover_pixmap, ok_button_pressed_pixmap)
        ok_button.clicked.connect(self.on_click)


        stat_good_field=QLineEdit("1")
        stat_asked_field=QLineEdit("4")
        stat_remains_field=QLineEdit("6")
        stat_percent_field=QLineEdit("40")
        stat_percent_sign_label=QLabel("%")

        stat_history=QLabel("1 0 0 1 1")
        stat_points=QLineEdit("8")

        # --------------------
        # general grid setting
        # --------------------
        #
        grid=QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(1)

        # --------------------
        # Fields location
        # --------------------

        fields_rows=4
        grid.addWidget( question_title, 0, 0, 1, fields_rows )
        grid.addWidget( question_field, 1, 0, 1, fields_rows )

        grid.addWidget( self.result_field, 2, fields_rows-1, 1, 1, Qt.AlignRight )

        grid.addWidget( answer_title, 4, 0, 1, fields_rows)
        grid.addWidget( self.answer_field, 5, 0, 1, fields_rows-1)
        grid.addWidget( self.good_answer_field, 6, 0, 1, fields_rows )
        #grid.addWidget( stat_, 7, 0, 1, fields_rows ) 
        grid.addWidget( stat_history, 8, 0, 1, fields_rows )
        
        grid.addWidget( ok_button, 5, fields_rows-1, 1, 1 )


        self.setGeometry(300, 300, 450, 150)
        self.setWindowTitle(_("TITLE_WINDOW"))    
        self.show()

    def on_click(self):
        self.result_field.set_result(False)
        self.good_answer_field.show_text()


class AnswerField(QWidget):
    def __init__(self, word_list):
        super().__init__()
        self.set_text(word_list)

    def set_text(self, word_list):

        self.layout=QHBoxLayout()
        self.layout.setSpacing(1)
        
        for i in word_list:
            self.layout.addWidget( self.getSingleField(i) )
        self.layout.addStretch(10)
        self.setLayout(self.layout)

    def getSingleField(self, word):
        return SingleField(len(word), 15, Qt.blue, Qt.lightGray)

class GoodAnswerField(AnswerField):
    def __init__(self, word_list, bg):
        self.word_list=word_list
        self.bg=bg
        super().__init__(word_list)
        
    def getSingleField(self, word):
        sf = SingleField(len(word), 15, Qt.red, self.bg)
        print(self.bg.name())
        sf.setEnabled(False)
        return sf

    def show_text(self):
        j=0
        for i in self.word_list:
            widget=self.layout.itemAt(j).widget()
            widget.setText( i )
            j += 1

class SingleField(QLineEdit):
        def __init__(self, length, size, color, background):
            QLineEdit.__init__(self)
            
            # monospace font - size:15 Bold
            self.setFont(QFont("Courier New",pointSize=size, weight=QFont.Bold))

            # font color and background color
            palette = QPalette()
            palette.setColor(QPalette.Text, color)
            palette.setColor(self.backgroundRole(), background)
            self.setPalette( palette )
            

            # border not visible
            self.setFrame(False)

            # max enabled characters
            self.setMaxLength(length)
            # widht of 'W'
            self.setFixedWidth(self.fontMetrics().width("W" * length) + 5)
            



class ResultWidget(QLabel):
    """
    Shows the result as a red/green light
    """
    WIDTH=42
    HEIGHT=42
    def __init__(self, result=None):
        QLabel.__init__(self)

        self.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum))

        self.set_result(result)

    def set_result(self, result):
        if result is None:
            pixmap = QPixmap(resource_filename(__name__, "/".join(("images", "empty-light.png"))))        
        elif result:
            pixmap = QPixmap(resource_filename(__name__, "/".join(("images", "green-light.png"))))        
        else:
            pixmap = QPixmap(resource_filename(__name__, "/".join(("images", "red-light.png"))))        

        pixmap = pixmap.scaled(type(self).WIDTH, type(self).HEIGHT, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.setPixmap(pixmap)

    def sizeHint(self): 
        return QSize(type(self).WIDTH, type(self).HEIGHT)


class PicButton(QAbstractButton):
    """
    Button
    """
    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        
        return QSize(100,38)

def main():    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    
    
