import sys
from prala.common.common import getSetupIni
from prala.accessories import _, Enum, PicButton, getConfigIni
from prala.core import FilteredDictionary
from prala.core import Record
from prala.accessories import Property
from prala.exceptions import EmptyDictionaryError
from prala.exceptions import NoDictionaryError

from threading import Thread

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QGridLayout, QFrame, QMainWindow,
    QLabel, QPushButton, QLineEdit, QApplication, QHBoxLayout, QTextEdit,
    QDesktopWidget, QSizePolicy)
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtCore import Qt, QSize, QEvent
from PyQt5.QtGui import QPixmap, QIcon, QPalette
from pkg_resources import resource_string, resource_filename

class GuiPrala(QMainWindow):

    def __init__(self, file_name, base_language, learning_language, part_of_speech_filter="", extra_filter="", say_out=True, show_pattern=True, show_note=True):

        super().__init__()

        central_widget = CentralWidget( self, file_name, base_language, learning_language, part_of_speech_filter, extra_filter, say_out, show_pattern, show_note)
        self.setCentralWidget( central_widget )

        self.resize(500, 150)
        self.statusBar().showMessage("")
        self.center()
        setup = getSetupIni()
        self.setWindowTitle( setup['title'] + " - " + setup['version'])
        self.show()

    def center(self):
        """Aligns the window to middle on the screen"""
        fg=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

class CentralWidget(QWidget):
    
    def __init__(self, main_gui, file_name, base_language, learning_language, part_of_speech_filter="", extra_filter="", say_out=True, show_pattern=True, show_note=True):
        super().__init__()
        
        self.main_gui = main_gui

        self.myFilteredDictionary=FilteredDictionary(file_name, base_language, learning_language, part_of_speech_filter, extra_filter) 
        self.say_out=say_out
        self.show_pattern=show_pattern
        self.show_note=show_note

        self.initUI()
        
        self.round()
        
    def initUI(self):        
                
        # --------------------
        # Fields
        # --------------------
        #
        
        good_answer=[""]

        self.pos_field=TextLabel("", font_size=10, font_color=Qt.gray)

        self.question_field=TextLabel("", font_size=13, font_color=QColor(212, 140, 95))

        self.note_field=TextLabel("", font_size=10, font_color=Qt.gray, font_bold=True, font_italic=True)

        self.answer_field=AnswerField(good_answer, bg=self.palette().color(QPalette.Background))

        self.good_answer_field=ExpectedAnswerField(good_answer, bg=self.palette().color(QPalette.Background))

        self.result_lamp=ResultWidget(failed_position_list=None)

        self.ok_button = self.getOKButton()

        # --------------------
        # general grid setting
        # --------------------
        #
        grid=QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(1)      # space between the fields

        # --------------------
        # Fields location
        # --------------------

        fields_columns=4

        # PART OF SPEECH field
        grid.addWidget( self.pos_field, 0, 0, 1, fields_columns )

        # QUESTION field
        grid.addWidget( self.question_field, 1, 0, 1, fields_columns-1 )

        # NOTE field
        grid.addWidget( self.note_field, 1, fields_columns-1, 1, 1 )

        # ANSWER field
        grid.addWidget( self.answer_field, 5, 0, 1, fields_columns-1)

        # EXPECTED ANSWER field
        grid.addWidget( self.good_answer_field, 6, 0, 1, fields_columns-1 )

        # OK buttn
        grid.addWidget( self.ok_button, 5, fields_columns-1, 1, 1, Qt.AlignCenter )

        # RESULT lamp
        grid.addWidget( self.result_lamp, 6, fields_columns-1, 1, 1, Qt.AlignCenter )

        self.setGeometry(300, 300, 450, 150)
        self.setWindowTitle(_("TITLE_WINDOW"))    
        self.show()

    def showStat(self):
        overall=self.myFilteredDictionary.get_recent_stat_list()                    
                    
        good = str(overall[1])
        all = str(overall[0])
        remains = str(overall[2]) if overall[2] > 0 else ""
        success = str(int(100 * overall[1] / overall[0])) + "%"
        recent_stat = self.record.get_recent_stat()
        sequence =  ", ".join( [str(i) for i in recent_stat])
        points = str(self.myFilteredDictionary.get_points(recent_stat))


        message = good + "/" + all + ("/" + remains if len(remains.strip()) > 0 else "") + " | " + success + " | " + points + " | " + sequence  
        self.main_gui.statusBar().showMessage( message )
        
    def round( self, wrong_record=None ):
        """
            Frame of asking word.
            The other part of hte round is in the OKButton's on_click() method

            -calculates the the new word to ask
            -fill up the POS field
            -fill up the QUESTION field
            -fill up the ANSWER field
            -fill up the EXPECTED ANSWER field
            -say out the question
            -waiting for the user response

            Input
                wrong_record
                    - It is unrelevant until all words was answerd
                    - If it is EMPTY then the chance depends on the points
                    - If it is NOT EMPTY the the same question will be asked until it answered
            
        """
        
        # hides the result lamp
        self.result_lamp.set_result(None)

        self.record = self.myFilteredDictionary.get_next_random_record(wrong_record)

        # pos field
        self.pos_field.setText(self.record.part_of_speach)

        good_answer = self.record.learning_words

        # question
        self.question_field.setText( self.record.base_word )

        # note field
        if self.show_note:
            self.note_field.setText(self.record.note)

        # answer
        self.answer_field.setExpectedWordList( good_answer )

        # expected answer
        self.good_answer_field.setExpectedWordList( good_answer )

        # say out the question in a thread
        if self.say_out:
            Thread(target = self.record.say_out_base, args = ()).start()

    def getOKButton( gui_object ):

        class OKButton(PicButton):
            STATUS = Enum(
                ACCEPT = 0,
                NEXT = 1
            )

            def __init__(self, gui_object):
                self.gui_object = gui_object

                ok_button_pixmap = QPixmap(resource_filename(__name__, "/".join(("images", "ok-button.png"))))        
                ok_button_hover_pixmap = QPixmap(resource_filename(__name__, "/".join(("images", "ok-button-hover.png"))))
                ok_button_focus_pixmap = QPixmap(resource_filename(__name__, "/".join(("images", "ok-button-focus.png"))))        
                ok_button_pressed_pixmap = QPixmap(resource_filename(__name__, "/".join(("images", "ok-button-pressed.png"))))   
                super().__init__(ok_button_pixmap, ok_button_focus_pixmap, ok_button_hover_pixmap, ok_button_pressed_pixmap)

                self.clicked.connect(self.on_click)
                self.status = OKButton.STATUS.ACCEPT

            def on_click(self):
                
                if self.status == OKButton.STATUS.ACCEPT:
        
                    gui_object.answer_field.disableText()

                    # shows the difference between the the answer and the good answer -> tuple
                    # [0] -> False/True
                    # [1] -> list of list of thedisable positions of the difference in the words
                    self.result=gui_object.record.check_answer(gui_object.answer_field.getFieldsContentList())

                    # write back the stat
                    gui_object.myFilteredDictionary.add_result_to_stat(gui_object.record.word_id,self.result[0])

                    # show the result in green/red lamp
                    if self.result[0]:
                        gui_object.result_lamp.set_result(True)
                    else:
                        gui_object.result_lamp.set_result(False)

                    # shows the expected answer with differences
                    gui_object.good_answer_field.showText(self.result[1], gui_object.answer_field.getFieldsContentList())

                    # shows statistics
                    gui_object.showStat()

                    self.status = OKButton.STATUS.NEXT
            
                    # say out the right answer in thread          
                    if gui_object.say_out:
                        Thread(target = gui_object.record.say_out_learning, args = ()).start()

                elif self.status == OKButton.STATUS.NEXT:

                    self.status  = OKButton.STATUS.ACCEPT

                    # shows statistics
                    gui_object.showStat()

                    # starts a new round
                    gui_object.round( None if self.result[0] else gui_object.record )

  

        return OKButton(gui_object)


class TextLabel(QLabel):
    FONT_SIZE = 12
    FONT_COLOR = Qt.black
    FONT_NAME = "Courier New"
    FONT_BOLD = False
    FONT_ITALIC=True

    def __init__(self, text, font_name=None, font_size=None, font_color=None, font_bold=None, font_italic=None):
        super().__init__()        

        if font_name is None:
            self.font_name = TextLabel.FONT_NAME
        else:
            self.font_name = font_name
        if font_size is None:
            self.font_size = TextLabel.FONT_SIZE
        else:
            self.font_size = font_size
        if font_color is None:
            self.font_color = TextLabel.FONT_COLOR
        else:
            self.font_color = font_color
        if font_bold is None:
            self.font_bold = TextLabel.FONT_BOLD
        else:
            self.font_bold = font_bold
        if font_italic is None:
            self.font_italic = TextLabel.FONT_ITALIC
        else:
            self.font_italic = font_italic
 
        # font type
        #self.setFont(QFont(self.font_name,pointSize=self.font_size, weight=QFont.Bold))
        font = QFont(self.font_name,pointSize=self.font_size)
        font.setBold( self.font_bold)
        font.setItalic( self.font_italic )
        self.setFont( font )
        
        # font color
        palette = QPalette()
        palette.setColor(self.foregroundRole(), self.font_color)
        self.setPalette( palette )

        self.setText(text)

    def setText(self, text):
        super().setText(text)




class WordField(QWidget):
    FONT_SIZE = 15
    FONT_COLOR = Qt.black
    FONT_BG = Qt.white
    SPACE = 2

    def __init__(self, word, font_size=None, font_color=None, font_bg=None):
        super().__init__()        
        
        if font_size is None:
            self.font_size = WordField.FONT_SIZE
        else:
            self.font_size = font_size
        if font_color is None:
            self.font_color = WordField.FONT_COLOR
        else:
            self.font_color = font_color
        if font_bg is None:
            self.font_bg = WordField.FONT_BG
        else:
            self.font_bg = font_bg

        # Set layout
        layout = QHBoxLayout()
        layout.setSpacing(WordField.SPACE)
        self.setLayout(layout)

        self.setWord(word)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def __clear_layout(self, layout):
        
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.__clear_layout(item.layout())

    def __get_single_field(self, word):
        """
        Returns the empty SingleField of the specific part of the word
        with the right length, font size, basic_bg for inside use
        """
        return SingleField(len(word), size=self.font_size, color=self.font_color, bg=self.font_bg)

    def setWord(self, word):
        """
        Every time when it is called, a new layout will be generated
        """

        # saves the word
        self.__word = word
    
        # remove all widgets
        self.__clear_layout(self.layout())
          
        # place an empty SingelField
        self.layout().addWidget( self.__get_single_field(word) )

        # add an Strech to the end
        self.layout().addStretch(10)

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
        Clears and Enables all fields to edit
        """
        for widget in self.getFieldIterator():
            widget.clear()
            widget.setEnabled( True )

    def getWord(self):
        """
        Returns the set word
        """
        return self.__word
    
    def getFieldsContentList(self):
        """
        Returns the contents of the fields in a list if it was modified by user
        """
        fields_content_list = []
        
        for widget in self.getFieldIterator():
            
            # adds the text from the field to the list
            fields_content_list.append( widget.toPlainText().strip() )

        return fields_content_list

    def getFieldIterator(self):
        """
        Returns the SingleField widgets
        """
        for widget in self.children():
            if isinstance(widget, SingleField):
                yield widget



class AnswerField(QWidget):
    FONT_BASIC_SIZE = 15
    FONT_BASIC_COLOR = Qt.blue
    FONT_BG = Qt.white

    def __init__(self, expected_word_list, bg):
        super().__init__()        
        
        self.__bg = bg
        
        layout = QHBoxLayout()
        layout.setSpacing(2)
        self.setLayout(layout)

        self.setExpectedWordList(expected_word_list)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def __clear_layout(self, layout):
        
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.__clear_layout(item.layout())

    def setExpectedWordList(self, expected_word_list):
        """
        Every time when it is called, a new layout will be generated
        """

        self.__expected_word_list = expected_word_list
    
        # remove all widgets
        self.__clear_layout(self.layout())
          
        for i in expected_word_list:
            self.layout().addWidget( self._get_single_field(i) )

        self.layout().addStretch(10)
        #print("children: ", self.layout().count(),  self.__class__.__name__)
        

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
        Clears and Enables all fields to edit
        """
        for widget in self.getFieldIterator():
            widget.clear()
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
        #print("children: ", self.children())
        #for i in range(self.layout.count()):
        for widget in self.children():
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
        for i in range(self.layout().count()):

            # self.layout.itemAt(i) -> QWidgetItem
            widget = self.layout().itemAt(i).widget()
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
    
    def changed_text(self):
        
        if len(self.toPlainText()) > self.length:
            self.setPlainText( self.toPlainText().strip()[0:self.length] )
        
            cursor = self.textCursor()
            cursor.setPosition(self.length)
            self.setTextCursor(cursor)

        #print(self.toPlainText())

    
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


def main():    
    app = QApplication(sys.argv)

    par = getConfigIni()
 
    try:
        ex = GuiPrala(
        par['file_name'], 
        par['base_language'], 
        par['learning_language'], 
        part_of_speech_filter=par['part_of_speech_filter'], 
        extra_filter=par['extra_filter'], 
        say_out=par['say_out'], 
        show_pattern=par['show_pattern'], 
        show_note=par['show_note']
        )
    except EmptyDictionaryError as e:
        print("------------------------")
        print("Error: ")
        print( e, "\n   File name: " + e.dict_file_name, "\n   Part of speech: " + e.part_of_speach, "\n   Extra filter: " + e.extra_filter )
        print("------------------------")
        exit(-1)

    except NoDictionaryError as f:
        print("------------------------")
        print("Error: ")
        print(f.dict_message + ": ", f.dict_file_name)
        print()
        res=input("Do you want me to generate '" + f.dict_file_name + "' dict file (Y/[n])?")
        if res.strip() == "Y":
            temp_dict_path="/".join(("templates", ConsolePrala.TEMPLATE_DICT_FILE_NAME))
            binary_content=resource_string(__name__, temp_dict_path)
            with open(f.dict_file_name, "w") as f:
                print(binary_content.decode("utf-8"), file=f)
        print("------------------------")
        exit(-1)



    sys.exit(app.exec_())
    
   
 
