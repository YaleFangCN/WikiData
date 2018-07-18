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
        # NMAE标签
        self.sid = QLabel('NAME', self)
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

        # entity_id
        self.entity_id = QLabel('ENTITY_ID', self)
        self.entity_id.move(15, 140)
        self.entity_id.resize(50, 20)
        self.entity_idEdit=QTextEdit(self)
        self.entity_idEdit.move(100, 120)
        self.entity_idEdit.resize(680,60)

        # type
        self.type = QLabel('TYPE', self)
        self.type.move(15, 200)
        self.type.resize(50, 20)
        self.typeEdit = QTextEdit(self)
        self.typeEdit.move(100, 180)
        self.typeEdit.resize(680, 60)

        #len
        self.len = QLabel('LEN', self)
        self.len.move(15, 260)
        self.len.resize(80, 20)
        self.lenEdit = QTextEdit(self)
        self.lenEdit.move(100, 240)
        self.lenEdit.resize(680, 60)

        # lable
        self.lable = QLabel('LABLE', self)
        self.lable.move(15, 320)
        self.lable.resize(80, 20)
        self.lableEdit = QTextEdit(self)
        self.lableEdit.move(100, 300)
        self.lableEdit.resize(680, 160)

        #description
        self.description = QLabel('DESCRIPTION', self)
        self.description.move(15, 380)
        self.description.resize(80, 20)
        self.descriptionEdit = QTextEdit(self)
        self.descriptionEdit.move(100, 360)
        self.descriptionEdit.resize(680, 60)

        # alise
        self.aliases = QLabel('ALISE', self)
        self.aliases.move(15, 440)
        self.aliases.resize(80, 20)
        self.aliasesEdit = QTextEdit(self)
        self.aliasesEdit.move(100, 400)
        self.aliasesEdit.resize(680, 60)

        # site
        self.site = QLabel('SITE', self)
        self.site.move(15, 500)
        self.site.resize(80, 20)
        self.siteEdit = QTextEdit(self)
        self.siteEdit.move(100, 460)
        self.siteEdit.resize(680, 60)

        # title
        self.title = QLabel('TITLE', self)
        self.title.move(15, 560)
        self.title.resize(80, 20)
        self.titleEdit = QTextEdit(self)
        self.titleEdit.move(100, 520)
        self.titleEdit.resize(680, 60)

        self.resize( 800, 650)
        self.center()
        self.setWindowTitle('WikiData---Qs1 ID-Search')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.show()
        self.searchButton.clicked.connect(self.fun)
        self.clearButton.clicked.connect(self.clear)


    def fun(self):
        start = time.clock()
        queryname=self.searchBar.text()


        sql1 = "SELECT entity_id FROM web_main WHERE lable = '%s'" % (queryname)
        cur.execute(sql1)
        entity_id = str(cur.fetchall()).replace('\'','').replace(',','').replace('(','').replace(')','')
        con.commit()
       # print("entity_id")
        self.entity_idEdit.append(entity_id)

        sql2 = "SELECT type FROM web_main WHERE lable = '%s'" % (queryname)
        cur.execute(sql2)
        type = str(cur.fetchall()).replace('\'', '').replace(',', '').replace('(', '').replace(')', '')
        #print("1111111")
        con.commit()
        self.typeEdit.append(type)

        sql3 = "SELECT description FROM web_main WHERE lable = '%s'" % (queryname)
        cur.execute(sql3)
        description = str(cur.fetchall()).replace('\'', '').replace(',', '').replace('(', '').replace(')', '')
        con.commit()
        self.descriptionEdit.append(description)

        sql4 = "SELECT aliase FROM web_main WHERE lable = '%s'" % (queryname)
        cur.execute(sql4)
        aliases = str(cur.fetchall()).replace('\'', '').replace(',', '').replace('(', '').replace(')', '')
        con.commit()
        self.aliasesEdit.append(aliases)

        sql5 = "SELECT len FROM web_main WHERE lable = '%s'" % (queryname)
        cur.execute(sql5)
        len = str(cur.fetchall()).replace('\'', '').replace(',', '').replace('(', '').replace(')', '')
        con.commit()
        self.lenEdit.append(len)

        sql6 = "SELECT lable FROM web_main WHERE lable = '%s'" % (queryname)
        cur.execute(sql6)
        lable= str(cur.fetchall()).replace('\'', '').replace(',', '').replace('(', '').replace(')', '')
        con.commit()
        self.lableEdit.append(lable)

        sql7 = "SELECT site FROM web_main WHERE lable = '%s'" % (queryname)
        cur.execute(sql7)
        site = str(cur.fetchall()).replace('\'', '').replace(',', '').replace('(', '').replace(')', '')
        con.commit()
        self.siteEdit.append(site)

        sql8 = "SELECT title FROM web_main WHERE lable = '%s'" % (queryname)
        cur.execute(sql8)
        title = str(cur.fetchall()).replace('\'', '').replace(',', '').replace('(', '').replace(')', '')
        con.commit()
        self.titleEdit.append(title)


        end = time.clock()
        ex_time = 'Execution Time:' + str(end - start)
        # print(ex_time)
        self.time.setText(ex_time)


    def clear(self):
        self.searchBar.setText('')
        self.entity_idEdit.setText('')
        self.typeEdit.setText('')
        self.descriptionEdit.setText('')
        self.aliasesEdit.setText('')
        self.lenEdit.setText('')
        self.lableEdit.setText('')
        self.siteEdit.setText('')
        self.titleEdit.setText('')
        self.rhashEdit.setText('')
        self.rlableEdit.setText('')
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