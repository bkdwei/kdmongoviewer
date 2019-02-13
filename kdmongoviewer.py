import os
import sys
import json
from pymongo import MongoClient
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.uic import loadUi
import kdconfig


class kdmongoviewer(QMainWindow):
    def __init__(self):
        super(kdmongoviewer, self).__init__()
        loadUi("kdmongoviewer.ui", self)
        conf = kdconfig.init_conf()
        if conf:
            self.le_host.setText(conf["host"])
            self.le_port.setText(conf["port"])
        #~ 待修复
        self.cb_db.currentIndexChanged.connect(
            self.on_cb_db_currentIndexChanged)
        self.lw_collection.itemClicked.connect(
            self.on_lw_collection_itemClicked)

    @pyqtSlot()
    def on_pb_connect_clicked(self):
        self.host = self.le_host.text()
        self.port = self.le_port.text()

        kdconfig.update_conf(self.host, self.port)

        self.conn = MongoClient(self.host, int(self.port))
        self.dbs = self.conn.list_database_names()
        self.cb_db.addItem("请选择数据库")
        self.cb_db.addItems(self.dbs)

    @pyqtSlot()
    def on_cb_db_currentIndexChanged(self):
        cur_db = self.cb_db.currentText()
        print(cur_db)
        if cur_db != "":
            self.db = getattr(self.conn, cur_db)
            self.collection_names = self.db.collection_names()
            self.lw_collection.clear()
            self.lw_collection.addItems(self.collection_names)

    @pyqtSlot()
    def on_lw_collection_itemClicked(self):
        cur_item = self.lw_collection.currentItem().text()
        print(cur_item + "clicked")
        cur_collection = getattr(self.db, cur_item)
        sets = cur_collection.find()
        sets_result = ""
        for i in sets:
            js = json.dumps(i, sort_keys=True, indent=4, separators=(',', ':'))
            print(js)
            sets_result += js
        self.te_result.setText(sets_result)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = kdmongoviewer()
    win.show()
    sys.exit(app.exec_())
