import sys
from functools import partial

from PyQt5.QtWidgets import (QFrame, QShortcut, QWidget, QLabel,  QPushButton,
                             QApplication, QHBoxLayout,
                             QFileDialog, qApp, QDesktopWidget, QMessageBox,
                             QTabWidget, QVBoxLayout)
from PyQt5.QtGui import QIcon,  QFont, QKeySequence



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
            "privateKey": 0
        }
        self.setWindowTitle('Lab4')
        self.setWindowIcon(QIcon('6112_Logo_git_prefinal.jpg'))
        layout = QVBoxLayout()
        self.setLayout(layout)
        tabs = QTabWidget()
        tabs.addTab(self.__general_tab(), "general")
        tabs.addTab(self.__generate_keys(), "GenKeys")
        tabs.addTab(self.__encryption_tab(), "EncryptionTab")
        tabs.addTab(self.__decryption_tab(), "DecryptionTab")
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
        line2 = QLabel('''At GenKeys you can generate and save keys:\n - 1.1: Generate key for symm alg\n - 1.2: Generate key for assym alg\n - 1.3: serializate assymm key\n - 1.4: Encrypt public key via private key and save
                        \nAt EncryptionTab you can:\n - 2.1: Decrypt symmetric key\n - 2.2: Encrypt you text and save it
                        \nAt DecryptionTab data of hybrid system:\n - 3.1: Decrypt symmetric key\n - 3.2: Decrypt you text and save it''')
        line2.setFont(custom_font)
        text.addWidget(line1)
        text.addWidget(line2)
        layout.addLayout(text)
        generalTab.setLayout(layout)
        return generalTab

    def __generate_keys(self) -> QWidget:
        """create tab with buttons to get pathes and solve creating and saving keys"""
        generalTab = QWidget()
        layout = QVBoxLayout()
        first = QVBoxLayout()
        first.setContentsMargins(10, 10, 10, 200)
        second = QHBoxLayout()
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setLineWidth(2)
        line1 = QHBoxLayout()
        button11 = QPushButton("Path for encrypted key")
        line11 = QLabel(self.settings['pathOfEncryptedSymmKeyToSave'])
        line11.setStyleSheet("border: 3px solid red;")
        line1.addWidget(button11)
        line1.addWidget(line11)
        button11.clicked.connect(
            partial(self.__input_path, self.settings, "pathOfEncryptedSymmKeyToSave", line11))
        line2 = QHBoxLayout()
        button22 = QPushButton("Path for public key")
        line22 = QLabel(self.settings["pathOfPublicKeyToSave"])
        line22.setStyleSheet("border: 3px solid red;")
        line2.addWidget(button22)
        line2.addWidget(line22)
        button22.clicked.connect(
            partial(self.__input_path, self.settings, "pathOfPublicKeyToSave", line22))
        line3 = QHBoxLayout()
        button33 = QPushButton("Path for private key")
        line33 = QLabel(self.settings["pathOfPrivateKeyToSave"])
        line33.setStyleSheet("border: 3px solid red;")
        line3.addWidget(button33)
        line3.addWidget(line33)
        button33.clicked.connect(
            partial(self.__input_path, self.settings, "pathOfPrivateKeyToSave", line33))
        first.addLayout(line1)
        first.addLayout(line2)
        first.addLayout(line3)
        button1 = QPushButton("gen symm key")
        button1.setStyleSheet("background-color: red")
        button1.clicked.connect(partial(self.__generate_symm_key, button1))
        button2 = QPushButton("gen assymm key")
        button2.setStyleSheet("background-color: red")
        button2.clicked.connect(partial(self.__generate_assym_keys, button2))
        button3 = QPushButton("save assymm keys")
        button3.clicked.connect(partial(self.__save_assym_keys, "pathOfPublicKeyToSave",
                                "pathOfPrivateKeyToSave", "publicKey", "privateKey", self.settings, button3))

        button4 = QPushButton("encrypt and save symm key")
        button4.clicked.connect(partial(
            self.__save_symm_key, "pathOfEncryptedSymmKeyToSave", "publicKey", "symmKey", self.settings, button4))
        second.addWidget(button1)
        second.addWidget(button2)
        second.addWidget(button3)
        second.addWidget(button4)
        layout.addLayout(first)
        layout.addWidget(separator)
        layout.addLayout(second)
        generalTab.setLayout(layout)
        return generalTab

    def __encryption_tab(self) -> QWidget:
        """create tab with buttons to get pathes and solve encryption of symm key and encryption of data"""
        generalTab = QWidget()
        layout = QVBoxLayout()

        first = QVBoxLayout()
        first.setContentsMargins(10, 10, 10, 200)
        second = QHBoxLayout()
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setLineWidth(2)
        line1 = QHBoxLayout()
        button11 = QPushButton("Path of data")
        line11 = QLabel(self.settings["pathOfDataToGet"])
        line11.setStyleSheet("border: 3px solid red;")
        line1.addWidget(button11)
        line1.addWidget(line11)
        button11.clicked.connect(
            partial(self.__input_file, self.settings, "pathOfDataToGet", line11, '.txt'))
        line2 = QHBoxLayout()
        button22 = QPushButton("Path of private key")
        line22 = QLabel(self.settings["pathOfPrivateKeyToGet1"])
        line22.setStyleSheet("border: 3px solid red")
        line2.addWidget(button22)
        line2.addWidget(line22)
        button22.clicked.connect(
            partial(self.__input_file, self.settings, "pathOfPrivateKeyToGet1", line22, '.pem'))
        line3 = QHBoxLayout()
        button33 = QPushButton("Path of encrypted key")
        line33 = QLabel(self.settings["pathOfEnctyptedSymmKeyToGet1"])
        line33.setStyleSheet("border: 3px solid red;")
        line3.addWidget(button33)
        line3.addWidget(line33)
        button33.clicked.connect(
            partial(self.__input_file, self.settings, "pathOfEnctyptedSymmKeyToGet1", line33, '.bin'))
        line4 = QHBoxLayout()
        button44 = QPushButton("Path for encrypted data")
        line44 = QLabel(self.settings["pathOfEncryptedDataToSave"])
        line44.setStyleSheet("border: 3px solid red;")
        line4.addWidget(button44)
        line4.addWidget(line44)
        button44.clicked.connect(
            partial(self.__input_path, self.settings, "pathOfEncryptedDataToSave", line44))
        first.addLayout(line1)
        first.addLayout(line2)
        first.addLayout(line3)
        first.addLayout(line4)
        button1 = QPushButton("decrypt key")
        button1.setStyleSheet("background-color: red")
        button1.clicked.connect(partial(self.__load_and_decrypt_symmKey,
                                "pathOfEnctyptedSymmKeyToGet1", "pathOfPrivateKeyToGet1", self.settings, button1))
        button2 = QPushButton("encrypt data and save")
        button2.clicked.connect(partial(self.__encrypt_data, "pathOfEncryptedDataToSave",
                                "pathOfDataToGet", "symmKey", self.settings, button2))
        second.addWidget(button1)
        second.addWidget(button2)
        layout.addLayout(first)
        layout.addWidget(separator)
        layout.addLayout(second)
        generalTab.setLayout(layout)
        return generalTab

    def __decryption_tab(self) -> QWidget:
        """create tab with buttons to get pathes and solve encryption of symm key and decryption of data"""
        generalTab = QWidget()
        layout = QVBoxLayout()
        first = QVBoxLayout()
        first.setContentsMargins(10, 10, 10, 200)
        second = QHBoxLayout()
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setLineWidth(2)
        line1 = QHBoxLayout()
        button11 = QPushButton("Path of encrypted data")
        line11 = QLabel(self.settings["pathOfEncryptedDataToGet"])
        line11.setStyleSheet("border: 3px solid red")
        line1.addWidget(button11)
        line1.addWidget(line11)
        button11.clicked.connect(
            partial(self.__input_file, self.settings, "pathOfEncryptedDataToGet", line11, '.bin'))
        line2 = QHBoxLayout()
        button22 = QPushButton("Path of private key")
        line22 = QLabel(self.settings["pathOfPrivateKeyToGet2"])
        line22.setStyleSheet("border: 3px solid red;")
        line2.addWidget(button22)
        line2.addWidget(line22)
        button22.clicked.connect(
            partial(self.__input_file, self.settings, "pathOfPrivateKeyToGet2", line22, '.pem'))
        line3 = QHBoxLayout()
        button33 = QPushButton("Path of encrypted key")
        line33 = QLabel(self.settings["pathOfEnctyptedSymmKeyToGet2"])
        line33.setStyleSheet("border: 3px solid red;")
        line3.addWidget(button33)
        line3.addWidget(line33)
        button33.clicked.connect(
            partial(self.__input_file, self.settings, "pathOfEnctyptedSymmKeyToGet2", line33, '.bin'))
        line4 = QHBoxLayout()
        button44 = QPushButton("Path for decrypted data")
        line44 = QLabel(self.settings["pathOfDataToSave"])
        line44.setStyleSheet("border: 3px solid red")
        line4.addWidget(button44)
        line4.addWidget(line44)
        button44.clicked.connect(
            partial(self.__input_path, self.settings, "pathOfDataToSave", line44))
        first.addLayout(line1)
        first.addLayout(line2)
        first.addLayout(line3)
        first.addLayout(line4)
        button1 = QPushButton("decrypt key")
        button1.setStyleSheet("background-color: red")
        button1.clicked.connect(partial(self.__load_and_decrypt_symmKey,
                                "pathOfEnctyptedSymmKeyToGet2", "pathOfPrivateKeyToGet1", self.settings, button1))
        button2 = QPushButton("decrypt data and save")
        button2.clicked.connect(partial(self.__decrypt_data, "pathOfDataToSave",
                                "pathOfEncryptedDataToGet", "symmKey", self.settings, button2))

        second.addWidget(button1)
        second.addWidget(button2)
        layout.addLayout(first)
        layout.addWidget(separator)
        layout.addLayout(second)
        generalTab.setLayout(layout)
        return generalTab

    def __input_path(self, settings: tuple, key: str, lable: QLabel) -> None:
        """service function"""
        settings[key] = QFileDialog.getExistingDirectory(self, 'Select Folder')
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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
