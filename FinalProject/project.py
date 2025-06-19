import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.collections import PatchCollection
#from matplotlib import cm, colors
from matplotlib.patches import Polygon

import sys

import pandas as pd
import numpy as np
import argparse as ap
import geopandas
import json
import plotly.express as px
import shapely

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QGridLayout, QPushButton, QComboBox, QSlider, QLabel

#----- Global Variables -----
dataDropdownOptions = ['Temperature Change', 'Precipitation Change', 'Extreme Precipitation', 'Dry Condition',  'Extreme Cold', 'Extreme Heat',
                       'Impervious Surface', 'Housing Density', 'Population Estimate', 'Low-lying Houses', 'Low-lying Roads',
                       'Hazard', 'Exposure', 'Vulnerability',
                       'Risk', 'Risk Percentage',]

    #Input drop down name to get the column name from the df
dictTrueName = {"Temperature Change":'TempChg', "Precipitation Change":'PrepChg', "Extreme Precipitation":'PrepExt', "Extreme Cold":'ColdExt', "Extreme Heat":'HeatExt', "Dry Condition":'DryChg', 
                       "Impervious Surface":'ImpSurface', "Housing Density":'HouseDen', "Population Estimate":'PopEst', "Low-lying Houses":'HouseSLR', "Low-lying Roads":'RoadSLR',
                       "Hazard":'Hazard(H)', "Exposure":'Expos(E)', "Vulnerability":'Vulner(V)', "Risk":'Risk=HEV', "Risk Percentage":'HEV*100'}

stateByID = {"01":'Alabama', "04":'Arizona', "05":'Arkansas', "06":'California', "08": 'Colorado',
             "09": 'Connecticut', "10": 'Delaware', "11": 'District of Columbia', "12": 'Flordia', 
             "13": 'Georgia', "16": 'Idaho', "17": 'Illinois', "18": 'Indiana', "19": 'Iowa', "20": 'Kansas', "21": 'Kentucky',
             "22": 'Louisiana', "23": 'Maine', "24": 'Maryland', "25": 'Massachusetts', "26": 'Michigan',
             "27": 'Minnesota', "28": 'Mississippi', "29": 'Missouri', "30": 'Montana', "31": 'Nebraska',
             "32": 'Nevada', "33": 'New Hampshire', "34": 'New Jersey', "35": 'New Mexico', "36": 'New York',
             "37": 'North Carolina', "38": 'North Dakota', "39": 'Ohio', "40": 'Oklahoma', "41": 'Oregon',
             "42": 'Pennsylvania', "44": 'Rhode Island', "45": 'South Carolina', "46": 'South Dakota',
             "47": 'Tennessee', "48": 'Texas', "49": 'Utah', "50": 'Vermont', "51": 'Virginia', "53": 'Washington',
             "54": 'West Virginia', "55": 'Wisconsin', "56": 'Wyoming'}

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QtWidgets.QGridLayout(self.main_widget)
        self.width = 1
        #global data, geoMap #Specify these are global because you change them by reordering

        self.mpl_canvas = FigureCanvas(Figure(figsize=(15, 8)))

        #Adds options to the dropdown
        #To add a new widget, have to fill it in, then do layout.addwidget()
        self.dropdown1 = QComboBox(self.main_widget)
        for name in dataDropdownOptions: 
            self.dropdown1.addItem(name)

        self.dropdown2 = QComboBox(self.main_widget)
        for name in dataDropdownOptions: 
            self.dropdown2.addItem(name)

        layout.addWidget(NavigationToolbar(self.mpl_canvas, self), 0, 0, 1, 6) # (Arg,   Row/Y,Column/X,Alignment)
        layout.addWidget(self.mpl_canvas,                          1, 0, 6, 6)
        #layout.addWidget(QLabel(''),                               7, 0, 1, 1) # Names the dropdown menu
        layout.addWidget(self.dropdown1,                           7, 1, 1, 1) # Adds the dropdown menu
        layout.addWidget(self.dropdown2,                           7, 4, 1, 1) # Adds the dropdown menu
        
        (self.ax, self.ax2) = self.mpl_canvas.figure.subplots(1,2)
        
        self.patchList = [] #Multipolygons have to be flattened, to turn them into a PatchCollection so tooltip works
        self.patchToID = [] #Since MultiPolys have to be flattened, it makes the array longer- so this ID will match to the data df.
        for polygon, fips in zip(geoMap['geometry'],geoMap['id']):
            if isinstance(polygon, shapely.geometry.multipolygon.MultiPolygon):
                for poly in polygon.geoms: #Have to itterate over every polygon in the multi-polygon to add it to the array
                    shape = np.array(poly.exterior.coords)
                    patch = Polygon(shape, facecolor='white', edgecolor='black')
                    self.patchList.append(patch)
                    self.patchToID.append(fips)
            else:
                shape = np.array(polygon.exterior.coords)
                patch = Polygon(shape, facecolor='white', edgecolor='black')
                self.patchList.append(patch)
                self.patchToID.append(fips)

        self.fipsToCountyName = {}
        for name, fips in zip(geoMap['NAME'], geoMap['id']):
            self.fipsToCountyName[fips] = name

        #print(len(self.patches))
        self.patches = PatchCollection(self.patchList, match_original=True)
        self.patches2 = PatchCollection(self.patchList, match_original=True)
        
        self.ax.add_collection(self.patches)
        self.ax2.add_collection(self.patches2)
        
        self.ax.clear()
        self.ax2.clear()

        self.ax.set_title("U.S. Climate Risk Projections by County, 2040-2049", loc='right')
        
        #Set the data for the first instance
        self.dataSelect = 'TempChg'
        self.dataSelect2 = 'PrepChg'
        
        self.create_plot(self.dataSelect, "Temperature Change")
        self.create_plot2(self.dataSelect2, "Precipitation Change")

        #self.plots = geoMap.plot(ax=self.ax[0], column=data[dataSelect], cmap='plasma', edgecolor='black', zorder=0)
        
        # These vv are used to change the data on the graph.
        self.dropdown1.activated.connect(self.update_data1)
        self.dropdown2.activated.connect(self.update_data2)

        self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->", color='grey'), zorder=10)
        self.annot2 = self.ax2.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->", color='grey'), zorder=10)
        self.annot.set_visible(False)
        self.annot2.set_visible(False)

    def hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            pos = [event.xdata,event.ydata]
            cont, ind = self.patches.contains(event)
            if cont:
                self.update_annot(ind['ind'][0], pos, 1) #ind is a dict (key is 'ind') and the item within is a list, we only need the first item in the list
                self.annot2.set_visible(True)
                self.annot.set_visible(True)
                self.mpl_canvas.figure.canvas.draw_idle()
            else:
                if vis:
                    self.annot2.set_visible(False)
                    self.annot.set_visible(False)
                    self.mpl_canvas.figure.canvas.draw_idle()
        elif event.inaxes == self.ax2:
            pos = [event.xdata,event.ydata]
            cont, ind = self.patches2.contains(event)
            if cont:
                self.update_annot(ind['ind'][0], pos, 2) #ind is a dict (key is 'ind') and the item within is a list, we only need the first item in the list
                self.annot2.set_visible(True)
                self.annot.set_visible(True)
                self.mpl_canvas.figure.canvas.draw_idle()
            else:
                if vis:
                    self.annot2.set_visible(False)
                    self.annot.set_visible(False)
                    self.mpl_canvas.figure.canvas.draw_idle()

    def update_annot(self, ind, pos, inWhichAx):
        self.annot.xy = pos
        self.annot2.xy = pos
        fips = self.patchToID[ind]
        rowIndex = geoMap[geoMap['id'] == fips].index 
        rowIndex = rowIndex[0]

        #Get each text beforehand and then join it all together in one big text string
        state_name = stateByID[geoMap.at[rowIndex, 'STATE']]
        text_name = self.fipsToCountyName[fips]
        text_data = data.at[rowIndex, self.dataSelect]
        text_data2 = data.at[rowIndex, self.dataSelect2]
        text_str = "State: {}\nCounty Name: {}\n{}: {}\n{}: {}"
        text = text_str.format(state_name,text_name, self.dataSelect, text_data, self.dataSelect2, text_data2)

        #TODO: Ask prof about what to do when you mouse over multiple dots at once
        if inWhichAx == 1:
            self.annot.set_text(text)
            self.annot2.set_text("")
            self.annot.get_bbox_patch().set_facecolor("pink")
            self.annot.get_bbox_patch().set_alpha(1)
        else:
            self.annot2.set_text(text)
            self.annot.set_text("")
            self.annot2.get_bbox_patch().set_facecolor("pink")
            self.annot2.get_bbox_patch().set_alpha(1)

    def create_plot(self, dataSelect, name): #This updates the graph.
        self.plots = geoMap.plot(ax=self.ax, column=data[dataSelect], cmap='plasma', edgecolor='black', zorder=0)
        self.ax.set_position([0.02, 0.3, 0.5, 0.5]) #left, bottom, width, height
        self.ax.set_title("U.S. Climate Risk Projections by County, 2040-2049", loc='right')
        #plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.8,hspace=0.4)
        
        #   Making the cmap
        cmap = mpl.colormaps["plasma"]
        cax=self.ax.inset_axes([1.01, 0, 0.05, 1])
        cbar = plt.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(data[dataSelect].min(), data[dataSelect].max()), cmap=cmap), cax=cax)
        cbar.set_label(name)

        #Redraw Annotation
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->", color='grey'), zorder=10)
        self.annot.set_visible(False)
    
    def create_plot2(self, dataSelect, name): #This updates the bottom graph.

        self.plots = geoMap.plot(ax=self.ax2, column=data[dataSelect], cmap='plasma', edgecolor='black', zorder=0)
        self.ax2.set_position([0.5, 0.3, 0.5, 0.5]) #left, bottom, width, height
        #plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.8,hspace=0.4)

        #   Making the cmap
        cmap = mpl.colormaps["plasma"]
        cax=self.ax2.inset_axes([1.01, 0, 0.05, 1])
        cbar = plt.colorbar(mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(data[dataSelect].min(), data[dataSelect].max()), cmap=cmap), cax=cax)
        cbar.set_label(name)

        #Redraw annotation
        self.annot2 = self.ax2.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->", color='grey'),zorder=10)
        self.annot2.set_visible(False)

    #Update X-Axis Variable
    def update_data1(self, index):
        name = self.dropdown1.currentText()
        self.ax.clear()
        self.dataSelect = dictTrueName[name]
        self.plots = self.create_plot(dictTrueName[name], name)
        #self.mpl_canvas.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.8,hspace=0.4)
        self.mpl_canvas.draw()

    def update_data2(self, index):
        name = self.dropdown2.currentText()
        self.ax2.clear()
        self.dataSelect2 = dictTrueName[name]
        self.plots = self.create_plot2(dictTrueName[name], name)
        self.mpl_canvas.draw()

if __name__ == '__main__':
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    parser = ap.ArgumentParser(description='CS439: Part 1, Bargraph')
    parser = ap.ArgumentParser(description='CS439: Simple Scatter Plot Example')
    parser.add_argument('-m', '--map', type=str, required=True, help='Map of the US Counties in GeoJSON format')
    parser.add_argument('-d', '--data', type=str, required=True, help='Climate data in an Excel spreadsheet')
    #parser.add_argument('-f', '--flights', type=str, required=True, help='List of all the flights in a JSON format')
    args = parser.parse_args()

    global data
    data = pd.read_csv(args.data, converters={'GEOID': str})
    #print(max(data['Capita']))
    #flights = pd.read_json(args.flights)

    global geoMap
    geoMap = geopandas.read_file(args.map)

    geoMap = geoMap.sort_values('id')
    geoMap = geoMap.reset_index()
    data = data.sort_values('GEOID')
    data = data.reset_index()

    app = ApplicationWindow()

    app.mpl_canvas.figure.canvas.mpl_connect("motion_notify_event", app.hover)

    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()
