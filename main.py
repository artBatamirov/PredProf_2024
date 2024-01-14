import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QMainWindow, QTabWidget, QListWidget, \
    QDateEdit, QLayout, QGraphicsView, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout


class WordTrick(QWidget):
    def __init__(self):
        super().__init__()
        #uic.loadUi('test.ui', self)
        self.initUI()

    def initUI(self):
        self.setGeometry(900, 400, 600, 600)
        self.setWindowTitle('Биржа')

        self.date_start1 = QDateEdit(self)
        self.date_end1 = QDateEdit(self)
        self.graph1 = pg.PlotWidget()

        self.date_start2 = QDateEdit(self)
        self.date_end2 = QDateEdit(self)
        self.graph2 = pg.PlotWidget()


        self.date_start3 = QDateEdit(self)
        self.date_end3 = QDateEdit(self)
        self.graph3 = pg.PlotWidget()


        self.date_start4 = QDateEdit(self)
        self.date_end4 = QDateEdit(self)
        self.graph4 = pg.PlotWidget()



        self.grid = QGridLayout()
        self.tabWidget = QTabWidget(self)

        self.tab1 = QWidget(self)
        self.tab1.layout = QGridLayout(self)
        self.tab1.setLayout(self.tab1.layout)
        self.list1 = QListWidget(self)
        self.tab1.layout.addWidget(self.list1, 2, 1)
        self.tab1.layout.addWidget(self.date_start1, 0, 1)
        self.tab1.layout.addWidget(QLabel('Начало:', self), 0, 0)
        self.tab1.layout.addWidget(self.date_end1, 1, 1)
        self.tab1.layout.addWidget(QLabel('Конец:', self), 1, 0)
        self.tab1.layout.addWidget(self.graph1, 2, 0)

        self.tab2 = QWidget(self)
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.setLayout(self.tab2.layout)
        self.tab2.layout.addWidget(self.date_start2)
        self.tab2.layout.addWidget(self.date_end2)
        self.tab2.layout.addWidget(self.graph2)

        self.tab3 = QWidget(self)
        self.tab3.layout = QVBoxLayout(self)
        self.tab3.setLayout(self.tab3.layout)
        self.tab3.layout.addWidget(self.date_start3)
        self.tab3.layout.addWidget(self.date_end3)
        self.tab3.layout.addWidget(self.graph3)

        self.tab4 = QWidget(self)
        self.tab4.layout = QVBoxLayout(self)
        self.tab4.setLayout(self.tab4.layout)
        self.tab4.layout.addWidget(self.date_start4)
        self.tab4.layout.addWidget(self.date_end4)
        self.tab4.layout.addWidget(self.graph4)

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

class CreatePage(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.homeBtn = QPushButton("Home")

        self.frontLabel = QLabel("Front")
        self.frontLabel.setFont(QFont("Decorative", 20))
        self.frontEdit = QTextEdit(placeholderText="frontEdit")
        self.frontEdit.setFont(QFont("Decorative", 11))

        self.backLabel = QLabel("Back")
        self.backLabel.setFont(QFont("Decorative", 20))
        self.backEdit = QTextEdit(placeholderText="backEdit")
        self.backEdit.setFont(QFont("Decorative", 11))

        grid = QGridLayout()
        grid.addWidget(self.homeBtn,    0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)
        grid.addWidget(self.frontLabel, 1, 0, alignment=Qt.AlignCenter)
        grid.addWidget(self.frontEdit,  2, 0)
        grid.addWidget(self.backLabel,  3, 0, alignment=Qt.AlignCenter)
        grid.addWidget(self.backEdit,   4, 0)

        self.setLayout(grid)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WordTrick()
    ex.show()
    sys.exit(app.exec())