from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

class WorkItem():
	def __init__(self):
		pass

class SectionItem():
	def __init__(self):
		pass

class InputItem():
	def __init__(self, name, unit):
		self._name = name
		self._unit = unit

class OutputItem():
	def __init__(self, name, unit, formula):
		self._name = name
		self._unit = unit
		self._formula = formula

class TreeNode(object):
	def __init__(self, parent, row):
		self._parent = parent
		self._row = row
		self._children = self._getChildren()

	def _getChildren(self):
		pass


class TreeModel(QAbstractItemModel):
	def __init__(self):
		super().__init__(self)



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

