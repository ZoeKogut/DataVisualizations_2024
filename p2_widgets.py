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
# These vv should be changed whenever the dropdown menu is
x = "GDP_per_capita"
y = "military_expenditures"
color = "population"
size = "life_expectancy"
sizeC = 0
data = {"x": x, "y": y, "c": color, "s": size, "xlabel": x, "ylabel": y, "sizeC": sizeC}
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
    
    print(f'value stops: {vstops}')
    print(f'size stops: {sstops}')
    return vstops, sstops

def make_size_text(stops):
    labels = []
    mino, maxo = n_orders(stops[0], stops[1]) # Whats the point?
    if mino >= 0 and maxo <= 4:
        return [ f'{s}' for s in stops ]
    else:
        return [ f'{s:.1e}' for s in stops ]

def make_size_legend(self, values, sizes, nstops, shape='o', title='None', log_scale=True, spacing=0.5):
    value_stops, size_stops = legend_helper(values, sizes, nstops, log_scale=log_scale)
    size_text = make_size_text(value_stops)
    size_values = size_stops
    print(f'sizes are {size_values}')
    custom_circles = [ plt.Line2D(range(1), range(1), markersize=math.sqrt(s),
                                  color='white', marker=shape,
                                  markerfacecolor='white',
                                  markeredgecolor='black')
                       for s in size_values ]

    size_legend = self.ax.legend(custom_circles,
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

        self.mpl_canvas = FigureCanvas(Figure(figsize=(10, 6)))

        #Adds options to the dropdown
        #To add a new widget, have to fill it in, then do layout.addwidget()
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

        layout.addWidget(NavigationToolbar(self.mpl_canvas, self), 0, 0, 1, 6) # (Arg,   Row/Y,Column/X,Alignment)
        layout.addWidget(self.mpl_canvas,                          1, 0, 6, 4)
        layout.addWidget(QLabel('X-Axis'),                         1, 4, 1, 1) # Names the dropdown menu
        layout.addWidget(self.dropdownX,                           1, 5, 1, 1) # Adds the dropdown menu
        layout.addWidget(QLabel('Y-Axis'),                         2, 4, 1, 1)
        layout.addWidget(self.dropdownY,                           2, 5, 1, 1)
        layout.addWidget(QLabel('Size'),                           3, 4, 1, 1)
        layout.addWidget(self.dropdownSize,                        3, 5, 1, 1)
        layout.addWidget(QLabel('Color'),                          4, 4, 1, 1)
        layout.addWidget(self.dropdownColor,                       4, 5, 1, 1)
        layout.addWidget(QLabel('Dot Size'),                       5, 4, 1, 1)
        layout.addWidget(self.slider,                              5, 5, 1, 1)

        self.ax = self.mpl_canvas.figure.subplots()
        self.create_plot(df, x, y, color, size, sizeC)

        # These vv are used to change the data on the graph.
        self.dropdownX.activated.connect(self.update_dataX)
        self.dropdownY.activated.connect(self.update_dataY)
        self.dropdownColor.activated.connect(self.update_dataC)
        self.dropdownSize.activated.connect(self.update_dataS)
        self.slider.valueChanged.connect(self.update_width)

    def create_plot(self, d, x, y, color, size, sizeC): #This updates the graph.
        #So you dont need to stick everything in a dictionary, it just makes it easier.
        #Just use global variables for every X/Y/etc
        
        # Normalizing Size
        minR = 1 + sizeC
        maxR = 240 + 2*sizeC
        minV = df[size].min()
        maxV = df[size].max()
        norm_size = minR + ((df[size] - minV)/(maxV - minV)) * (maxR - minR)

        self.plots = self.ax.scatter(x=d[x], y=d[y], s=norm_size, c=df[color], cmap='plasma', alpha=0.6)
        print("Color ", df[color])
        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y)
        self.ax.set_title('CIA Factbook')

        make_size_legend(self, df[size], norm_size, 4, log_scale=False, spacing=1.5, title='Size')
        
        #   Making the cmap
        cmap = mpl.colormaps["plasma"]
        cax=self.ax.inset_axes([.98, 0, 0.05, 1])
        cbar = plt.colorbar(cm.ScalarMappable(norm=colors.Normalize(0, df[color].max()), cmap=cmap), cax=cax)
        cbar.set_label(color)


    #Update X-Axis Variable
    def update_dataX(self, index):
        name = self.dropdownX.currentText()
        self.ax.clear()
        data["x"] = name
        self.plots = self.create_plot(df, data['x'], data['y'], data['c'], data['s'], data["sizeC"])
        self.mpl_canvas.draw()

    #Update Y-Axis Variable
    def update_dataY(self, index):
        name = self.dropdownY.currentText()
        self.ax.clear()
        data["y"] = name
        self.plots = self.create_plot(df, data['x'], data['y'], data['c'], data['s'], data["sizeC"])
        self.mpl_canvas.draw()
    
    #Update Color Variable
    def update_dataC(self, index):
        name = self.dropdownColor.currentText()
        self.ax.clear()
        data["c"] = name
        self.plots = self.create_plot(df, data['x'], data['y'], data['c'], data['s'], data["sizeC"])
        self.mpl_canvas.draw()

    #Update Size Variable
    def update_dataS(self, index):
        name = self.dropdownSize.currentText()
        self.ax.clear()
        data["s"] = name
        self.plots = self.create_plot(df, data['x'], data['y'], data['c'], data['s'], data["sizeC"])
        self.mpl_canvas.draw()

    #Update size
    def update_width(self, width):
        data["sizeC"] = width
        self.ax.clear()
        self.plots = self.create_plot(df, data['x'], data['y'], data['c'], data['s'], data["sizeC"])
        self.mpl_canvas.draw()




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

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()

    ## ================== Everything below will be deleted ====================


"""
    minR = 50
    maxR = 500
    minV = df["population"].min()
    maxV = df["population"].max()

#Normalize the size so it isnt too large
    norm_size = minR + ((df["population"] - minV)/(maxV - minV)) * (maxR - minR)

#Making the Grpah
    fig, axes = plt.subplots(1,1,figsize=(8,6))
    axes.scatter(df["GDP_per_capita"], df["military_expenditures"], s=norm_size, c=df["life_expectancy"], cmap='plasma', alpha=0.6)
    plt.xlabel("GDP_per_capita")
    plt.ylabel("military_expenditures")
    plt.title("GDP_per_capita, military_expenditures, population, and life_expectancy")

    size_legend = make_size_legend(df["population"], norm_size, 4, log_scale=False, spacing=1.5, title='Size')
    axes.add_artist(size_legend)

    cmap = cm.get_cmap("plasma")
    cbar = plt.colorbar(cm.ScalarMappable(norm=colors.Normalize(0, df["life_expectancy"].max()), cmap=cmap))
    cbar.set_label("life_expectancy")    

    plt.show()
"""