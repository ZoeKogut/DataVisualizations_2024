import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import argparse as ap
import math
from scipy.interpolate import make_interp_spline
from matplotlib import cm, colors

import sys
import time

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QGridLayout, QPushButton, QComboBox, QSlider, QLabel

# ====== Global Variables ======
dataX = ['CO2', 'GDP_per_capita', 'airports', 'alcohol', 'area',	
         'birth_rate', 'broadband', 'budget_surplus_or_deficit',	
         'child_mortality_ratio', 'death_rate', 'debt', 'education',
         'electricity',	'energy_per_capita', 'exports',	'imports', 
         'inflation', 'internet_users', 'labor_force', 'life_expectancy', 
         'maternal_mortality_ratio', 'median_age', 'military_expenditures',
         'net_migration_rate', 'obesity', 'population', 'population_growth_rate', 
         'railways', 'roadways', 'total_fertility', 'unemployment']
dataY = ['CO2', 'GDP_per_capita', 'airports', 'alcohol', 'area',	
         'birth_rate', 'broadband', 'budget_surplus_or_deficit',	
         'child_mortality_ratio', 'death_rate', 'debt', 'education',
         'electricity',	'energy_per_capita', 'exports',	'imports', 
         'inflation', 'internet_users', 'labor_force', 'life_expectancy', 
         'maternal_mortality_ratio', 'median_age', 'military_expenditures',
         'net_migration_rate', 'obesity', 'population', 'population_growth_rate', 
         'railways', 'roadways', 'total_fertility', 'unemployment']
dataSize = ['CO2', 'GDP_per_capita', 'airports', 'alcohol', 'area',	
         'birth_rate', 'broadband', 'budget_surplus_or_deficit',	
         'child_mortality_ratio', 'death_rate', 'debt', 'education',
         'electricity',	'energy_per_capita', 'exports',	'imports', 
         'inflation', 'internet_users', 'labor_force', 'life_expectancy', 
         'maternal_mortality_ratio', 'median_age', 'military_expenditures',
         'net_migration_rate', 'obesity', 'population', 'population_growth_rate', 
         'railways', 'roadways', 'total_fertility', 'unemployment']
dataColor = ['CO2', 'GDP_per_capita', 'airports', 'alcohol', 'area',	
         'birth_rate', 'broadband', 'budget_surplus_or_deficit',	
         'child_mortality_ratio', 'death_rate', 'debt', 'education',
         'electricity',	'energy_per_capita', 'exports',	'imports', 
         'inflation', 'internet_users', 'labor_force', 'life_expectancy', 
         'maternal_mortality_ratio', 'median_age', 'military_expenditures',
         'net_migration_rate', 'obesity', 'population', 'population_growth_rate', 
         'railways', 'roadways', 'total_fertility', 'unemployment']
gray =   (0.7, 0.7, 0.7, 1.0)
# These vv should be changed whenever the dropdown menu is
x = "GDP_per_capita"
y = "military_expenditures"
color = "population"
size = "life_expectancy"
sizeC = 0
data = {"x": x, "y": y, "c": color, "s": size, "xlabel": x, "ylabel": y, "sizeC": sizeC}
dataR = {"x": x, "y": y, "c": color, "s": size, "xlabel": x, "ylabel": y, "sizeC": sizeC}
# ====== End of Global Variables ======

## Start of legend.py code ========================================
    ## ==== I did the comments tho =====
def n_orders(_min, _max):
    print(_min)
    minR = 10
    maxR = 250
    minV = df[size].min()
    maxV = df[size].max()
    maxo = minR + ((maxV - minV)/(maxV - minV)) * (maxR - minR)
    mino = minR + ((minV - minV)/(maxV - minV)) * (maxR - minR)
    #mino = int(math.log10(_min))
    #maxo = int(math.log10(_max))
    return mino, maxo

def legend_helper(values, sizes, nstops=4, log_scale=True):
    all_vals = np.array([values, sizes]).transpose()
    #print(all_vals.shape)

    #print(f'values are\n{values}')
    #print(f'sizes are\n{sizes}')
    #print(f'values before sorting:\n{all_vals}')
    all_vals = np.sort(all_vals, axis=0)
#===== I wrote this code vv
    all_vals = np.where(np.isfinite(all_vals), all_vals, 0) # Change any NaN into a 0
    for i in reversed(range(0,len(all_vals))): # Delete any 0s in the array
        if all_vals[i][0] == 0:
            all_vals = np.delete(all_vals, i, axis=0)
    for i in reversed(range(0,len(all_vals))): # Delete any 0s in the array
        if all_vals[i][0] == all_vals[i-1][0]:
            all_vals = np.delete(all_vals, i, axis=0)
#===== I wrote this code ^^

    #print(f'values after sorting:\n{all_vals}')

    val_to_size = make_interp_spline(all_vals[:, 0], all_vals[:, 1]) # Makes the legend circles a reasonable size
    minv = np.min(values) # Min Value
    maxv = np.max(values) # Max Value
    print(f'minval={minv}, maxval={maxv}, minsize={np.min(sizes)}, maxsize={np.max(sizes)}, nstops={nstops}, log_scale={log_scale}')
    min_order, max_order = n_orders(minv, maxv) # Makes the log10 of min and max values
    val_range = maxv-minv # Get range
    # What do these mean
    vstops = [] # Value Stops
    sstops = [] # Size Stops
    if not log_scale:
        dv = val_range/(nstops-1) # Basically sperating the range into 4 chunks
        v = minv
        for i in range(nstops): # nstops = Number of Stops?
            if v > 10:
                vstops.append(int(v)) # Removing the decimals should the number be larger then 10
            else:
                vstops.append(v)
            sstops.append(val_to_size(v))
            v += dv 
    else: # Changing log back into exponents, I think
        do = (max_order - min_order) // (nstops-1)
        ord = min_order 
        for i in range(nstops):
            vstops.append(math.pow(10, ord))
            ord += do
            sstops.append(val_to_size(vstops[-1]))
    
    #print(f'value stops: {vstops}')
    #print(f'size stops: {sstops}')
    return vstops, sstops

def make_size_text(stops):
    labels = []
    mino, maxo = n_orders(stops[0], stops[1]) # Whats the point?
    if mino >= 0 and maxo <= 4:
        return [ f'{s}' for s in stops ]
    else:
        return [ f'{s:.1e}' for s in stops ]

def make_size_legend(ax, values, sizes, nstops, shape='o', title='None', log_scale=True, spacing=0.5):
    value_stops, size_stops = legend_helper(values, sizes, nstops, log_scale=log_scale)
    size_text = make_size_text(value_stops)
    size_values = size_stops
    #print(f'sizes are {size_values}')
    custom_circles = [ plt.Line2D(range(1), range(1), markersize=math.sqrt(s),
                                  color='white', marker=shape,
                                  markerfacecolor='white',
                                  markeredgecolor='black')
                       for s in size_values ]

    size_legend = ax.legend(custom_circles,
                         [ f"{s}" for s in size_text ],
                         title=title, title_fontproperties={'weight': 'bold'},loc='upper right',
                         bbox_to_anchor=(1, 1),
                         labelspacing=spacing)
    return size_legend
## End of legend.py code ========================================


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QtWidgets.QGridLayout(self.main_widget)
        self.width = 1

        self.mpl_canvas = FigureCanvas(Figure(figsize=(6, 4)))
        self.mpl_canvas2 = FigureCanvas(Figure(figsize=(6, 4)))

        #Adds options to the dropdown
        #To add a new widget, have to fill it in, then do layout.addwidget()
    #========== Widgets for Left Graph ==========
        self.dropdownX = QComboBox(self.main_widget)
        for name in dataX: 
            self.dropdownX.addItem(name)
        
        self.dropdownY = QComboBox(self.main_widget)
        for name in dataY: 
            self.dropdownY.addItem(name)
        
        self.dropdownColor = QComboBox(self.main_widget)
        for name in dataColor:
            self.dropdownColor.addItem(name)

        self.dropdownSize = QComboBox(self.main_widget)
        for name in dataSize: 
            self.dropdownSize.addItem(name)

        self.slider = QSlider(self.main_widget)
        self.slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)

    #========== Widgets for Right Graph ==========
        self.dropdownXR = QComboBox(self.main_widget)
        for name in dataX: 
            self.dropdownXR.addItem(name)
        
        self.dropdownYR = QComboBox(self.main_widget)
        for name in dataY: 
            self.dropdownYR.addItem(name)
        
        self.dropdownColorR = QComboBox(self.main_widget)
        for name in dataColor:
            self.dropdownColorR.addItem(name)

        self.dropdownSizeR = QComboBox(self.main_widget)
        for name in dataSize: 
            self.dropdownSizeR.addItem(name)

        self.sliderR = QSlider(self.main_widget)
        self.sliderR.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.sliderR.setMinimum(1)
        self.sliderR.setMaximum(100)
    #==============================================

        #layout.addWidget(NavigationToolbar(self.mpl_canvas, self), 0, 0, 1, 6) # (Arg,   Row/Y,Column/X,rowspan,columnspan)
        layout.addWidget(self.mpl_canvas,                          0, 0, 4, 4)
        #layout.addWidget(NavigationToolbar(self.mpl_canvas2, self), 1, 0, 4, 7) # (Arg,   Row/Y,Column/X,rowspan,columnspan)
        layout.addWidget(self.mpl_canvas2,                          0, 5 , 4, 4) # Rowspan = # rows it takes up, same for columnspan
        
    #===== Left Widgets ======
        layout.addWidget(QLabel('X-Axis'),                         5, 0, 1, 1) # Names the dropdown menu
        layout.addWidget(self.dropdownX,                           5, 1, 1, 1) # Adds the dropdown menu
        layout.addWidget(QLabel('Y-Axis'),                         6, 0, 1, 1)
        layout.addWidget(self.dropdownY,                           6, 1, 1, 1)
        layout.addWidget(QLabel('Size'),                           5, 2, 1, 1)
        layout.addWidget(self.dropdownSize,                        5, 3, 1, 1)
        layout.addWidget(QLabel('Color'),                          6, 2, 1, 1)
        layout.addWidget(self.dropdownColor,                       6, 3, 1, 1)
        layout.addWidget(QLabel('Scaling Factor'),                 7, 0, 1, 1)
        layout.addWidget(self.slider,                              7, 1, 1, 3)

        #===== Right Widgets ======
        layout.addWidget(QLabel('X-Axis'),                         5, 5, 1, 1) # Names the dropdown menu
        layout.addWidget(self.dropdownXR,                          5, 6, 1, 1) # Adds the dropdown menu
        layout.addWidget(QLabel('Y-Axis'),                         6, 5, 1, 1)
        layout.addWidget(self.dropdownYR,                          6, 6, 1, 1)
        layout.addWidget(QLabel('Size'),                           5, 7, 1, 1)
        layout.addWidget(self.dropdownSizeR,                       5, 8, 1, 1)
        layout.addWidget(QLabel('Color'),                          6, 7, 1, 1)
        layout.addWidget(self.dropdownColorR,                      6, 8, 1, 1)
        layout.addWidget(QLabel('Scaling Factor'),                 7, 5, 1, 1)
        layout.addWidget(self.sliderR,                             7, 6, 1, 3)

        #Create the plots
        self.ax = self.mpl_canvas.figure.subplots()
        self.ax2 = self.mpl_canvas2.figure.subplots()
        
        self.create_plot(df, x, y, df[color], size, sizeC)
        self.create_plotR(df, x, y, df[color], size, sizeC)

        abrush = Brush(app=self, df=df, colors=df[color], plot=self.ax, plot2=self.ax2, cb=self.update_CSelect, cb2=self.update_CSelectR)
        self.abrush = abrush

        # These vv are used to change the data on the graph.
        self.dropdownX.activated.connect(self.update_dataX)
        self.dropdownY.activated.connect(self.update_dataY)
        self.dropdownColor.activated.connect(self.update_dataC)
        self.dropdownSize.activated.connect(self.update_dataS)
        self.slider.valueChanged.connect(self.update_width)

        self.dropdownXR.activated.connect(self.update_dataXR)
        self.dropdownYR.activated.connect(self.update_dataYR)
        self.dropdownColorR.activated.connect(self.update_dataCR)
        self.dropdownSizeR.activated.connect(self.update_dataSR)
        self.sliderR.valueChanged.connect(self.update_widthR)
    


    #Creating the Plots
    def create_plot(self, d, x, y, colorL, size, sizeC): #This updates the graph.
        #ColorL = ColorLocal, ie the passed var vs the global one
    
        # Normalizing Size
        minR = 1 + sizeC
        maxR = 240 + 2*sizeC
        minV = df[size].min()
        maxV = df[size].max()
        norm_size = minR + ((df[size] - minV)/(maxV - minV)) * (maxR - minR)

        self.plots = self.ax.scatter(x=d[x], y=d[y], s=norm_size, c=colorL, cmap='plasma', alpha=.6)

        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y)
        self.ax.set_title("CIA Factbook 2023")

        #redraw rectangle
        self.abrush = Brush(app=self, df=df, colors=df[color], plot=self.ax, 
                    plot2=self.ax2, cb=self.update_CSelect, cb2=self.update_CSelectR)
        
        
        make_size_legend(self.ax, df[size], norm_size, 4, log_scale=False, spacing=1.5, title=size)
        
        #   Making the cmap
        cmap = mpl.colormaps["plasma"]
        cax=self.ax.inset_axes([.98, 0, 0.05, 1])
        cbar = plt.colorbar(cm.ScalarMappable(norm=colors.Normalize(0, df[data['c']].max()), cmap=cmap), cax=cax)
        cbar.set_label(data['c'])  
    def create_plotR(self, d, x, y, colorL, size, sizeC): #This updates the graph.
        #So you dont need to stick everything in a dictionary, it just makes it easier.
        #Just use global variables for every X/Y/etc
    
        # Normalizing Size
        minR = 1 + sizeC
        maxR = 240 + 2*sizeC
        minV = df[size].min()
        maxV = df[size].max()
        norm_size = minR + ((df[size] - minV)/(maxV - minV)) * (maxR - minR)

        self.plots2 = self.ax2.scatter(x=d[x], y=d[y], s=norm_size, c=colorL, cmap='plasma', alpha=.6)
        self.ax2.set_xlabel(x)
        self.ax2.set_ylabel(y)
        self.ax2.set_title("CIA Factbook 2023")
        self.abrush = Brush(app=self, df=df, colors=df[color], plot=self.ax, 
                            plot2=self.ax2, cb=self.update_CSelect, cb2=self.update_CSelectR)

        make_size_legend(self.ax2, df[size], norm_size, 4, log_scale=False, spacing=1.5, title=size)
        
        #   Making the cmap
        cmap = mpl.colormaps["plasma"]
        cax=self.ax2.inset_axes([.98, 0, 0.05, 1])
        cbar = plt.colorbar(cm.ScalarMappable(norm=colors.Normalize(0, df[dataR['c']].max()), cmap=cmap), cax=cax)
        cbar.set_label(dataR['c'])
    
        #Update Color Selection
    
    #Updating the plots after a selection
    def update_CSelect(self, pos):
        color
        if pos.empty: #Revert back to origional colors
            colors = df[data['c']]
        else: #Change the unselected colors to grey
            #Obtain the colors for all the points
            cmap = mpl.colormaps["plasma"]
            norm_points = df[data['c']]/df[data['c']].max()
            colors = cmap(norm_points)
            #print(colors)

            #Turn everything not selected grey
            for i in range(len(colors)):
                if i not in pos.index:
                    colors[i] = gray
 
        self.ax.clear()
        self.create_plot(df, data['x'], data['y'], colors, data['s'], data["sizeC"])
        #print(colors)
        self.mpl_canvas.draw()

    
            #Update Color Selection for R graph
    def update_CSelectR(self, pos):
        #color
        if pos.empty: #Revert back to origional colors
            colors = df[dataR['c']]
        else: #Change the unselected colors to grey
            #Obtain the colors for all the points
            cmap = mpl.colormaps["plasma"]
            norm_points = df[dataR['c']]/df[dataR['c']].max()
            colors = cmap(norm_points)
            #print(colors)

            #Turn everything not selected grey
            for i in range(len(colors)):
                if i not in pos.index:
                    colors[i] = gray
        
        self.ax2.clear()
        self.create_plotR(df, dataR['x'], dataR['y'], colors, dataR['s'], dataR["sizeC"])
        self.mpl_canvas2.draw()

    #Update X-Axis Variable
    def update_dataX(self, index):
        name = self.dropdownX.currentText()
        self.ax.clear()
        data["x"] = name
        self.create_plot(df, data['x'], data['y'], df[data['c']], data['s'], data["sizeC"])
        self.mpl_canvas.draw()

        #X-Axis Right Graph ======================================
    def update_dataXR(self, index):
        name = self.dropdownXR.currentText()
        self.ax2.clear()
        dataR["x"] = name
        self.create_plotR(df, dataR['x'], dataR['y'], df[dataR['c']], dataR['s'], dataR["sizeC"])
        self.mpl_canvas2.draw()

    #Update Y-Axis Variable
    def update_dataY(self, index):
        name = self.dropdownY.currentText()
        self.ax.clear()
        data["y"] = name
        self.create_plot(df, data['x'], data['y'], df[data['c']], data['s'], data["sizeC"])
        self.mpl_canvas.draw()

        #Y-Axis Right Graph  ======================================
    def update_dataYR(self, index):
        name = self.dropdownYR.currentText()
        self.ax2.clear()
        dataR["y"] = name
        self.create_plotR(df, dataR['x'], dataR['y'], df[dataR['c']], dataR['s'], dataR["sizeC"])
        self.mpl_canvas2.draw()
    
    #Update Color Variable
    def update_dataC(self, index):
        name = self.dropdownColor.currentText()
        self.ax.clear()
        data["c"] = name
        self.create_plot(df, data['x'], data['y'], df[data['c']], data['s'], data["sizeC"])
        self.mpl_canvas.draw()

        #Color Right Graph  ======================================
    def update_dataCR(self, index):
        name = self.dropdownColorR.currentText()
        self.ax2.clear()
        dataR["c"] = name
        self.create_plotR(df, dataR['x'], dataR['y'], df[dataR['c']], dataR['s'], dataR["sizeC"])
        self.mpl_canvas2.draw()


    #Update Size Variable
    def update_dataS(self, index):
        name = self.dropdownSize.currentText()
        self.ax.clear()
        data["s"] = name
        self.create_plot(df, data['x'], data['y'], df[data['c']], data['s'], data["sizeC"])
        self.mpl_canvas.draw()

        #Size Right Graph  ======================================
    def update_dataSR(self, index):
        name = self.dropdownSizeR.currentText()
        self.ax2.clear()
        dataR["s"] = name
        self.create_plotR(df, dataR['x'], dataR['y'], df[dataR['c']], dataR['s'], dataR["sizeC"])
        self.mpl_canvas2.draw()

    #Update size
    def update_width(self, width):
        data["sizeC"] = width
        self.ax.clear()
        self.create_plot(df, data['x'], data['y'], df[data['c']], data['s'], data["sizeC"])
        self.mpl_canvas.draw()

        #Size Right Graph  ======================================
    def update_widthR(self, width):
        dataR["sizeC"] = width
        self.ax2.clear()
        self.create_plotR(df, dataR['x'], dataR['y'], df[dataR['c']], dataR['s'], dataR["sizeC"])
        self.mpl_canvas2.draw()

## Start of brushing.py code ========================================
class Brush:
    def __init__(self, df, colors, plot: mpl.axes, plot2: mpl.axes, app, cb, cb2, column1=None, column2=None):
        self.df = df
        self.colors = colors
        self.selected = [] #Select Left Graph
        self.selected2 = [] #Select Right graph
        self.plot = plot #Left Graph
        self.plot2 = plot2 #Right Graph
        self.app = app
        self.cb = cb #Callback function
        self.cb2 = cb2 #Callback function

        self.rec = RectangleSelector(plot, cb)
        self.rec2 = RectangleSelector(plot2, cb2)

        #These functions take the position and color the specific points
        #self.helperL = helperL
        #self.helperR = helperR

    def callback(self, eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata #Notes the first click loc. of the selection rectangle
        x2, y2 = erelease.xdata, erelease.ydata #Notes the release location of the selec. rec.
        
        #print("x1: ",x1)
        selected = []
        # vv Puts selected into an array
        self.selected = df[(df[data['x']].between(x1, x2, inclusive='both') & df[data['y']].between(y1, y2, inclusive='both'))]
        #print('the selected data points are: {}'.format(list(self.selected.index)))
                
        self.cb(self.selected)
        self.cb2(self.selected)

    def callback2(self, eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata #Notes the first click loc. of the selection rectangle
        x2, y2 = erelease.xdata, erelease.ydata #Notes the release location of the selec. rec.
        
        #print("x1: ",x1)
        selected = []
        # vv Puts selected into an array
        self.selected2 = df[(df[dataR['x']].between(x1, x2, inclusive='both') & df[dataR['y']].between(y1, y2, inclusive='both'))]
        #print('the selected data points are: {}'.format(list(self.selected.index)))
                
        self.cb2(self.selected2)
        self.cb(self.selected2)

## End of brushing.py code ========================================

if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    parser = ap.ArgumentParser(description='CS439: Part 2, Bubble Chart')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path of Excel workbook')
    args = parser.parse_args()

    global df #Make the df a global variable so it can be used in the AppWindow func
    df = pd.read_excel(args.input)
    df = df.fillna(0)

    app = ApplicationWindow()
    brush = Brush(df, df[color], plot=app.ax, plot2=app.ax2, app=app, cb=app.update_CSelect, cb2=app.update_CSelectR)
    selector = RectangleSelector(app.ax, brush.callback)
    selector2 = RectangleSelector(app.ax2, brush.callback2)

    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()