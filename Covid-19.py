# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 18:03:51 2020

@author: santi
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                             QPushButton, QRadioButton, QVBoxLayout,
                             QColorDialog,QFileDialog)

from io import StringIO 
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import urllib.request
import sys

class Covid(QDialog):
    
    def __init__(self, parent=None):
        
        super().__init__(parent)
        self.originalPalette = QApplication.palette()
        QLabel("&Pais:")       
        
        # Genera las funciones
        self.dataBase()
        self.createTop()
        self.createBottomRight() 
        self.createCenterLeft()
        self.createCenterRight()
        self.createBottomLeft()
        self.createBottomCenter()
        
        # Distribuye las funciones en el layout
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.top, 0, 0, 1, 3)
        mainLayout.addWidget(self.centerLeft, 1, 0)
        mainLayout.addWidget(self.centerRight, 1, 1, 1,2)
        mainLayout.addWidget(self.bottomLeft, 2, 0)
        mainLayout.addWidget(self.bottomCenter, 2, 1)
        mainLayout.addWidget(self.bottomRight, 2, 2)
        
        self.setLayout(mainLayout)
        self.setWindowTitle("Covid-19 Estadisticas")
        self.bottomRight.setEnabled(False)
        
    def closeEvent(self,event):
        """Función que se ejecuta al cerrar la ventana"""
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
        df = df.drop(columns = ['Province/State','Lat', 'Long'])
        self.covid_data_recovered = df.groupby('Country/Region').agg('sum')

    def createTop(self):
        """Crea el layout de arriba"""
        
        self.top = QGroupBox()
        layout = QHBoxLayout()
        
        self.total = QRadioButton("Totales")
        self.daily = QRadioButton("Diarios")
        self.total.setChecked(True) #Setea el predeterminado
        self.country = QComboBox()
        self.total.toggled.connect(self.graph)
        self.country.addItem("Seleccione un país")
        self.country.addItems(self.covid_data_confirmed.index.values)

        self.country.currentTextChanged.connect(self.graph)
        layout.addWidget(self.country, alignment = Qt.AlignLeft)
        layout.addWidget(self.total, alignment = Qt.AlignCenter)
        layout.addWidget(self.daily, alignment = Qt.AlignRight)
        
        self.top.setLayout(layout)
        
    def createCenterLeft(self):
        """Crea el layout de la izquierda"""
        self.centerLeft = QGroupBox("Opciones temporales")
        layout = QVBoxLayout()
        
        self.t_comienzo = QRadioButton("Desde el comienzo")
        self.t_month = QRadioButton("Último mes")
        self.t_week = QRadioButton("Última semana")
        self.t_comienzo.setChecked(True) #Setea el predeterminado
        self.avg = QCheckBox("Suavizado (Media movil 7 dias)")
        
        self.t_comienzo.toggled.connect(self.turnOn)
        self.t_month.toggled.connect(self.turnOn)
        self.t_week.toggled.connect(self.turnOn)
        
        self.t_comienzo.toggled.connect(self.turnOff)
        self.t_month.toggled.connect(self.turnOff)
        self.t_week.toggled.connect(self.turnOff)
        
        
        self.t_comienzo.toggled.connect(self.graph)
        self.avg.toggled.connect(self.graph)
        self.t_month.toggled.connect(self.graph)
        self.t_week.toggled.connect(self.graph)
        
        
        layout.addWidget(self.t_comienzo)
        layout.addWidget(self.t_month)
        layout.addWidget(self.t_week)
        layout.addWidget(self.avg)
        self.centerLeft.setLayout(layout)     
    
    def turnOff(self):
        """Desactiva los widgets que tenga que desactivar en función de que está seleccionado"""
        if self.t_comienzo.isChecked():
            self.interpol.setChecked(True)
            self.bottomRight.setEnabled(False)
            
        if self.t_week.isChecked():
            self.avg.setEnabled(False) 
            self.avg.setChecked(False)
    
    def turnOn(self):
        """Activa los widgets que tenga que activar en función de lo que está seleccionado"""
        if self.t_comienzo.isChecked()==False:
            self.bottomRight.setEnabled(True)
            
        if self.t_week.isChecked()==False:
            self.avg.setEnabled(True)

    def createCenterRight(self):
        """Crea el layout del gráfico"""
        self.centerRight = QGroupBox()
        layout = QGridLayout()
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.sub = self.figure.add_subplot(111)
        self.sub.plot()
        self.sub.clear()
        self.export = QPushButton("Exportar gráfico")
        
        self.export.clicked.connect(self.exportar)
        layout.addWidget(self.canvas, 0,0,1,3)
        layout.addWidget(self.export, 1,2)
        
        
        self.centerRight.setLayout(layout)
    


    def createBottomLeft(self):
        """Crea el layout de abajo a la izquierda"""
        self.bottomLeft = QGroupBox("Opciones de datos")
        layout = QGridLayout()
        self.confirmed = QCheckBox("Contagios")
        self.deaths = QCheckBox("Muertos")
        self.recovered = QCheckBox("Recuperados")
        
        self.c_confirmed = QPushButton("")
        self.c_confirmed.setStyleSheet("background-color: blue")

        self.c_deaths = QPushButton("")
        self.c_deaths.setStyleSheet("background-color: green")

        self.c_recovered = QPushButton("")
        self.c_recovered.setStyleSheet("background-color: violet")
        
        
        self.c_confirmed.clicked.connect(self.color_confirmed)
        self.c_deaths.clicked.connect(self.color_deaths)
        self.c_recovered.clicked.connect(self.color_recovered)
        
        self.confirmed.stateChanged.connect(self.graph)
        self.deaths.stateChanged.connect(self.graph)
        self.recovered.stateChanged.connect(self.graph)
        
        self.all = QPushButton("Todos")
        self.all.clicked.connect(self.todos)
        self.confirmed.setChecked(True)


        layout.addWidget(self.confirmed, 0, 0)
        layout.addWidget(self.deaths, 1, 0)
        layout.addWidget(self.recovered, 2, 0)
        
        layout.addWidget(self.c_confirmed, 0, 1)
        layout.addWidget(self.c_deaths, 1, 1)
        layout.addWidget(self.c_recovered, 2, 1)
        layout.addWidget(self.all)
        
        self.bottomLeft.setLayout(layout)
    
    def exportar(self):
        print("Hey")
        filename = QFileDialog.getSaveFileName(self, "Exportar", None, ".png;;.pdf;;.jpg;;.eps")
        self.figure.savefig(filename[0]+filename[1])

        
    def todos(self):
        """Activa el boton "todos", el cual activa los 3 gráficos"""
        self.confirmed.setChecked(True)
        self.deaths.setChecked(True)
        self.recovered.setChecked(True)
        
    
    def color_confirmed(self):
        """Asigna el color de la curva de casos confirmados"""
        
        self.color_confirmed = QColorDialog.getColor()
        self.c_confirmed.setStyleSheet("background-color:" + self.color_confirmed.name())
        self.graph()
        
    def color_deaths(self):
        """Asigna el color de la curva de fallecidos"""
        self.color_deaths = QColorDialog.getColor()
        self.c_deaths.setStyleSheet("background-color:" + self.color_deaths.name())
        self.graph()
        
    def color_recovered(self):
        """Asigna el color de la curva de recuperados"""
        self.color_recovered = QColorDialog.getColor()
        self.c_recovered.setStyleSheet("background-color:" + self.color_recovered.name())
        self.graph()       
        
    def createBottomCenter(self):
        """Crea el layout de abajo en el centro"""
        self.bottomCenter = QGroupBox("Opciones de escala")
        layout = QGridLayout()
        
        self.lin = QRadioButton("Lineal")
        self.log = QRadioButton("Logarítmico")
        
        self.lin.setChecked(True)
        self.lin.toggled.connect(self.graph)
        layout.addWidget(self.lin)
        layout.addWidget(self.log)
        self.bottomCenter.setLayout(layout)
        
        
    def createBottomRight(self):
        """Crea el layout de abajo a la derecha"""
        self.bottomRight = QGroupBox("Tipo de gráfico")
        layout = QVBoxLayout()
        
        self.interpol = QRadioButton("Interpolación")
        self.bar = QRadioButton("Barra")
        self.interpol.setChecked(True)
        self.interpol.toggled.connect(self.graph)
        
        layout.addWidget(self.interpol)
        layout.addWidget(self.bar)
        self.bottomRight.setLayout(layout)
        
    def graph(self):
        """La funcion que se encarga del grafico"""
        self.max = 0 #Para que se resetee el maximo, ya que habia un problema 
        #si pasabas de un pais con muchas muertes a uno con pocas
        labeled = []
        self.sub.clear()
        color = [] #resetea el vector de colores cada vez que se ejecuta
        if self.country.currentIndex() > 0:
            country = self.covid_data_confirmed.index.values[self.country.currentIndex()-1]
            #El -1 esta para no contar el "seleccionar pais"
        else:
            pass #No hace nada
            return
        checked = [self.confirmed, self.recovered, self.deaths ]
        label = ["Casos confirmados", "Recuperados", "Muertos"]
        data = [self.covid_data_confirmed, self.covid_data_recovered, self.covid_data_deaths]
        
        for colores, default in (                                                                     
                (self.color_confirmed, "b"), (self.color_recovered, "violet"), (self.color_deaths, 'g')):                                                                                                   
            try:                                                                                    
                color.append(colores.name())                                                          
            except:                    
                                                    
                color.append(default)
        
        if self.avg.isChecked(): # Determina la ventana de promedio
            avg = 7
        else:
            avg = 1
        
        if self.lin.isChecked(): # Setea si es logaritmico o no
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
            start = -30 
        elif self.t_week.isChecked():
            start = -8
            
        for checked_i, data_i, color_i, label_i in zip(checked, data, color, label):                
            if checked_i.isChecked():                                                               
                country_data = data_i[data_i.index.values == country]   
                #El siguiente if varia en funcion de si cuenta
                #los casos acumulativos o solamente los diarios. 
                #Toma esta información de lo seleccionado en self.top                      
                if self.total.isChecked():       
                    #En caso de que este seleccionado los casos acumulativos                               
                    by_date = country_data.filter(like='/20').T
                    by_date = by_date.rolling(window=avg).mean()  
                    by_date[start:-1].plot(ax=self.sub, color=color_i, logy=logY, label=label_i,    
                                           title="Covid 19 acumulativo en " + country, kind=kind, linewidth=2) 
                                                                                         
                else:     
                    #En caso de que esten seleccionados los casos diarios                                                                          
                    by_date = country_data.filter(like='/20').T
                    by_date = by_date.rolling(window=avg).mean()  
                    by_date = by_date.diff(axis=0)
                    by_date[start:-1].plot(ax=self.sub, color=color_i, logy=logY, label=label_i,    
                                           title="Covid 19 diario en " + country, kind=kind, linewidth=2)
                #Lo siguiente setea configuraciones del máximo                                                                                           
                if by_date[country].max() >= self.max:                                              
                    self.max = by_date[country].max()                                               
                self.sub.set_ylim(mini, self.max)                                                   
                labeled.append(label_i)
                self.sub.legend(labeled)
                self.sub.grid() #Setea la grilla
            
        self.canvas.draw() #Grafica
        
        


if __name__ == '__main__':
    
    
    app = QApplication(sys.argv)
    gallery = Covid()
    gallery.show()
    app.exec_()