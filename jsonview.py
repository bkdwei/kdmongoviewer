# this code copy from https://github.com/trufasa/jsonViewer

import os
import sys
import json
import ast
from collections import OrderedDict
from PyQt5 import QtCore, QtWidgets, QtGui, uic


class jsonviewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = uic.loadUi("viewUI.ui")
        self.widget = self.ui.treeWidget
        self.jsonViewArray = [self]
        self.currentJSON = ""
        self.childrenArray = dict()
        self.revertDict = []
        self.parentsArray = []

    # Fills single cell in table
    def fillItem(self, item, value):
        if type(value) is dict:
            for key, val in sorted(value.items()):
                child = QtWidgets.QTreeWidgetItem()
                child.setText(0, key)
                item.addChild(child)
                item.setExpanded(True)
                child.setFlags(child.flags() | QtCore.Qt.ItemIsEditable)
                self.fillItem(child, val)
        elif type(value) is list:
            for single_value in value:
                child = QtWidgets.QTreeWidgetItem()
                child.setText(0, "list")
                item.addChild(child)
                item.setExpanded(True)
                child.setFlags(child.flags() | QtCore.Qt.ItemIsEditable)
                self.fillItem(child, single_value)
                # ~ self.fillItem(self.ui.treeWidget.invisibleRootItem(), single_value)
            # ~ item.setText(1, str(value))
            # ~ item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        else:
            item.setText(1, str(value))
            item.setExpanded(False)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

    # Fills entire table widget
    def fillWidget(self, value):
        self.ui.treeWidget.clear()
        self.fillItem(self.ui.treeWidget.invisibleRootItem(), value)

    def children(self, parent):
        childCount = parent.childCount()
        if childCount > 0:
            if parent.parent():
                dictArray = []
                self.childrenArray = []
                for index in range(childCount):
                    self.children(parent.child(index))
                iterChildren = iter(self.childrenArray)
                iterArray = dict(zip(iterChildren, iterChildren))
                self.childrenArray = []
                self.childrenArray.append(iterArray)
                self.childrenArray = []
                self.childrenArray.append(parent.text(0))
                self.childrenArray.append(iterArray)
                print(self.childrenArray)
            else:
                self.parentsArray.append(parent)
                for index in range(childCount):
                    self.children(parent.child(index))
        elif parent.text(1):
            value0 = parent.text(0)
            value1 = parent.text(1)
            self.childrenArray.append(value0)
            self.childrenArray.append(value1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = jsonviewer()
    window.ui.show()
    sys.exit(app.exec_())
