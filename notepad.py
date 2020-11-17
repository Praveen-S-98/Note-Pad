from PyQt5.QtWidgets import (QApplication, QMainWindow, QPlainTextEdit, QMenuBar, QAction,
                             QFileDialog, QMessageBox, QPushButton, QHBoxLayout, QWidget, QFrame)
import sys
from PyQt5.QtGui import QFont, QFontDatabase, QIcon, QColor
from PyQt5 import QtCore


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "untitled ~(Notepad-praveen)"
        self.left = 700
        self.top = 100
        self.width = 400
        self.height = 400
        self.path = None
        self.setWindowIcon(QIcon("logo.png"))
        self.setStyleSheet(
            "background-color: SkyBlue;")

        self.initWindow()

    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Defing Actions for Mainmenu
        openFile = QAction("Open", self)
        openFile.setShortcut("Ctrl+o")
        openFile.setIcon(QIcon("open.png"))
        openFile.triggered.connect(self.openFileMethod)

        saveFile = QAction("Save", self)
        saveFile.setShortcut("Ctrl+s")
        saveFile.setIcon(QIcon("save.png"))
        saveFile.triggered.connect(self.saveFileMethod)

        saveAs = QAction("SaveAs...", self)
        saveAs.setIcon(QIcon("saveas.png"))
        saveAs.triggered.connect(self.file_saveas)

        closeFile = QAction("Close", self)
        closeFile.setShortcut("Ctrl+w")
        closeFile.setIcon(QIcon("close.png"))
        closeFile.triggered.connect(self.closeFileMethod)

        quitFile = QAction("Quit", self)
        quitFile.setShortcut("Ctrl+q")
        quitFile.setIcon(QIcon("quit.png"))
        quitFile.triggered.connect(self.quitFileMethod)

        copy = QAction("Copy", self)
        copy.setShortcut("Ctrl+c")
        copy.setIcon(QIcon("copy.png"))
        copy.triggered.connect(self.copyMethod)

        cut = QAction("Cut", self)
        cut.setShortcut("Ctrl+x")
        cut.setIcon(QIcon("cut.png"))
        cut.triggered.connect(self.cutMethod)

        paste = QAction("Paste", self)
        paste.setShortcut("Ctrl+v")
        paste.setIcon(QIcon("paste.png"))
        paste.triggered.connect(self.pasteMethod)

        redo = QAction("Redo", self)
        redo.setShortcut("Shift+Ctrl+z")
        redo.setIcon(QIcon("redo.jpg"))
        redo.triggered.connect(self.redoMethod)

        undo = QAction("Undo", self)
        undo.setShortcut("Ctrl+z")
        undo.setIcon(QIcon("undo.jpg"))
        undo.triggered.connect(self.undoMethod)

        # Creating MainMenu
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        mainMenu.setFont(QFont("sanserif", 11))
        mainMenu.setStyleSheet(
            "QMenuBar::hover"
                             "{"
                             "background-color : lightgreen;"
                             "}"
        )

        # Creating MenuBars
        fileMenu = mainMenu.addMenu(" &File")
        fileMenu.setFont(QFont("sanserif", 11))
        fileMenu.addAction(openFile)
        fileMenu.addSeparator()
        fileMenu.addAction(saveFile)
        fileMenu.addSeparator()
        fileMenu.addAction(saveAs)
        fileMenu.addSeparator()
        fileMenu.addAction(closeFile)
        fileMenu.addSeparator()
        fileMenu.addAction(quitFile)

        editMenu = mainMenu.addMenu(" &Edit")
        editMenu.setFont(QFont("sanserif", 11))
        editMenu.addAction(copy)
        editMenu.addSeparator()
        editMenu.addAction(cut)
        editMenu.addSeparator()
        editMenu.addAction(paste)
        editMenu.addSeparator()
        editMenu.addAction(redo)
        editMenu.addSeparator()
        editMenu.addAction(undo)


        layout = QHBoxLayout()
        self.text = QPlainTextEdit()
        self.text.setStyleSheet(
            "background-color: white; border:4px solid rgb(105,105,105)")

        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.text.setFont(fixedfont)


        layout.addWidget(self.text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.show()

    # Creating Methods for QActions
    def openFileMethod(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Text documents (*.txt);All files (*.*)")

        if path:
            try:
                with open(path, 'rU') as f:
                    text = f.read()

            except Exception as e:
                print(str(e))

            else:
                self.path = path
                self.text.setPlainText(text)
                self.update_title()

    def saveFileMethod(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        self._save_to_path(self.path)

    def file_saveas(self):
        filedialog = QFileDialog()
        self.path, _ = filedialog.getSaveFileName(
            self, "Save file", "Untitled", "Text documents (*.txt);All files (*.*)")

        if not self.path:
            return
        self._save_to_path(self.path)

    def _save_to_path(self, path):
        text = self.text.toPlainText()
        try:
            with open(path, "w+") as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.update_title()

    def closeFileMethod(self):
        msg_box = QMessageBox()
        msg_box.setText("Do You Want To Save The Changes ?")
        msg_box.setFont(QFont("Helvetica [Cronyx]", 12, QFont.DemiBold))
        msg_box.setGeometry(QtCore.QRect(
            self.left, 300, self.width, self.height))
        msg_box.addButton(QPushButton("yes"), QMessageBox.YesRole)
        msg_box.addButton(QPushButton("Close Without Saving"),
                          QMessageBox.RejectRole)
        msg_box.addButton(QPushButton("No"), QMessageBox.NoRole)
        msg_box.setStyleSheet("QPushButton::hover"
                              "{"
                              "background-color : Cyan"
                              "}")
        retval = msg_box.exec_()
        if retval == 0:
            print("entering here")
            self.saveFileMethod()
            self.text.clear()
            self.setWindowTitle("~Untitled")
        elif retval == 2:
            msg_box.Cancel
        elif retval == 1:
            self.text.clear()
            self.setWindowTitle("~Untitled")

    def quitFileMethod(self):
        App.exit()

    def copyMethod(self):
        self.text.copy()

    def cutMethod(self):
        self.text.cut()

    def pasteMethod(self):
        self.text.paste()

    def redoMethod(self):
        self.text.redo()

    def undoMethod(self):
        self.text.undo()

    def update_title(self):
        temp_path = str(self.path)[::-1]
        fileName = " "
        for i in str(temp_path):
            if i != '/':
                fileName = fileName + i
            else:
                break
        newFileName = str(fileName)[::-1]
        self.setWindowTitle("~"+newFileName)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
