import sys
import json
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class MainApp(QWidget):
    structFilePath = "./config.json"

    def __init__(self):
        """Инициализация главного виджета"""
        super().__init__()
        self.loadConfig()
        self.loadUI()

    def loadConfig(self):
        """Загружаем файл конфигурации с прописанными работами"""
        if os.path.exists(self.structFilePath):
            with open(self.structFilePath, 'r', encoding='utf-8') as file:
                self.Config = json.load(file)
        else:
            QMessageBox.warning(self, "Ошибка", "Отсутствует файл конфигурации")
            self.Config = None
    
    def loadUI(self):
        """Загрузка интерфейса"""

        # Расположение элементов по сетке
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Загрузка всех кнопок в соответствии с файлом конфига
        # и добавление их в коллекцию для доступа в будущем
        self.btnCollection = []
        for btnData in self.Config:
            btnIconPath = btnData.get("btnIconPath", "")
            if os.path.exists(btnIconPath):
                icon = QIcon(btnIconPath)
            else: icon = QIcon()
            btnText = btnData.get("btnText")
            btnName = btnData.get("btnName")
            
            btn = QPushButton(icon, btnText, self)
            btn.setObjectName(btnName)
            btn.clicked.connect(self.button_clicked)
            layout.addWidget(btn)
            self.btnCollection.append(btn)

    def button_clicked(self):
        btnText = self.sender().text()
        sections = [i for i in self.Config if i['btnText'] == btnText][0]



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainApp()
    w.show()
    sys.exit(app.exec_())
