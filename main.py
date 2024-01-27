import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QMainWindow, QTabWidget, QListWidget, \
    QDateEdit, QLayout, QGraphicsView, QTextEdit, QMessageBox, QCheckBox, QComboBox
from pandas import Timestamp
from PyQt5.QtGui import QFont
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
import yfinance as yf
import numpy
import talib


from datetime import datetime, timedelta
import sqlite3

# Подключение к БД
con = sqlite3.connect("trade_bd.sqlite")

# Создание курсора
cur = con.cursor()


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

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.password = ''
        self.login = ''
        self.date = []
        self.date_axis = None
        self.initUI()
        self.graps = {self.list1: self.graph1, self.list2: self.graph2, self.list3: self.graph3,
                      self.list4: self.graph4}
        self.date_edits = {self.list1: (self.date_start1, self.date_end1),
                           self.list2: (self.date_start2, self.date_end2),
                           self.list3: (self.date_start3, self.date_end3),
                           self.list4: (self.date_start4, self.date_end4)}
        self.ckecks = {self.list1: (self.check_open_1, self.check_close_1, self.check_high_1, self.check_low_1),
                        self.list2: (self.check_open_2, self.check_close_2, self.check_high_2, self.check_low_2),
                        self.list3: (self.check_open_3, self.check_close_3, self.check_high_3, self.check_low_3),
                        self.list4: (self.check_open_4, self.check_close_4, self.check_high_4, self.check_low_4)}
        self.lists = {self.del_btn1: self.list1, self.del_btn2: self.list2, self.del_btn3: self.list3,
                      self.del_btn4: self.list4}
        self.comboboxes = {self.list1: self.indicators1, self.list2: self.indicators2,
                           self.list3: self.indicators3, self.list4: self.indicators4}
        self.db_inf = {self.add_btn1: (1, 'индекс'), self.add_btn2: (2, 'акцию'), self.add_btn3: (3, 'валюту'),
                  self.add_btn4: (4, 'криптовалюту')}


    def initUI(self):
        self.setGeometry(900, 400, 600, 600)
        self.setWindowTitle('Биржа')

        self.date_start1 = QDateEdit(self)
        self.date_end1 = QDateEdit(self)
        self.add_btn1 = QPushButton('Добавить', self)
        self.del_btn1 = QPushButton('Удалить', self)
        self.check_open_1 = QCheckBox('Open', self)
        self.check_close_1 = QCheckBox('Close', self)
        self.check_high_1 = QCheckBox('High', self)
        self.check_low_1 = QCheckBox('Low', self)
        self.check_open_1.setChecked(True)
        self.check_close_1.setChecked(True)
        self.check_high_1.setChecked(True)
        self.check_low_1.setChecked(True)
        self.graph1 = pg.PlotWidget()
        self.small_graph1 = pg.PlotWidget()

        self.date_start2 = QDateEdit(self)
        self.date_end2 = QDateEdit(self)
        self.add_btn2 = QPushButton('Добавить', self)
        self.del_btn2 = QPushButton('Удалить', self)
        self.check_open_2 = QCheckBox('Open', self)
        self.check_close_2 = QCheckBox('Close', self)
        self.check_high_2 = QCheckBox('High', self)
        self.check_low_2 = QCheckBox('Low', self)
        self.check_open_2.setChecked(True)
        self.check_close_2.setChecked(True)
        self.check_high_2.setChecked(True)
        self.check_low_2.setChecked(True)
        self.graph2 = pg.PlotWidget()
        self.small_graph2 = pg.PlotWidget()

        self.date_start3 = QDateEdit(self)
        self.date_end3 = QDateEdit(self)
        self.add_btn3 = QPushButton('Добавить', self)
        self.del_btn3 = QPushButton('Удалить', self)
        self.check_open_3 = QCheckBox('Open', self)
        self.check_close_3 = QCheckBox('Close', self)
        self.check_high_3 = QCheckBox('High', self)
        self.check_low_3 = QCheckBox('Low', self)
        self.check_open_3.setChecked(True)
        self.check_close_3.setChecked(True)
        self.check_high_3.setChecked(True)
        self.check_low_3.setChecked(True)
        self.graph3 = pg.PlotWidget()
        self.small_graph3 = pg.PlotWidget()

        self.date_start4 = QDateEdit(self)
        self.date_end4 = QDateEdit(self)
        self.add_btn4 = QPushButton('Добавить', self)
        self.del_btn4 = QPushButton('Удалить', self)
        self.check_open_4 = QCheckBox('Open', self)
        self.check_close_4 = QCheckBox('Close', self)
        self.check_high_4 = QCheckBox('High', self)
        self.check_low_4 = QCheckBox('Low', self)
        self.check_open_4.setChecked(True)
        self.check_close_4.setChecked(True)
        self.check_high_4.setChecked(True)
        self.check_low_4.setChecked(True)
        self.graph4 = pg.PlotWidget()
        self.small_graph4 = pg.PlotWidget()

        self.grid = QGridLayout()
        self.tabWidget = QTabWidget(self)

        self.tab1 = QWidget(self)
        self.tab1.layout = QGridLayout(self)
        self.tab1.setLayout(self.tab1.layout)
        self.list1 = QListWidget(self)
        self.indicators1 = QComboBox(self)
        self.tab1.layout.addWidget(self.indicators1, 0, 0)
        self.tab1.layout.addWidget(self.list1, 2, 2)
        self.tab1.layout.addWidget(self.date_start1, 0, 2)
        self.tab1.layout.addWidget(QLabel('Начало:', self), 0, 1)
        self.tab1.layout.addWidget(self.date_end1, 1, 2)
        self.tab1.layout.addWidget(QLabel('Конец:', self), 1, 1)
        self.tab1.layout.addWidget(self.graph1, 2, 0)
        self.tab1.layout.addWidget(self.add_btn1, 3, 2)
        self.tab1.layout.addWidget(self.del_btn1, 4, 2)
        self.tab1.layout.addWidget(self.check_open_1, 5, 1)
        self.tab1.layout.addWidget(self.check_close_1, 5, 2)
        self.tab1.layout.addWidget(self.check_high_1, 6, 1)
        self.tab1.layout.addWidget(self.check_low_1, 6, 2)

        self.tab2 = QWidget(self)
        self.tab2.layout = QGridLayout(self)
        self.tab2.setLayout(self.tab2.layout)
        self.list2 = QListWidget(self)
        self.indicators2 = QComboBox(self)
        self.tab2.layout.addWidget(self.indicators2, 0, 0)
        self.tab2.layout.addWidget(self.list2, 2, 2)
        self.tab2.layout.addWidget(self.date_start2, 0, 2)
        self.tab2.layout.addWidget(QLabel('Начало:', self), 0, 1)
        self.tab2.layout.addWidget(self.date_end2, 1, 2)
        self.tab2.layout.addWidget(QLabel('Конец:', self), 1, 1)
        self.tab2.layout.addWidget(self.graph2, 2, 0)
        self.tab2.layout.addWidget(self.add_btn2, 3, 2)
        self.tab2.layout.addWidget(self.del_btn2, 4, 2)
        self.tab2.layout.addWidget(self.check_open_2, 5, 1)
        self.tab2.layout.addWidget(self.check_close_2, 5, 2)
        self.tab2.layout.addWidget(self.check_high_2, 6, 1)
        self.tab2.layout.addWidget(self.check_low_2, 6, 2)

        self.tab3 = QWidget(self)
        self.tab3.layout = QGridLayout(self)
        self.tab3.setLayout(self.tab3.layout)
        self.list3 = QListWidget(self)
        self.indicators3 = QComboBox(self)
        self.tab3.layout.addWidget(self.indicators3, 0, 0)
        self.tab3.layout.addWidget(self.list3, 2, 2)
        self.tab3.layout.addWidget(self.date_start3, 0, 2)
        self.tab3.layout.addWidget(QLabel('Начало:', self), 0, 1)
        self.tab3.layout.addWidget(self.date_end3, 1, 2)
        self.tab3.layout.addWidget(QLabel('Конец:', self), 1, 1)
        self.tab3.layout.addWidget(self.graph3, 2, 0)
        self.tab3.layout.addWidget(self.add_btn3, 3, 2)
        self.tab3.layout.addWidget(self.del_btn3, 4, 2)
        self.tab3.layout.addWidget(self.check_open_3, 5, 1)
        self.tab3.layout.addWidget(self.check_close_3, 5, 2)
        self.tab3.layout.addWidget(self.check_high_3, 6, 1)
        self.tab3.layout.addWidget(self.check_low_3, 6, 2)

        self.tab4 = QWidget(self)
        self.tab4.layout = QGridLayout(self)
        self.tab4.setLayout(self.tab4.layout)
        self.list4 = QListWidget(self)
        self.indicators4 = QComboBox(self)
        self.tab4.layout.addWidget(self.indicators4, 0, 0)
        self.tab4.layout.addWidget(self.list4, 2, 2)
        self.tab4.layout.addWidget(self.date_start4, 0, 2)
        self.tab4.layout.addWidget(QLabel('Начало:', self), 0, 1)
        self.tab4.layout.addWidget(self.date_end4, 1, 2)
        self.tab4.layout.addWidget(QLabel('Конец:', self), 1, 1)
        self.tab4.layout.addWidget(self.graph4, 2, 0)
        self.tab4.layout.addWidget(self.add_btn4, 3, 2)
        self.tab4.layout.addWidget(self.del_btn4, 4, 2)
        self.tab4.layout.addWidget(self.check_open_4, 5, 1)
        self.tab4.layout.addWidget(self.check_close_4, 5, 2)
        self.tab4.layout.addWidget(self.check_high_4, 6, 1)
        self.tab4.layout.addWidget(self.check_low_4, 6, 2)

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
        self.list1.clicked.connect(self.show_graph)
        self.list2.clicked.connect(self.show_graph)
        self.list3.clicked.connect(self.show_graph)
        self.list4.clicked.connect(self.show_graph)
        self.line_1 = None
        self.line_2 = None
        self.line_3 = None
        self.line_4 = None
        self.ind_line = None
        self.ind_line2 = None
        self.graph1.showGrid(x=True, y=True)
        self.graph2.showGrid(x=True, y=True)
        self.graph3.showGrid(x=True, y=True)
        self.graph4.showGrid(x=True, y=True)
        self.graph1.addLegend()
        self.graph2.addLegend()
        self.graph3.addLegend()
        self.graph4.addLegend()
        self.add_btn1.clicked.connect(self.add)
        self.del_btn1.clicked.connect(self.remove)
        self.add_btn2.clicked.connect(self.add)
        self.del_btn2.clicked.connect(self.remove)
        self.add_btn3.clicked.connect(self.add)
        self.del_btn3.clicked.connect(self.remove)
        self.add_btn4.clicked.connect(self.add)
        self.del_btn4.clicked.connect(self.remove)

        self.show_list()


    def show_list(self):
        self.list1.clear()
        self.list2.clear()
        self.list3.clear()
        self.list4.clear()
        indexes_data = cur.execute("""SELECT name FROM market WHERE type = (SELECT id FROM type WHERE name = 'индексы')""").fetchall()
        for i in indexes_data:
            self.list1.addItem(i[0])

        stock_data = cur.execute(
            """SELECT name FROM market WHERE type = (SELECT id FROM type WHERE name = 'акции')""").fetchall()
        for i in stock_data:
            self.list2.addItem(i[0])

        currency_data = cur.execute(
            """SELECT name FROM market WHERE type = (SELECT id FROM type WHERE name = 'валюта')""").fetchall()
        for i in currency_data:
            self.list3.addItem(i[0])

        krypto_data = cur.execute(
            """SELECT name FROM market WHERE type = (SELECT id FROM type WHERE name = 'криптовалюта')""").fetchall()
        for i in krypto_data:
            self.list4.addItem(i[0])

        indicators_data = cur.execute(
            """SELECT name FROM market WHERE type = (SELECT id FROM type WHERE name = 'индикаторы')""").fetchall()
        indicators_data = [indicator[0] for indicator in indicators_data] + ['None']
        self.indicators1.addItems(indicators_data)
        self.indicators2.addItems(indicators_data)
        self.indicators3.addItems(indicators_data)
        self.indicators4.addItems(indicators_data)

    def show_graph(self):

        date_edit = self.date_edits[self.sender()]
        start = date_edit[0].date().toString('yyyy-MM-dd')
        end = date_edit[1].date().toString('yyyy-MM-dd')
        graph = self.graps[self.sender()]
        graph.removeItem(self.line_1)
        graph.removeItem(self.line_2)
        graph.removeItem(self.line_3)
        graph.removeItem(self.line_4)
        graph.removeItem(self.ind_line)
        graph.removeItem(self.ind_line2)
        cmp = yf.Ticker(self.sender().currentItem().text())
        hist = cmp.history(period='1mo', start=start, end=end)

        hist['Date'] = hist.index
        dates = hist.loc[:, 'Date'].tolist()
        values_open = hist.loc[:, 'Open'].tolist()
        values_close = hist.loc[:, 'Close'].tolist()
        values_high = hist.loc[:, 'High'].tolist()
        values_low = hist.loc[:, 'Low'].tolist()
        if values_open and values_close:
            graph.setTitle(self.sender().currentItem().text(), color="w", size="10pt")
            check_w = self.ckecks[self.sender()]
            graph.getPlotItem().enableAutoRange()
            date_axis = pg.DateAxisItem()
            dates = [datetime.fromtimestamp(x.timestamp()) for x in dates]
            dates = ["{:%d.%m.%Y}".format(date) for date in dates]
            ticks = [list(zip(range(len(dates)), tuple(dates)))]
            date_axis.setTicks(ticks)
            graph.setAxisItems({'bottom': date_axis})
            if check_w[0].isChecked():
                self.line_1 = graph.plot(y=values_open, pen='g', name='open')
            if check_w[1].isChecked():
                self.line_2 = graph.plot(y=values_close, pen='r', name='close')
            if check_w[2].isChecked():
                self.line_3 = graph.plot(y=values_high, pen='b', name='high')
            if check_w[3].isChecked():
                self.line_4 = graph.plot(y=values_low, pen='m', name='low')
            combobox: QComboBox = self.comboboxes[self.sender()]
            if combobox.currentText() != 'None':
                if combobox.currentText() == 'ATR':
                    high, low, close = numpy.asarray(values_high), numpy.asarray(values_low), numpy.asarray(values_close)
                    atr = talib.ATR(high, low, close, timeperiod=30)
                    self.ind_line = graph.plot(y=atr, pen='y', name='ATR')
                elif combobox.currentText() == 'EMA':
                    close = numpy.asarray(values_close)
                    ema = talib.EMA(close, timeperiod=30)
                    self.ind_line = graph.plot(y=ema, pen='y', name='EMA')
                elif combobox.currentText() == 'SMA':
                    close = numpy.asarray(values_close)
                    sma = talib.SMA(close, timeperiod=30)
                    self.ind_line = graph.plot(y=sma, pen='y', name='SMA')
                elif combobox.currentText() == 'MACD':
                    close = numpy.asarray(values_close)
                    macd, macdsignal, _ = talib.MACD(close, fastperiod=15, slowperiod=30, signalperiod=10)
                    self.ind_line = graph.plot(y=macd, pen='y', name='MACD')
                    self.ind_line2 = graph.plot(y=macdsignal, pen='w', name='')

    def add(self):
        inf = self.db_inf[self.sender()]
        text, pressed = QInputDialog.getText(self, "", f"Добавить {inf[1]}:", QLineEdit.Normal, "")

        cur.execute("INSERT INTO market(name, type) VALUES(?, ?)", (text, inf[0]))
        con.commit()
        self.show_list()

    def remove(self):
        list_w = self.lists[self.sender()]
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.resize(150, 100)
        text = list_w.currentItem().text()
        msg.setText(f"Вы дейсвительно хотите удалить {text}?")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
        if msg.clickedButton().text() == 'OK':
            cur.execute("DELETE FROM market WHERE name = ?", (text, ))
            con.commit()
            self.show_list()







    def authorize(self):
        self.dialog = Authorize(self)
        self.dialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())