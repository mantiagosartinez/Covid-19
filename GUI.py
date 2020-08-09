# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 18:03:51 2020

@author: santi
"""

from PyQt5.QtCore import QDateTime, Qt, QTimer, QRect
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QListWidget, QColorDialog)

from io import StringIO 
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

import urllib.request
import sys


class Covid(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.originalPalette = QApplication.palette()

        QLabel("&Pais:")       
        
        self.dataBase()
        self.createTopLayout()
        self.anotherGroup()
        
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftGroupBox()
        self.createBottomRightGroupBox()
        
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topLayout, 0, 0, 1, 3)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1, 1,2)
        mainLayout.addWidget(self.bottomLeftGroupBox, 2, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        mainLayout.addWidget(self.anotherGroup, 2, 2)
        
        
        self.setLayout(mainLayout)
        self.setWindowTitle("Covid-19 Estadisticas")
        self.anotherGroup.setEnabled(False)
        
        #Tengo un tema con la siguiente linea, se supone que lo que hace es cambiar el estilo de la ventana, por ejemplo podes hacer que parezca que es estilo win 98 o vista, etc. Mi favorita es fusion, pero por alguna razon cuando lo hago el QcomboBox falla, en vez de abrirse una lista tranqui de unos 8 elementos, se abre una lista que ocupa toda la pantalla, y solo cambiando eso. Como es algo tan especifico no encontre nada ni en foros ni en documentacion.
        #QApplication.setStyle(QStyleFactory.create("Fusion"))
        
    def closeEvent(self,event):
        QApplication.quit()
        
    def dataBase(self):
        """Carga la base de datos de casos confirmados, muertos y recuperados"""
        
        url = """https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"""
        confirmed = "time_series_covid19_confirmed_global.csv"
        deaths = "time_series_covid19_deaths_global.csv"
        recovered = "time_series_covid19_recovered_global.csv"
        
        with urllib.request.urlopen(url+confirmed) as f: 
            data = f.read().decode('utf-8')
            data = StringIO(data)
            
        df = pd.read_csv(data)
        df = df.drop(columns=['Province/State','Lat', 'Long'])
        self.covid_data_confirmed = df.groupby('Country/Region').agg('sum')

        
        with urllib.request.urlopen(url+deaths) as f: 
            data = f.read().decode('utf-8')
            data = StringIO(data)
        df = pd.read_csv(data)
        df = df.drop(columns=['Province/State','Lat', 'Long'])
        self.covid_data_deaths = df.groupby('Country/Region').agg('sum')
        
        with urllib.request.urlopen(url+recovered) as f: 
            data = f.read().decode('utf-8')
            data = StringIO(data)
        df = pd.read_csv(data)
        df = df.drop(columns=['Province/State','Lat', 'Long'])
        self.covid_data_recovered = df.groupby('Country/Region').agg('sum')
        
    def createTopLayout(self):
        """Crea el layout de arriba de todo"""
        
        self.topLayout = QGroupBox()
        layout = QHBoxLayout()
        
        self.total = QRadioButton("Totales")
        self.daily = QRadioButton("Diarios")
        self.total.setChecked(True)
        self.country = QComboBox()
        self.total.toggled.connect(self.graph)
        self.country.addItem("Seleccione un país")
        self.country.addItems(self.covid_data_confirmed.index.values)

        self.country.currentTextChanged.connect(self.graph)
        layout.addWidget(self.country, alignment = Qt.AlignLeft)
        layout.addWidget(self.total, alignment = Qt.AlignCenter)
        layout.addWidget(self.daily, alignment = Qt.AlignRight)
        
        self.topLayout.setLayout(layout)
        
    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Opciones temporales")
        layout = QVBoxLayout()
        
        self.t_comienzo = QRadioButton("Desde el comienzo")
        self.t_month = QRadioButton("Último mes")
        self.t_week = QRadioButton("Última semana")
        self.t_comienzo.setChecked(True)
        
        self.t_comienzo.toggled.connect(self.turnOff)
        self.t_month.toggled.connect(self.turnOn)
        self.t_month.toggled.connect(self.turnOn)
        self.t_comienzo.toggled.connect(self.graph)
        
        self.t_month.toggled.connect(self.graph)
        self.t_week.toggled.connect(self.graph)
        
        layout.addWidget(self.t_comienzo)
        layout.addWidget(self.t_month)
        layout.addWidget(self.t_week)
        #layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)     
    
    def turnOff(self):
        self.interpol.setChecked(True)
        self.anotherGroup.setEnabled(False)
    
    def turnOn(self):
        self.anotherGroup.setEnabled(True)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox()
        layout = QVBoxLayout()
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.sub = self.figure.add_subplot(111)
        self.sub.plot()
        self.sub.clear()
        
        layout.addWidget(self.canvas)
        self.topRightGroupBox.setLayout(layout)


    def createBottomLeftGroupBox(self):
        self.bottomLeftGroupBox = QGroupBox("Opciones de datos")
        layout = QGridLayout()
        self.cases = QCheckBox("Contagios")
        self.deaths = QCheckBox("Muertos")
        self.recovered = QCheckBox("Recuperados")
        
        self.c_cases = QPushButton("")
        self.c_cases.setStyleSheet("background-color: blue")

        self.c_deaths = QPushButton("")
        self.c_deaths.setStyleSheet("background-color: green")

        self.c_recovered = QPushButton("")
        self.c_recovered.setStyleSheet("background-color: violet")
        
        
        self.c_cases.clicked.connect(self.color_cases)
        self.c_deaths.clicked.connect(self.color_deaths)
        self.c_recovered.clicked.connect(self.color_recovered)
        
        self.cases.stateChanged.connect(self.graph)
        self.deaths.stateChanged.connect(self.graph)
        self.recovered.stateChanged.connect(self.graph)
        
        self.all = QPushButton("Todos")
        self.all.clicked.connect(self.todos)
        self.cases.setChecked(True)
        self.deaths.setChecked(False)
        self.recovered.setChecked(False)

        layout.addWidget(self.cases, 0, 0)
        layout.addWidget(self.deaths, 1, 0)
        layout.addWidget(self.recovered, 2, 0)
        layout.addWidget(self.c_cases, 0, 1)
        layout.addWidget(self.c_deaths, 1, 1)
        layout.addWidget(self.c_recovered, 2, 1)
        layout.addWidget(self.all)
        
        self.bottomLeftGroupBox.setLayout(layout)
    
    def color_cases(self):
        self.color_cases = QColorDialog.getColor()
        self.c_cases.setStyleSheet("background-color:" + self.color_cases.name())
        self.graph()
        
    def color_deaths(self):
        self.color_deaths = QColorDialog.getColor()
        self.c_deaths.setStyleSheet("background-color:" + self.color_deaths.name())
        self.graph()
        
    def color_recovered(self):
        self.color_recovered = QColorDialog.getColor()
        self.c_recovered.setStyleSheet("background-color:" + self.color_recovered.name())
        self.graph()       
        
    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Group 3")
        
        layout = QGridLayout()
        
        self.lin = QRadioButton("Lineal")
        self.log = QRadioButton("Logarítmico")
        
        self.lin.setChecked(True)
        self.lin.toggled.connect(self.graph)
        layout.addWidget(self.lin)
        layout.addWidget(self.log)
        self.bottomRightGroupBox.setLayout(layout)
        
        
    def anotherGroup(self):
        self.anotherGroup = QGroupBox("Group 4")
        
        layout = QVBoxLayout()
        self.interpol = QRadioButton("Interpolación")
        self.bar = QRadioButton("Barra")
        self.interpol.setChecked(True)
        self.interpol.toggled.connect(self.graph)
        
        layout.addWidget(self.interpol)
        layout.addWidget(self.bar)
        self.anotherGroup.setLayout(layout)
        
    def graph(self):
        self.max = 0
        labeled = []
        self.sub.clear()
        if self.country.currentIndex()>0:
            country = self.covid_data_confirmed.index.values[self.country.currentIndex()-1]
        else:
            
            return
        checked = [self.cases, self.recovered, self.deaths ]
        label = ["Casos confirmados", "Recuperados", "Muertos"]
        data = [self.covid_data_confirmed, self.covid_data_recovered, self.covid_data_deaths]
        
        color = []
        
        ###Se te ocurre otra forma de organizar las siguientes lineas? La otra que se me ocurrio es hacer dos listas de 3 elementos y un for que los recorra, y poner el try catch adentro del for, pero tiene la desventaja de que deberia asignar en una lista los elementos de cada color, por lo tanto ya en la asignacion me tira error si no existen
        
        try:
            color.append(self.color_cases.name())
        except:
            color.append("b")
        try:
            color.append(self.color_recovered.name())
        except:
            color.append("violet")
        try:
            color.append(self.color_deaths.name())
        except:
            color.append("g")
            
        
        #Las siguientes lineas son los cambios si es lineal o log
        if self.lin.isChecked():
            logY = False
            mini = 0
            
        else:
            logY = True
            mini = 1
        
        #Las siguientes lineas cambian si es grafico de linea o de barra
        if self.interpol.isChecked():
            kind="line"
        else:
            kind="bar"
            
        #Las siguientes lineas cambian segun el tiempo de inicio que está seleccionado
        if self.t_comienzo.isChecked():
            start = -len(self.covid_data_confirmed.columns)
        elif self.t_month.isChecked():
            start=-30
        elif self.t_week.isChecked():
            start=-8
        
        #El grafico general, decidi hacerlos en dos, si es total o si es diario porque tenian varios cambios (Ademas del titulo hay una linea extra en donde se restan) De todas formas se que podria meter un if afuera para cambiar el titulo y otro if adentro para ver si es necesaria la linea en que se resta para obtener los casos diarios
        if self.total.isChecked():
            for checked_i, data_i, color_i, label_i in zip(checked, data, color, label):
                if checked_i.isChecked():
                    country_data = data_i[data_i.index.values == country]
                    by_date = country_data.filter(like='/20').T
                    by_date[start:-1].plot(ax=self.sub, color=color_i, logy=logY, label=label_i, title="Covid 19 acumulativo en " + country, kind=kind, linewidth=2)
                    if by_date[country].max() >= self.max:
                        self.max = by_date[country].max()
                    self.sub.set_ylim(mini, self.max)
                    labeled.append(label_i)
                self.sub.legend(labeled)
        else:
            for checked_i, data_i, color_i, label_i in zip(checked, data, color, label):
                if checked_i.isChecked():
                    country_data = data_i[data_i.index.values == country]
                    by_date = country_data.filter(like='/20').diff(axis=1).T
                    by_date[start:-1].plot(ax=self.sub, color=color_i, logy=logY, label=label_i, title="Covid 19 diario en " + country, kind=kind, linewidth=2)
                    if by_date[country].max() >= self.max:
                        self.max = by_date[country].max()
                    self.sub.set_ylim(mini, self.max)
                    labeled.append(label_i)
                self.sub.legend(labeled)
                    
        self.canvas.draw()
        
        
    def todos(self):
        #El boton que acciona las 3 opciones
        self.cases.setChecked(True)
        self.deaths.setChecked(True)
        self.recovered.setChecked(True)
        
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    gallery = Covid()
    gallery.show()
    sys.exit(app.exec_())