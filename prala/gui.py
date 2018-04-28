import sys
from prala.accessories import _
#from PyQt5.QtWidgets import QToolTip, QMainWindow, QPushButton, QApplication, QMessageBox, QDesktopWidget, QAction, QMenu
#from PyQt5.QtGui import QFont    

from PyQt5.QtWidgets import (QWidget, QGridLayout, 
    QLabel, QPushButton, QLineEdit, QApplication,
    )
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets


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
        question_title=QLabel(_("TITLE_QUESTION"))
        question_field=QLabel("here is the question")

        resource_path="/".join(("images", "red-light.png"))
        binary_content=resource_filename(__name__, resource_path)
        pixmap = QPixmap(binary_content)        
        pixmap = pixmap.scaled(42, 42, Qt.KeepAspectRatio, Qt.FastTransformation)
        result_field=QLabel()
        result_field.setPixmap(pixmap)

        answear_title=QLabel(_("TITLE_ANSWEAR"))
        answear_field=QLineEdit()
        good_answear_field=QLabel("here is the good answer")

        ok_button=QPushButton(_("BUTTON_OK"))

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

        grid.addWidget( result_field, 2, fields_rows-1, 1, 1, Qt.AlignRight )

        grid.addWidget( answear_title, 4, 0, 1, fields_rows)
        grid.addWidget( answear_field, 5, 0, 1, fields_rows)
        grid.addWidget( good_answear_field, 6, 0, 1, fields_rows )
        #grid.addWidget( stat_, 7, 0, 1, fields_rows ) 
        grid.addWidget( stat_history, 8, 0, 1, fields_rows )


        self.setGeometry(300, 300, 450, 150)
        self.setWindowTitle(_("TITLE_WINDOW"))    
        self.show()

def main():    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    
    
