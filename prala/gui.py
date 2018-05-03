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
        #question_field=QLabel("here is the question")
        #question_field.setStyleSheet('basic_color: brown')

        self.result_field=ResultWidget(failed_position_list=None)

        answer_title=QLabel(_("TITLE_ANSWER") + ":") 

        self.good_answer=["hej", "HelloWorld", "a", "ez pedig egy kicsit hosszabb"]

        self.answer_field=AnswerField(self.good_answer, self.palette().color(QPalette.Background))


        #print(self.palette().basic_color(QPalette.Base).name())
        #myFont = self.answer_field.font()  
        #myFont=QtGui.QFont()
        #myFont.setBold(True)
        #self.answer_field.setFont(myFont)
        #self.answer_field.setStyleSheet('basic_color: blue; font: 30 pt bold; basic_size:18')

        self.good_answer_field=GoodAnswerField(self.good_answer, self.palette().color(QPalette.Background))

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

        #grid.addWidget( self.result_field, 2, fields_rows-1, 1, 1, Qt.AlignRight )

        grid.addWidget( answer_title, 4, 0, 1, fields_rows)
        grid.addWidget( self.answer_field, 5, 0, 1, fields_rows-1)
        grid.addWidget( self.good_answer_field, 6, 0, 1, fields_rows )
        grid.addWidget( self.result_field, 6, fields_rows-1, 1, 1, Qt.AlignCenter )
        #grid.addWidget( stat_, 7, 0, 1, fields_rows ) 
        grid.addWidget( stat_history, 8, 0, 1, fields_rows )
        
        grid.addWidget( ok_button, 5, fields_rows-1, 1, 1 )


        self.setGeometry(300, 300, 450, 150)
        self.setWindowTitle(_("TITLE_WINDOW"))    
        self.show()

    def on_click(self):
        self.result_field.set_result(False)
        self.good_answer_field.show_text()
        self.answer_field.start_correction([[],[1],[],[]])

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

    def __init__(self, good_answer_list, bg):
        super().__init__()
        self.bg = bg
        self.set_fields(good_answer_list)

    def start_input(self):
        for i in range(self.layout.count()):

            widget = self.layout.itemAt(i).widget()
            
            if isinstance(widget, SingleField):
                widget.ready_to_input()

    def __get_answer_list(self):
        
        answer_list = []
        
        for i in range(self.layout.count()):

            # self.layout.itemAt(i) -> QWidgetItem
            widget = self.layout.itemAt(i).widget()
            
            if isinstance(widget, SingleField):
                answer_list.append( widget.toPlainText().strip() )
        return answer_list
        
    def start_correction(self, failed_position_list):      

        answer_list=self.__get_answer_list()              

        # complite the number of words if missing in both direction
        # finally we get same number of answers and questions
        zipped_list=list(zip( 
            answer_list + ["_"*len(i) for i in self.good_answer_list][len(answer_list):], 
            self.good_answer_list + [" "*len(i) for i in answer_list][len(self.good_answer_list):] 
        ) )

        # complite the length of the answers if they shorter than the good answer
        completed_answer=[i[0] + ("_"*len(i[1]))[len(i[0]):] for i in zipped_list]

        # go trough the answer and the failed_position_list pairs        
        word_failed_position_pair_list = list(zip( completed_answer, failed_position_list ))

        # trough the widgets in the layout
        for i in range(self.layout.count()):

            # self.layout.itemAt(i) -> QWidgetItem
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, SingleField):

                # if the i. list in the failed_position_list is not empty
                #if failed_position_list[i]:
                if True: #word_failed_position_pair_list[i][1]:
                    # then we need to show the difference

                    # start the single field correnction
                    # remove the text from the field
                    # disable field
                    widget.ready_to_correction()

                    # go trough all characters in the widget
                    for pos in range(len(word_failed_position_pair_list[i][0])):

                        if pos in word_failed_position_pair_list[i][1]:
                            
                            # font basic_color and background basic_color
                            #palette = QPalette()
                            #palette.setColor(QPalette.Text, Qt.red)
                            #palette.setColor(widget.backgroundRole(), AnswerField.FONT_BG)                            
                            #widget.setPalette( palette )
                            widget.append_fail(word_failed_position_pair_list[i][0][pos])

                          
                        #    sys.stdout.write(type(self).COLOR_CORRECTION_WRONG)
                        else:
                            #palette = QPalette()
                            #palette.setColor(QPalette.Text, Qt.green)
                            #palette.setColor(widget.backgroundRole(), AnswerField.FONT_BG)                            
                            #widget.setPalette( palette )
                            widget.append_pass(word_failed_position_pair_list[i][0][pos])
                        
                        #print(word_failed_position_pair_list[i][0][pos])
                        
                        #widget.insert(word_failed_position_pair_list[i][0][pos])

    def set_fields(self, good_answer_list):

        self.good_answer_list=good_answer_list

        self.layout=QHBoxLayout()
        self.layout.setSpacing(1)
        
        for i in good_answer_list:
            self.layout.addWidget( self.getSingleField(i) )
        self.layout.addStretch(10)
        self.setLayout(self.layout)

    def getSingleField(self, word):
        return SingleField(len(word), AnswerField.FONT_BASIC_SIZE, AnswerField.FONT_BASIC_COLOR, self.bg)

class GoodAnswerField(AnswerField):
    FONT_SIZE = 15
    FONT_COLOR = Qt.red
    def __init__(self, word_list, bg):
        self.word_list=word_list
        self.bg=bg
        super().__init__(word_list, bg)
        
    def getSingleField(self, word):
        sf = SingleField(len(word), GoodAnswerField.FONT_SIZE, GoodAnswerField.FONT_COLOR, self.bg)
        sf.setEnabled(False)
        return sf

    def show_text(self):
        j=0
        for i in self.word_list:
            widget=self.layout.itemAt(j).widget()
            widget.setText( i )
            j += 1

class SingleField(QTextEdit):

    state = Enum(
        INPUT=0,
        CORRECTION=1
    )

    def __init__(self, length, basic_size, basic_color, background):
        super().__init__()

        self.single_field_correction = None

        self.length = length
        self.basic_size=basic_size
        self.basic_color=basic_color
        self.background=background

        self.setFrameStyle(QFrame.NoFrame)
          
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # font, colors
        self.__set_basic_font()

        # height
        self.setFixedHeight(self.fontMetrics().height() + 3)

        # widht of 'W'
        self.setFixedWidth(self.fontMetrics().width("W" * length) + 10)

        self.ready_to_input()

        self.textChanged.connect(self.changed_text)

    def keyPressEvent(self, event):
        key = event.key()
        if key in [ Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab ]:
            self.parent().focusNextChild()
        else:
            QTextEdit.keyPressEvent(self, event)
    

    def changed_text(self):
        
        if len(self.toPlainText()) > self.length:
            self.setPlainText( self.toPlainText().strip()[0:self.length] )
        
            cursor = self.textCursor()
            cursor.setPosition(self.length)
            self.setTextCursor(cursor)

        print(self.toPlainText())

    def __set_basic_font(self):
       
        # monospace font - basic_size:15 Bold
        self.setFont(QFont("Courier New",pointSize=self.basic_size, weight=QFont.Bold))

        # font basic_color and background basic_color
        palette = self.palette()
        #palette = self.viewport().palette() # QPalette()
        palette.setColor(QPalette.Text, self.basic_color)
        palette.setColor(self.backgroundRole(), self.background)
        self.setPalette( palette )

    def ready_to_correction(self):
        self.setEnabled( False )
        self.clear()
        self.state=SingleField.state.CORRECTION

    def ready_to_input(self):
        self.setEnabled( True )
        self.clear()
        self.state=SingleField.state.INPUT

    def append_pass( self, text ):
        if self.state == SingleField.state.CORRECTION:
            self.setTextColor(Qt.green)
            self.setTextBackgroundColor(self.background)
            self.insertPlainText(text)

    def append_fail( self, text ):
        if self.state == SingleField.state.CORRECTION:
            self.setTextColor(Qt.red)
            self.setTextBackgroundColor(self.background)            
            self.insertPlainText(text)

    
class __SingleField(QLineEdit):
        def __init__(self, length, basic_size, basic_color, background):
            QLineEdit.__init__(self)
            
            # monospace font - basic_size:15 Bold
            self.setFont(QFont("Courier New",pointSize=basic_size, weight=QFont.Bold))

            # font basic_color and background basic_color
            palette = QPalette()
            palette.setColor(QPalette.Text, basic_color)
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
    
    
