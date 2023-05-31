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
            "pathOfEncryptedSymmKeyToSave": "Empty",
            "pathOfPublicKeyToSave": "Empty",
            "pathOfPrivateKeyToSave": "Empty",
            "pathOfDataToGet": "Empty",
            "pathOfPrivateKeyToGet1": "Empty",
            "pathOfEnctyptedSymmKeyToGet1": "Empty",
            "pathOfEncryptedDataToSave": "Empty",
            "pathOfEncryptedDataToGet": "Empty",
            "pathOfPrivateKeyToGet2": "Empty",
            "pathOfEnctyptedSymmKeyToGet2": "Empty",
            "pathOfDataToSave": "Empty",
            "symmKey": 0,
            "publicKey": 0,
            "privateKey": 0,


            "pathToFolder": "Empty",
            "lastNum": "7819",
            "cardNum": 0,
            "stats": {},
            "defaultHash": "f56ab81d14e7c55304dff878c3f61f2d96c8ef1f56aff163320e67df",
            "bins": ["477932", "427714", "431417", "458450", "475791", "477714", "477964", "479087", "419540", "426101", "428905",
                     "428906", "458411", "458443", "415482"]
        }

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
        # tabs.addTab(self.__decryption_tab(), "DecryptionTab")
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
        text.addWidget(line1)
        text.addWidget(line2)
        layout.addLayout(text)
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
        first.addLayout(layoutPath)

        buttonCalculate = QPushButton("Calculate")
        buttonCalculate.setStyleSheet("background-color: red")
        buttonCalculate.clicked.connect(
            partial(self.calculate_num_card, buttonCalculate))
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

    def calculate_num_card(self, button: QPushButton):
        """the method launches a function to find 
        the card number for different pools"""
        # if (self.settings['pathToFolder'] != 'Empty' and self.settings['cardNum'] == 0) or (self.settings['pathToFolder'] != '' and self.settings['cardNum'] == 0):
        if (not (self.settings['pathToFolder'] == 'Empty' or self.settings['pathToFolder'] == '') and self.settings['cardNum'] == 0):
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
            self.settings['card_num'] = result
            # for i in range(0, 101):
            #     time.sleep(0.01)
            button.setStyleSheet("background-color: green;")
            return
        elif self.settings['pathToFolder'] == 'Empty' or self.settings['pathToFolder'] == '':
            QMessageBox.critical(
                self, "Error", "Please select folder", QMessageBox.Ok)
            return
        elif self.settings['cardNum'] != 0:
            QMessageBox.critical(
                self, "Error", "You have already done calculation", QMessageBox.Ok)
            return


    def create_graph(self, button: QPushButton):
        """the method create the histogram"""
        if (self.settings['stats']):

            self.graph.axes.cla()
            self.graph.axes.bar(self.settings['stats'].keys(), self.settings['stats'].values())
            button.setStyleSheet("background-color: green;")
            self.graph.draw()
        else:
            QMessageBox.critical(
                self, "Error", "Please finish previous step", QMessageBox.Ok)


    def card_num_verification(self, lable: QLabel, button: QPushButton):
        """the method calls the function of the luhn algorithm"""
        if(self.settings['cardNum']):
            result_algorithm = algorithm_luhn(str(self.settings["cardNum"]))
            lable.setText(f"Algorithm Luhn return - {result_algorithm}")
            button.setStyleSheet("background-color: green;")
        else:
            QMessageBox.critical(
                self, "Error", "Please finish previous step", QMessageBox.Ok)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
