import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QMainWindow, QTabWidget, QListWidget, \
    QDateEdit, QLayout, QGraphicsView, QTextEdit
from pandas import Timestamp
from PyQt5.QtGui import QFont
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
import yfinance as yf
import timestamp
import numpy
import time
from datetime import datetime, timedelta


msft = yf.Ticker("MSFT")
class Authorize(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.login = '2'
        self.password = '1'
        self.main.logon = True
        #uic.loadUi('test.ui', self)
        self.initUI()

    def initUI(self):
        self.setGeometry(900, 400, 300, 100)
        self.setWindowTitle('Авторизация')
        self.grid = QGridLayout(self)
        self.login_edit = QLineEdit(self)
        self.password_edit = QLineEdit(self)
        self.enter_btn = QPushButton('Войти', self)
        self.cancel_btn = QPushButton('Отмена', self)
        self.reg_btn = QPushButton('Зарегистрироваться', self)
        self.grid.addWidget(QLabel('Логин:', self), 0, 0)
        self.grid.addWidget(self.login_edit, 0, 1)
        self.grid.addWidget(QLabel('Пароль:', self), 1, 0)
        self.grid.addWidget(self.password_edit, 1, 1)
        self.grid.addWidget(self.enter_btn, 2, 0)
        self.grid.addWidget(self.cancel_btn, 2, 1)
        self.grid.addWidget(self.reg_btn, 2, 2)

        self.enter_btn.clicked.connect(self.enter)
        self.cancel_btn.clicked.connect(self.cancel)
        self.reg_btn.clicked.connect(self.register)

    def enter(self):
        password = self.password_edit.text()
        login = self.login_edit.text()
        if password == self.password and login == self.login:
            self.main.password = password
            self.main.login = login
            self.close()


    def cancel(self):
        self.close()

    def register(self):
        password = self.password_edit.text()
        login = self.login_edit.text()

class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value) for value in values]

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.password = ''
        self.login = ''
        self.initUI()

    def initUI(self):


        self.setGeometry(900, 400, 600, 600)
        self.setWindowTitle('Биржа')

        self.date_start1 = QDateEdit(self)
        self.date_end1 = QDateEdit(self)
        self.add_btn1 = QPushButton('Добавить', self)
        self.graph1 = pg.PlotWidget()

        self.date_start2 = QDateEdit(self)
        self.date_end2 = QDateEdit(self)
        self.add_btn2 = QPushButton('Добавить', self)
        self.graph2 = pg.PlotWidget()

        self.date_start3 = QDateEdit(self)
        self.date_end3 = QDateEdit(self)
        self.add_btn3 = QPushButton('Добавить', self)
        self.graph3 = pg.PlotWidget()

        self.date_start4 = QDateEdit(self)
        self.date_end4 = QDateEdit(self)
        self.add_btn4 = QPushButton('Добавить', self)
        self.graph4 = pg.PlotWidget()

        self.grid = QGridLayout()
        self.tabWidget = QTabWidget(self)

        self.tab1 = QWidget(self)
        self.tab1.layout = QGridLayout(self)
        self.tab1.setLayout(self.tab1.layout)
        self.list1 = QListWidget(self)
        self.tab1.layout.addWidget(self.list1, 2, 2)
        self.tab1.layout.addWidget(self.date_start1, 0, 2)
        self.tab1.layout.addWidget(QLabel('Начало:', self), 0, 1)
        self.tab1.layout.addWidget(self.date_end1, 1, 2)
        self.tab1.layout.addWidget(QLabel('Конец:', self), 1, 1)
        self.tab1.layout.addWidget(self.graph1, 2, 0)
        self.tab1.layout.addWidget(self.add_btn1, 3, 2)

        self.tab2 = QWidget(self)
        self.tab2.layout = QGridLayout(self)
        self.tab2.setLayout(self.tab2.layout)
        self.list2 = QListWidget(self)
        self.tab2.layout.addWidget(self.list2, 2, 2)
        self.tab2.layout.addWidget(self.date_start2, 0, 2)
        self.tab2.layout.addWidget(QLabel('Начало:', self), 0, 1)
        self.tab2.layout.addWidget(self.date_end2, 1, 2)
        self.tab2.layout.addWidget(QLabel('Конец:', self), 1, 1)
        self.tab2.layout.addWidget(self.graph2, 2, 0)
        self.tab2.layout.addWidget(self.add_btn2, 3, 2)

        self.tab3 = QWidget(self)
        self.tab3.layout = QGridLayout(self)
        self.tab3.setLayout(self.tab3.layout)
        self.list3 = QListWidget(self)
        self.tab3.layout.addWidget(self.list3, 2, 2)
        self.tab3.layout.addWidget(self.date_start3, 0, 2)
        self.tab3.layout.addWidget(QLabel('Начало:', self), 0, 1)
        self.tab3.layout.addWidget(self.date_end3, 1, 2)
        self.tab3.layout.addWidget(QLabel('Конец:', self), 1, 1)
        self.tab3.layout.addWidget(self.graph3, 2, 0)
        self.tab3.layout.addWidget(self.add_btn3, 3, 2)

        self.tab4 = QWidget(self)
        self.tab4.layout = QGridLayout(self)
        self.tab4.setLayout(self.tab4.layout)
        self.list4 = QListWidget(self)
        self.tab4.layout.addWidget(self.list4, 2, 2)
        self.tab4.layout.addWidget(self.date_start4, 0, 2)
        self.tab4.layout.addWidget(QLabel('Начало:', self), 0, 1)
        self.tab4.layout.addWidget(self.date_end4, 1, 2)
        self.tab4.layout.addWidget(QLabel('Конец:', self), 1, 1)
        self.tab4.layout.addWidget(self.graph4, 2, 0)
        self.tab4.layout.addWidget(self.add_btn4, 3, 2)

        self.tab5 = QWidget(self)
        self.tab5.layout = QVBoxLayout(self)
        self.tab5.setLayout(self.tab5.layout)

        self.tabWidget.addTab(self.tab1, 'Индексы')
        self.tabWidget.addTab(self.tab2, 'Акции')
        self.tabWidget.addTab(self.tab3, 'Валюты')
        self.tabWidget.addTab(self.tab4, 'Криптовалюты')
        self.tabWidget.addTab(self.tab5, 'Настройки')
        self.grid.addWidget(self.tabWidget, 0, 0)
        self.setLayout(self.grid)

        hist = msft.history(period='1mo')
        hist['Date'] = hist.index
        dates = hist.loc[:, 'Date'].tolist()
        values = hist.loc[:, 'Open'].tolist()

        date_axis = pg.DateAxisItem()  # TimeAxisItem(orientation='bottom')
        dates = [datetime.fromtimestamp(x.timestamp()) for x in dates]
        dates = ["{:%d-%m-%Y %H:%M}".format(date) for date in dates]
        ticks = [list(zip(range(len(dates)), tuple(dates)))]
        date_axis.setTicks(ticks)
        self.graph1.setAxisItems({'bottom': date_axis})

        self.graph1.plot(y=values, pen='r')



    def authorize(self):
        self.dialog = Authorize(self)
        self.dialog.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())