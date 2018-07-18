# python 3
# -*- coding: utf-8 -*-

import re
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
        self.time.move(50,80)
        self.time.resize(200, 20)
        # 搜索按钮
        self.searchButton = QPushButton("Search",self)
        self.searchButton.move(600, 30)
        self.searchButton.resize(80,50)
        # 清空按钮
        self.clearButton = QPushButton("Clear", self)
        self.clearButton.move(700, 30)
        self.clearButton.resize(80, 50)
        # 搜索框
        self.searchBar = QLineEdit(self)
        self.searchBar.move(50, 30)
        self.searchBar.resize(500,50)
        # 搜索结果框
        self.resultEdit=QTextEdit(self)
        self.resultEdit.move(50, 120)
        self.resultEdit.resize(730,350)

        self.resize( 820, 550)
        self.center()
        self.setWindowTitle('WikiData---Qs5 Ask-Answer')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.show()
        self.searchButton.clicked.connect(self.fun)
        self.clearButton.clicked.connect(self.clear)


    def fun(self):
        start = time.clock()
        queryquestion= self.searchBar.text()

        #content = '%s' %(queryquestion)
        result = re.match('^China.*population$', queryquestion)
        print(result)
        if result:
            #sql1 = "SELECT datavalue_value FROM web_claims WHERE entity_id = 'Q148'"
            sql1 = "SELECT datavalue_value FROM web_claims WHERE property_id = 'P1082'"
            cur.execute(sql1)
            value = str(cur.fetchall()).replace('\'', '').replace(',', '').replace('(', '').replace(')', '')
            con.commit()
            print(type(value))
            self.resultEdit.append(value)
        else:
            self.resultEdit.append("请输入正确问题！谢谢！")


        end = time.clock()
        ex_time = 'Execution Time:' + str(end - start)
        # print(ex_time)
        self.time.setText(ex_time)


    def clear(self):
        self.searchBar.setText('')
        self.resultEdit.setText('')
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