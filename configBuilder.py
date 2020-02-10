from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class TreeModel(QAbstractProxyModel):
	pass


class ConfigConstructor(QDialog):
    def __init__(self, config):
        """Дмалог набора конфига"""
        super().__init__()        
        loadUi(r"./ui/configConstructor.ui", self)
        self.model = QStandardItemModel()
        self.treeView.setModel(self.model)

        item = QStandardItem("nest")
        item.insertRows(0, 3)
        self.model.appendRow(QStandardItem(item))
        self.model.appendRow(QStandardItem("test"))

    def buildTree(self, structure):
    	d = {}
    	for work in structure:
    		workItem = QStandardItem(work.get("Name", ""))
    		for section in work.get("Children", {}):
    			pass

