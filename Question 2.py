# python 3
# -*- coding: utf-8 -*-

import time
import sys
import pymysql
from PyQt5.QtWidgets import (QWidget,QPushButton, QMessageBox, QLineEdit,QLabel,
    QTextEdit,QApplication,QDesktopWidget)
from PyQt5.QtGui import QIcon

con = pymysql.connect(host="localhost", port=3306, user="root", passwd="root", db="wikidata", charset="utf8")
cur = con.cursor()


class GUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 执行时间标签
        self.time=QLabel('',self)
        self.time.move(100,80)
        self.time.resize(200, 20)
        # ID标签
        self.sid = QLabel('ID', self)
        self.sid.move(25, 50)
        self.sid.resize(50, 20)
        # ID搜索框
        self.searchBar = QLineEdit(self)
        self.searchBar.move(100, 30)
        self.searchBar.resize(450,50)
        # 搜索按钮
        self.searchButton = QPushButton("Search",self)
        self.searchButton.move(600, 30)
        self.searchButton.resize(80,50)
        # 清空按钮
        self.clearButton = QPushButton("Clear", self)
        self.clearButton.move(700, 30)
        self.clearButton.resize(80, 50)
        # cnlabels
        self.cnlabels = QLabel('LABELS', self)
        self.cnlabels.move(15, 140)
        self.cnlabels.resize(50, 20)
        self.cnlabelsEdit=QTextEdit(self)
        self.cnlabelsEdit.move(100, 120)
        self.cnlabelsEdit.resize(680,60)

        # descriptions
        self.descriptions = QLabel('DESCRIPTIONS', self)
        self.descriptions.move(15, 200)
        self.descriptions.resize(80, 20)
        self.descriptionsEdit = QTextEdit(self)
        self.descriptionsEdit.move(100, 180)
        self.descriptionsEdit.resize(680, 60)
        # aliases
        self.aliases = QLabel('ALIASES', self)
        self.aliases.move(15, 260)
        self.aliases.resize(80, 20)
        self.aliasesEdit = QTextEdit(self)
        self.aliasesEdit.move(100, 240)
        self.aliasesEdit.resize(680, 60)
        # properties
        self.properties = QLabel('PROPERTIES', self)
        self.properties.move(15, 320)
        self.properties.resize(80, 20)
        self.propertiesEdit = QTextEdit(self)
        self.propertiesEdit.move(100, 300)
        self.propertiesEdit.resize(680, 60)
        # datavalue
        self.datavalue = QLabel('DATAVALUE', self)
        self.datavalue.move(15, 380)
        self.datavalue.resize(80, 20)
        self.datavalueEdit = QTextEdit(self)
        self.datavalueEdit.move(100, 360)
        self.datavalueEdit.resize(680, 160)


        self.resize( 800, 600)
        self.center()
        self.setWindowTitle('WikiData---Qs2 ID-Search')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.show()
        self.searchButton.clicked.connect(self.fun)
        self.clearButton.clicked.connect(self.clear)


    def fun(self):
        start = time.clock()
        queryid=self.searchBar.text()

        sql1 = "SELECT lable FROM web_main WHERE entity_id = '%s'" % (queryid)
        cur.execute(sql1)
        cnlabels = str(cur.fetchall()).replace('\'','').replace(',','').replace('(','').replace(')','')
        con.commit()
        self.cnlabelsEdit.append(cnlabels)


        sql3 = "SELECT description FROM web_main WHERE entity_id = '%s'" % (queryid)
        cur.execute(sql3)
        descriptions = str(cur.fetchall()).replace('\'', '').replace(',', '').replace('(', '').replace(')', '')
        con.commit()
        self.descriptionsEdit.append(descriptions)

        sql4 = "SELECT aliase FROM web_main WHERE entity_id = '%s'" % (queryid)
        cur.execute(sql4)
        aliases = str(cur.fetchall()).replace('\'', '').replace(',', '').replace('(', '').replace(')', '')
        con.commit()
        self.aliasesEdit.append(aliases)

        sql5 = "SELECT property_id FROM web_claims WHERE entity_id = '%s'" % (queryid)
        cur.execute(sql5)
        properties = str(cur.fetchall()).replace('\'', '').replace(',', '').replace('(', '').replace(')', '')
        con.commit()
        self.propertiesEdit.append(properties)

        sql6 = "SELECT datavalue_value FROM web_claims WHERE entity_id = '%s'" % (queryid)
        cur.execute(sql6)
        datavalue= str(cur.fetchall()).replace('\'', '').replace(',', '').replace('(', '').replace(')', '')
        con.commit()
        self.datavalueEdit.append(datavalue)


        end = time.clock()
        ex_time = 'Execution Time:' + str(end - start)
        # print(ex_time)
        self.time.setText(ex_time)


    def clear(self):
        self.searchBar.setText('')
        self.cnlabelsEdit.setText('')
        self.enlabelsEdit.setText('')
        self.descriptionsEdit.setText('')
        self.aliasesEdit.setText('')
        self.propertiesEdit.setText('')
        self.datavalueEdit.setText('')
        self.qhashEdit.setText('')
        self.qdatavalueEdit.setText('')
        self.rhashEdit.setText('')
        self.rdatavalueEdit.setText('')
        self.snakorderEdit.setText('')
        self.time.setText('')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to exit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())