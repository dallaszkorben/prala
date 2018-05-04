import sys
from prala.accessories import _, Enum
#from PyQt5.QtWidgets import QToolTip, QMainWindow, QPushButton, QApplication, QMessageBox, QDesktopWidget, QAction, QMenu
#from PyQt5.QtGui import QFont    

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QGridLayout, QFrame, 
    QLabel, QPushButton, QLineEdit, QApplication, QHBoxLayout, QTextEdit )
from PyQt5.QtGui import QPainter, QFont, QColor
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
        question_field=QuestionField("Here is the question")
 
        self.good_answer=["hej", "HelloWorld", "a", "ez pedig egy kicsit hosszabb"]

        answer_title=QLabel(_("TITLE_ANSWER") + ":") 
        self.answer_field=AnswerField(self.good_answer, bg=self.palette().color(QPalette.Background))

        self.good_answer_field=ExpectedAnswerField(self.good_answer, bg=self.palette().color(QPalette.Background))

        self.result_lamp=ResultWidget(failed_position_list=None)

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

        #grid.addWidget( self.result_lamp, 2, fields_rows-1, 1, 1, Qt.AlignRight )

        grid.addWidget( answer_title, 4, 0, 1, fields_rows)
        grid.addWidget( self.answer_field, 5, 0, 1, fields_rows-1)
        grid.addWidget( self.good_answer_field, 6, 0, 1, fields_rows )
        grid.addWidget( self.result_lamp, 6, fields_rows-1, 1, 1, Qt.AlignCenter )
        #grid.addWidget( stat_, 7, 0, 1, fields_rows ) 
        grid.addWidget( stat_history, 8, 0, 1, fields_rows )
        
        grid.addWidget( ok_button, 5, fields_rows-1, 1, 1 )


        self.setGeometry(300, 300, 450, 150)
        self.setWindowTitle(_("TITLE_WINDOW"))    
        self.show()

    def on_click(self):
        self.answer_field.disableText()
        self.result_lamp.set_result(False)
        self.good_answer_field.showText([[],[1],[],[]], self.answer_field.getFieldsContentList())

class QuestionField(QLabel):
    FONT_SIZE = 13
    FONT_COLOR = QColor(212, 140, 95)
    def __init__(self, question):
        super().__init__()
        
        self.setFont(QFont("Courier New",pointSize=QuestionField.FONT_SIZE, weight=QFont.Bold))
        
        palette = QPalette()
        palette.setColor(self.foregroundRole(), QuestionField.FONT_COLOR)
        self.setPalette( palette )

        self.set_fields(question)

    def set_fields(self, question):
        self.setText(question)

class AnswerField(QWidget):
    FONT_BASIC_SIZE = 15
    FONT_BASIC_COLOR = Qt.blue
    FONT_BG = Qt.white

    def __init__(self, expected_word_list, bg):
        super().__init__()        
        
        self.__bg = bg
        self.__set_fields(expected_word_list)

    def __set_fields(self, expected_word_list):
        """
        Every time when it is called, a new layout will be generated
        """
        self.__expected_word_list=expected_word_list

        self.layout=QHBoxLayout()
        self.layout.setSpacing(1)
        
        for i in expected_word_list:
            self.layout.addWidget( self._get_single_field(i) )
        self.layout.addStretch(10)
        self.setLayout(self.layout)

    def _get_single_field(self, word):
        """
        Returns the empty SingleField of the specific part of the word
        with the right length, font size, basic_bg for inside use
        """
        return SingleField(len(word), size=AnswerField.FONT_BASIC_SIZE, color=AnswerField.FONT_BASIC_COLOR, bg=self.getBackgroundColor())

    def clearText(self):
        """
        Clear all fields of text
        """
        for widget in self.getFieldIterator():
            widget.clear()

    def disableText(self):
        """
        Disable all fields
        """
        for widget in self.getFieldIterator():
            widget.setEnabled( False )

    def enableText(self):
        """
        Enable all fields to edit
        """
        for widget in self.getFieldIterator():
            widget.setEnabled( True )

    def getBackgroundColor(self):
        return self.__bg

    def getExpectedWordList(self):
        return self.__expected_word_list
    
    def getFieldsContentList(self):
        """
        Returns the contents of the fields in a list
        """
        fields_content_list = []
        
        for widget in self.getFieldIterator():
            
            # adds the text from the field to the list
            fields_content_list.append( widget.toPlainText().strip() )

        return fields_content_list

        #for i in range(self.layout.count()):
        #
        #    # self.layout.itemAt(i) -> QWidgetItem
        #    widget = self.layout.itemAt(i).widget()
        #    
        #    if isinstance(widget, SingleField):
        #        fields_content_list.append( widget.toPlainText().strip() )
        #return fields_content_list

    def getFieldIterator(self):
        """
        Returns the SingleField widgets
        """
        for i in range(self.layout.count()):

            # self.layout.itemAt(i) -> QWidgetItem
            widget = self.layout.itemAt(i).widget()
            
            if isinstance(widget, SingleField):
                yield widget


class ExpectedAnswerField(AnswerField):
    FONT_SIZE = 15
    FONT_COLOR = Qt.black
    def __init__(self, word_list, bg):
        super().__init__(word_list, bg)
        
    def _get_single_field(self, word):
        """
        Returns the empty SingleField of the specific part of the word
        with the right length, font size, basic_bg for inside use
        """
        sf = SingleField(len(word), size=ExpectedAnswerField.FONT_SIZE, color=ExpectedAnswerField.FONT_COLOR, bg=self.getBackgroundColor())
        sf.setEnabled(False)
        return sf

    def showText(self, failed_position_list, answer_list):      
        """
        Shows the expected answer, coloring the faild characters in position
        """

        good_answer_list = self.getExpectedWordList()

        # go trough the answer and the failed_position_list pairs        
        #word_failed_position_pair_list = list(zip( completed_answer, failed_position_list ))
        word_failed_position_pair_list = list(zip( good_answer_list, failed_position_list ))

        self.clearText()

        # trough the widgets in the layout
        #for widget in self.getFieldIterator():
        for i in range(self.layout.count()):

            # self.layout.itemAt(i) -> QWidgetItem
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, SingleField):

                    # go trough all characters in the widget
                    for pos in range(len(word_failed_position_pair_list[i][0])):

                        if pos in word_failed_position_pair_list[i][1]:
                            widget.appendText(word_failed_position_pair_list[i][0][pos], color=Qt.red)
                          
                        else:
                            widget.appendText(word_failed_position_pair_list[i][0][pos], color=Qt.green)

class SingleField(QTextEdit):

    BASIC_FONT = "Courier New"
    BASIC_SIZE = 12
    BASIC_COLOR = Qt.black
    BASIC_BG = Qt.white

    def __init__(self, length, font=None, size=None, color=None, bg=None):
        super().__init__()

        if font == None:
            self.basic_font=SingleField.BASIC_FONT
        else:
            self.basic_font=font
        if size == None:
            self.basic_size = SingleField.BASIC_SIZE
        else:
            self.basic_size = size
        if color == None:
            self.basic_color = SingleField.BASIC_COLOR
        else:
            self.basic_color = color
        if bg == None:
            self.basic_bg = SingleField.BASIC_BG
        else:
            self.basic_bg = bg

        self.length = length

        # No Border
        self.setFrameStyle(QFrame.NoFrame)
          
        # No ScrollBar
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # font, colors
        self.__set_basic_font()

        # Vertical size of the field (1 line)
        self.setFixedHeight(self.fontMetrics().height() + 3)

        # Horizontal size of the field
        self.setFixedWidth(self.fontMetrics().width("W" * length) + 10)

        # for control the number of the characters in the field
        self.textChanged.connect(self.changed_text)

    def __set_basic_font(self):
       
        # monospace font - basic_size:15 Bold
        self.setFont(QFont("Courier New",pointSize=self.basic_size, weight=QFont.Bold))

        # font basic_color and basic_bg basic_color
        palette = self.palette()   # QPalette()
        palette.setColor(QPalette.Text, self.basic_color)
        palette.setColor(self.backgroundRole(), self.basic_bg)
        self.setPalette( palette )

    def appendText( self, text, color=None, bg=None ):
        if color == None:
            color = self.basic_color
        if bg == None:
            bg = self.basic_bg

        self.setTextColor(color)
        self.setTextBackgroundColor(bg)
        self.insertPlainText(text)

    def keyPressEvent(self, event):
        key = event.key()
        if key in [ Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab ]:
            self.parent().focusNextChild()
        else:
            QTextEdit.keyPressEvent(self, event)
    
#    def textChanged( self, )

    def changed_text(self):
        
        if len(self.toPlainText()) > self.length:
            self.setPlainText( self.toPlainText().strip()[0:self.length] )
        
            cursor = self.textCursor()
            cursor.setPosition(self.length)
            self.setTextCursor(cursor)

        print(self.toPlainText())




    
class __SingleField(QLineEdit):
        def __init__(self, length, basic_size, basic_color, basic_bg):
            QLineEdit.__init__(self)
            
            # monospace font - basic_size:15 Bold
            self.setFont(QFont("Courier New",pointSize=basic_size, weight=QFont.Bold))

            # font basic_color and basic_bg basic_color
            palette = QPalette()
            palette.setColor(QPalette.Text, basic_color)
            palette.setColor(self.backgroundRole(), basic_bg)
            self.setPalette( palette )

            # border not visible
            self.setFrame(False)

            # max enabled characters
            self.setMaxLength(length)
            
            # widht of 'W'
            self.setFixedWidth(self.fontMetrics().width("W" * length) + 5)


class ResultWidget(QLabel):
    """
    Shows the failed_position_list as a red/green light
    """
    WIDTH=42
    HEIGHT=42
    def __init__(self, failed_position_list=None):
        QLabel.__init__(self)

        self.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Minimum))

        self.set_result(failed_position_list)

    def set_result(self, failed_position_list):
        if failed_position_list is None:
            pixmap = QPixmap(resource_filename(__name__, "/".join(("images", "empty-light.png"))))        
        elif failed_position_list:
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
    
    
