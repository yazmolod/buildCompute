import sys
import json
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from configBuilder import ConfigConstructor

class MainApp(QMainWindow):
    structFilePath = "./config.json"
    def __init__(self):
        """Инициализация главного окна"""
        super().__init__()
        self.loadConfig()
        self.initMenu()
        self.initCentralWidget()

    def loadConfig(self):
        """Загружаем файл конфигурации с прописанными работами"""
        if os.path.exists(self.structFilePath):
            with open(self.structFilePath, 'r', encoding='utf-8') as file:
                self.Config = json.load(file)
        else:
            QMessageBox.warning(self, "Ошибка", "Отсутствует файл конфигурации")
            self.Config = None

    def initMenu(self):        
        editConfigAction = QAction("&Редактировать", self)
        editConfigAction.triggered.connect(self.editConfig)

        fileMenu = self.menuBar().addMenu("&Конфигурация")
        fileMenu.addAction(editConfigAction)

    def initCentralWidget(self):
        self.setCentralWidget(CentralWidget(self))

    def editConfig(self):
        dialog = ConfigConstructor(self.Config)
        dialog.exec()


class CentralWidget(QWidget):    

    def __init__(self, parent=None):
        """Инициализация центрального виджета"""
        super().__init__(parent=parent)
        self.loadUI()
    
    def loadUI(self):
        """Загрузка интерфейса"""

        # Расположение элементов по сетке
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Загрузка всех кнопок в соответствии с файлом конфига
        # и добавление их в коллекцию для доступа в будущем
        self.btnCollection = []
        for btnData in self.parent().Config:
            btnIconPath = btnData.get("IconPath", "")
            if os.path.exists(btnIconPath):
                icon = QIcon(btnIconPath)
            else: icon = QIcon()
            btnText = btnData.get("Name")
            
            btn = QPushButton(icon, btnText, self)
            btn.clicked.connect(self.button_clicked)
            layout.addWidget(btn)
            self.btnCollection.append(btn)

    def button_clicked(self):
        btnText = self.sender().text()
        inputDataConfig = [i for i in self.parent().Config if i['Name'] == btnText][0]['Sections']
        dialog = InputDataDialog(inputDataConfig)


class InputDataDialog(QDialog):

    def __init__(self, config):
        super().__init__()
        loadUi(r"./ui/inputDialog.ui", self)
        self.inputs = []
        self.outputs = []
        self.backButton.setEnabled(False)
        self.config = config
        self.loadSectionSheet(self.Stack.widget(0), [i.get("Name") for i in config])
        self.loadSignals()
        self.exec()


    def loadSignals(self):
        self.nextButton.clicked.connect(self.nextButton_clicked)
        self.backButton.clicked.connect(self.backButton_clicked)
        self.acceptButton.clicked.connect(self.acceptButton_clicked)
        self.buttonGroup.buttonClicked.connect(self.radioButtonGroup_clicked)

    def loadSectionSheet(self, parent, data):
        layout = QVBoxLayout(parent)
        self.buttonGroup = QButtonGroup(parent)
        for section in data:
            radio = QRadioButton(section, parent)
            self.buttonGroup.addButton(radio)
            layout.addWidget(radio)

    def loadInputSheet(self, parent, data):
        self.inputs.clear()
        layout = QGridLayout(parent)
        for i in range(len(data)):
            nameLabel = QLabel(data[i].get("Name"), parent)
            measureLabel = QLabel(data[i].get("Unit"), parent)
            le = QDoubleSpinBox(parent)
            le.valueChanged.connect(self.updateOutputs)
            self.inputs.append(le)
            layout.addWidget(nameLabel, i, 0)
            layout.addWidget(le, i, 1)
            layout.addWidget(measureLabel, i, 2)

    def loadOutputSheet(self, parent, data):
        layout = QGridLayout(parent)
        self.outputs.clear()
        for i in range(len(data)):
            nameLabel = QLabel(data[i].get("Name"), parent)
            measureLabel = QLabel(data[i].get("Unit"), parent)
            
            le = QDoubleSpinBox(parent)
            self.outputs.append(le)
            le.formula = data[i].get("Formula", "").replace("[", "self.inputs[").replace("]", "].value()")
            le.setValue(0)

            le.setEnabled(False)
            layout.addWidget(nameLabel, i, 0)
            layout.addWidget(le, i, 1)
            layout.addWidget(measureLabel, i, 2)

    def updateOutputs(self, *args):
        print (1)
        for o in self.outputs:
            print (o.formula)
            exec('global xxx; xxx = ' + o.formula)
            o.setValue(xxx)


    def radioButtonGroup_clicked(self, btn):
        inputWidget = self.Stack.widget(1)
        outputWidget = self.Stack.widget(2)
        inputLayout = inputWidget.layout()
        if inputLayout != None:
            for i in reversed(range(inputLayout.count())): 
                inputLayout.itemAt(i).widget().setParent(None)
        self.loadInputSheet(inputWidget, [i for i in self.config if i['Name'] == btn.text()][0]['Inputs'])
        self.loadOutputSheet(outputWidget, [i for i in self.config if i['Name'] == btn.text()][0]['Outputs'])


    def nextButton_clicked(self):
        curInd = self.Stack.currentIndex()
        self.Stack.setCurrentIndex(curInd + 1)
        self.backButton.setEnabled(True)
        self.nextButton.setEnabled(curInd != self.Stack.count()-2) 

    def backButton_clicked(self):
        curInd = self.Stack.currentIndex()
        self.Stack.setCurrentIndex(curInd - 1)
        self.nextButton.setEnabled(True)
        self.backButton.setEnabled(curInd - 1 != 0 )

    def acceptButton_clicked(self):
        self.accept()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainApp()
    w.show()
    sys.exit(app.exec_())
