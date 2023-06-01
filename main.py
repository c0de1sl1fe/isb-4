import sys
from functools import partial
import time
from PyQt5.QtWidgets import (QFrame, QShortcut, QWidget, QLabel,  QPushButton,
                             QApplication, QHBoxLayout,
                             QFileDialog, qApp, QDesktopWidget, QMessageBox,
                             QTabWidget, QVBoxLayout, QProgressBar)
from PyQt5.QtGui import QIcon,  QFont, QKeySequence
import multiprocessing as mp
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import json
import logging
from utils import find_num_card, algorithm_luhn


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Window(QWidget):
    def __init__(self) -> None:
        """Constructor"""
        super().__init__()
        self.init_UI()

    def init_UI(self) -> None:
        """support constructor function"""
        self.shortcut_exit = QShortcut(QKeySequence('esc'), self)
        self.shortcut_exit.activated.connect(qApp.quit)
        self.settings = {
            "pathToFolder": "Empty",
            "lastNum": "",
            "cardNum": 0,
            "stats": {},
            "luhn": "",
            "defaultHash": "",
            "bins": []
            # "lastNum": "7819",
            # "cardNum": 0,
            # "stats": {},
            # "luhn": "Empty",
            # "defaultHash": "f56ab81d14e7c55304dff878c3f61f2d96c8ef1f56aff163320e67df",
            # "bins": ["477932", "427714", "431417", "458450", "475791", "477714", "477964", "479087", "419540", "426101", "428905",
            #          "428906", "458411", "458443", "415482"]
        }
        self.isOldFlag = False
        self.isLoaded = False
        self.pbar = QProgressBar(self)
        self.graph = MplCanvas(self, width=11, height=10, dpi=100)

        self.setWindowTitle('Lab4')
        self.setWindowIcon(QIcon('6112_Logo_git_prefinal.jpg'))
        layout = QVBoxLayout()
        self.setLayout(layout)
        tabs = QTabWidget()
        tabs.addTab(self.__general_tab(), "general")
        tabs.addTab(self.__card_number(), "Card number tab")
        tabs.addTab(self.__additional(), "Additional functions tab")
        layout.addWidget(tabs)
        self.setGeometry(400, 400, 450, 400)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.show()

    def __general_tab(self) -> QWidget:
        """main window with hello-words and descripition what's going on"""
        custom_font = QFont()
        custom_font.setPixelSize(40)
        generalTab = QWidget()
        layout = QVBoxLayout()
        text = QVBoxLayout()
        line1 = QLabel("Hello there!")
        line1.setFont(custom_font)
        custom_font.setPixelSize(20)
        line2 = QLabel('''At CardNumber you can word with
                        \nAt additional tab you can:\n - 1: Create histogram\n - 2: Check your card number with Lunh's algorithm''')
        line2.setFont(custom_font)
        buttonToSaveSettings = QPushButton("SaveSettings")
        buttonToSaveSettings.clicked.connect(partial(self.__settings, buttonToSaveSettings))
        
        text.addWidget(line1)
        text.addWidget(line2)
        layout.addLayout(text)
        layout.addWidget(buttonToSaveSettings)
        generalTab.setLayout(layout)
        return generalTab

    def __card_number(self) -> QWidget:
        """card number tab with information about card and some functions"""
        generalTab = QWidget()
        layout = QVBoxLayout()
        first = QVBoxLayout()
        second = QHBoxLayout()
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setLineWidth(2)
        layoutPath = QHBoxLayout()
        binlayout1 = QVBoxLayout()
        binlayout2 = QVBoxLayout()
        binlayout = QHBoxLayout()
        binlayout1.setSpacing(0)
        binlayout.setSpacing(0)
        binlayout.setContentsMargins(10, 10, 10, 100)
        for i in range(0, int(len(self.settings['bins'])/2)):
            binlayout1.addWidget(
                QLabel(f"{i + 1}. {self.settings['bins'][i]}\n"))
        for i in range(int(len(self.settings['bins'])/2), len((self.settings['bins']))):
            binlayout2.addWidget(
                QLabel(f"{i + 1}. {self.settings['bins'][i]}\n"))
        binlayout.addLayout(binlayout1)
        binlayout.addLayout(binlayout2)
        button = QPushButton("Path")
        line11 = QLabel(self.settings['pathToFolder'])
        line11.setStyleSheet("border: 3px solid red;")
        layoutPath.addWidget(button)
        layoutPath.addWidget(line11)
        button.clicked.connect(
            partial(self.__input_path, self.settings, "pathToFolder", line11))
        first.addLayout(binlayout)
        first.addWidget(
            QLabel(f"Last numbers of card: {self.settings['lastNum']}"))
        cardNumLable = QLabel("")
        first.addWidget(cardNumLable)
        first.addLayout(layoutPath)

        buttonCalculate = QPushButton("Calculate")
        buttonCalculate.setStyleSheet("background-color: red")
        buttonCalculate.clicked.connect(
            partial(self.calculate_num_card, cardNumLable, buttonCalculate))
        second.addWidget(buttonCalculate)
        second.addWidget(self.pbar)
        layout.addLayout(first)
        layout.addWidget(separator)
        layout.addLayout(second)
        generalTab.setLayout(layout)
        return generalTab

    def __additional(self) -> QWidget:
        """tab with additional function such as draw hish and check card"""
        generalTab = QWidget()
        layout = QVBoxLayout()
        first = QVBoxLayout()
        first.addWidget(self.graph)
        cardStatusLable = QLabel("None")
        first.addWidget(cardStatusLable)
        second = QHBoxLayout()
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setLineWidth(2)
        button1 = QPushButton("Create histogram")
        button1.setStyleSheet("background-color: red")
        second.addWidget(button1)
        button1.clicked.connect(partial(self.create_graph, button1))
        button2 = QPushButton("Check card")
        button2.setStyleSheet("background-color: red")
        button2.clicked.connect(
            partial(self.card_num_verification, cardStatusLable, button2))
        second.addWidget(button2)
        layout.addLayout(first)
        layout.addWidget(separator)
        layout.addLayout(second)
        generalTab.setLayout(layout)
        return generalTab

    def __input_path(self, settings: tuple, key: str, lable: QLabel) -> None:
        """service function"""
        settings[key] = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if (settings[key] == ''):
            return
        if not settings[key]:
            QMessageBox.critical(
                self, "Error", "please select dir", QMessageBox.Ok)

        else:
            lable.setText(settings[key])
            lable.setStyleSheet("border: 3px solid green;")

    def __input_file(self, settings: tuple, key: str,  lable: QLabel, typeCheck: str) -> None:
        """service function"""
        settings[key] = QFileDialog.getOpenFileName(self, 'Select Folder')[0]
        if (settings[key] == ''):
            return
        if not typeCheck in settings[key] and settings[key] != '':
            QMessageBox.critical(
                self, "Error", f"select correct file type - {typeCheck}", QMessageBox.Ok)
        else:
            lable.setText(settings[key])
            lable.setStyleSheet("border: 3px solid green;")

    def calculate_num_card(self, lable: QLabel, button: QPushButton):
        """the method launches a function to find 
        the card number for different pools"""
        if (self.isOldFlag and self.isLoaded):
            pools = mp.cpu_count()
            result = 0
            self.pbar.reset()
            for i in range(1, pools + 1):
                self.pbar.setValue(int(i/(pools)*100))
                start_time = time.time()
                result = find_num_card(
                    self.settings['defaultHash'],
                    self.settings['bins'],
                    self.settings['lastNum'], pools)
                final_time = time.time() - start_time
                self.settings['stats'][i] = final_time
            self.settings['cardNum'] = result
            lable.setText(str(self.settings['cardNum']))
            button.setStyleSheet("background-color: green;")
            self.isOldFlag = False
            return
        elif(not self.isOldFlag):
            QMessageBox.critical(
                self, "Error", "You have already done calculation", QMessageBox.Ok)
            return
        else:
            QMessageBox.critical(
                self, "Error", "Please load data", QMessageBox.Ok)
            return

    def create_graph(self, button: QPushButton):
        """the method create the histogram"""
        if (not self.isOldFlag and self.settings['stats']):

            self.graph.axes.cla()
            self.graph.axes.bar(
                self.settings['stats'].keys(), self.settings['stats'].values())
            button.setStyleSheet("background-color: green;")
            self.graph.draw()
        else:
            QMessageBox.critical(
                self, "Error", "Please finish previous step", QMessageBox.Ok)

    def card_num_verification(self, lable: QLabel, button: QPushButton):
        """the method calls the function of the luhn algorithm"""
        if (self.settings['cardNum'] and not self.isOldFlag):
            result_algorithm = algorithm_luhn(str(self.settings["cardNum"]))
            lable.setText(f"Algorithm Luhn return - {result_algorithm}")
            self.settings['luhn'] = f"Algorithm Luhn return - {result_algorithm}"
            button.setStyleSheet("background-color: green;")
        elif(not self.isOldFlag):
            QMessageBox.critical(
                self, "Error", "You have already done it", QMessageBox.Ok)
        else:
            QMessageBox.critical(
                self, "Error", "Please finish previous step", QMessageBox.Ok)

    def __settings(self, button: QPushButton):
        if(self.settings['pathToFolder'] != "Empty" and self.settings['pathToFolder' != ""]):
            if (not self.isLoaded):
                button.setText("saveSettings")
                try:
                    with open('settings.json', 'r') as f:
                        self.settings = json.load(f)
                    self.isOldFlag = True
                    self.isLoaded = True
                except Exception as e:
                    logging.error(
                        f"an error occurred when reading data to 'settings.json' file: {str(e)}")
            else:
                try:
                    with open('settings.json', 'w') as f:
                        json.dump(self.settings, f)
                except Exception as e:
                    logging.error(
                        f"an error occurred when reading data to 'settings.json' file: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
