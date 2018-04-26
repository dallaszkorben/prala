import sys
#from prala.accessories import _
from PyQt5.QtWidgets import QToolTip, QMainWindow, QPushButton, QApplication, QMessageBox, QDesktopWidget, QAction, QMenu
from PyQt5.QtGui import QFont    

class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):        
                
        # --- Status bar ---
        self.statusBar().showMessage('Ready')

        # --- Button ---
        btn = QPushButton('Change Status', self)
        btn.clicked.connect(self.on_click)
        QToolTip.setFont(QFont('SansSerif', 10))
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())        
        btn.move(50, 50)   

        # --- Menu ---
        # main menu
        # File
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        # sub menus        
        # File-Import
        importMenu = QMenu('&Import', self)  
        fileMenu.addMenu(importMenu)
        
        # File-Quit
        quitAct = QAction('&Quit', self)
        quitAct.triggered.connect(QApplication.instance().quit)
        fileMenu.addAction(quitAct)

        # File-Import-Import mail
        impMailAct = QAction('Import &Mail', self)
        importMenu.addAction(impMailAct)

        # --- Window ---
        self.setWindowTitle('Tooltips')    
        self.setGeometry(300, 300, 300, 200)
        self.center()
        self.show()    

    def on_click(self):
        self.statusBar().showMessage('Status changed')

    def closeEvent(self, event):
        """This method is called when the window is about to close"""    

        # --- Message Box ---        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()   

    def center(self):
        """Aligns the window to middle on the screen"""
        fg=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())



def main():    
    #ex = Example()
    #sys.exit(app.exec_())
    #app = QApplication(sys.argv)

    from prala.accessories import _
    print(_("MUST_BE_TRANSLATED"))
    print(_("ANOTHER_TRANSLATION"))
