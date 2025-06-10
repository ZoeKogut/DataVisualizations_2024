import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QGridLayout, QPushButton, QComboBox, QSlider, QLabel

import pandas as pd
import numpy as np
import argparse as ap
import geopandas

import math



def make_size_legend(minR, maxR, minV, maxV, bb_to_achor, ax, shape='o', spacing=0.5):
    size_text = ['10','100','1000','1800']
    size_values = np.array([10,100,1000,1800])
    size_values = minR + ((size_values - minV)/(maxV - minV)) * (maxR - minR)

    custom_circles = [ plt.Line2D(range(1), range(1), markersize=math.sqrt(s),
                                  color='white', marker=shape,
                                  markerfacecolor='white',
                                  markeredgecolor='black')
                       for s in size_values ]

    size_legend = ax.legend(custom_circles,
                         [ f"{s}" for s in size_text ],
                         title="Airport Signifigance", title_fontproperties={'weight': 'bold'},loc='upper left',
                         bbox_to_anchor=bb_to_achor,
                         labelspacing=spacing)
    return size_legend

def make_color_legend(maxC, cmap, bb_to_achor, ax, shape='o', spacing=0.5):
    color_text = ['5','10','30','75', '100']
    color_values = np.array([5, 10, 30, 75, 100])
    color_values = cmap(color_values/maxC)
    
    custom_circles = [ plt.Line2D(range(1), range(1), markersize=10,
                                  color='white', marker=shape,
                                  markerfacecolor=c,
                                  markeredgecolor='black')
                       for c in color_values ]

    color_legend = ax.legend(custom_circles,
                         [ f"{s}" for s in color_text ],
                         title="Number of Airlines", title_fontproperties={'weight': 'bold'},loc='upper left',
                         bbox_to_anchor=bb_to_achor,
                         labelspacing=spacing)
    return color_legend

def make_line_width_legend(minR, minNoF, maxNoF, maxSize, bb_to_achor, ax, spacing=0.5):
    lineW_text = ['8','16','24','32', '39']
    lineW_values = np.array([8, 16, 24, 32, 39])
    lineW_values = minR + ((lineW_values - minNoF)/(maxNoF - minNoF)) * (maxSize - minR)
    maxNoF = minR + ((maxNoF - minNoF)/(maxNoF - minNoF)) * (maxSize - minR)


    cmap_Blues = mpl.colormaps["Blues"]
    lineColors = cmap_Blues(lineW_values/maxNoF)
    custom_lines = [plt.Line2D([], [], lw=lineW_values[i] ,color=lineColors[i]) for i in range(len(lineW_values))]

    lineWidth_legend = ax.legend(custom_lines,
                         [ f"{s}" for s in lineW_text ],
                         title="Number of Flights", title_fontproperties={'weight': 'bold'},loc='upper left',
                         bbox_to_anchor=bb_to_achor,
                         labelspacing=spacing)
    return lineWidth_legend

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QtWidgets.QGridLayout(self.main_widget)
        self.width = 1

        #200 is the base case, call this funtion to recalc whenever the slider changes
        self.flight_sorted = flights.sort_values("number_of_flights")
        self.flight_sorted_subset = self.flight_sorted#.tail(200) #Get the subset of 200
        self.flight_sorted_subset = self.flight_sorted_subset.reset_index(drop=True)
        
        global ap_names      #Dictionary of all the Airport Names and their Lat/Long (Used in ploting the flights later)
        global ap_importance #Number of flights that go through this airport (used in tooltip and EC slider)
        global ap_NoF        #Gets all of the airlines that travel through this airport
        global ap_NoF_Count  #Gets the number of different airlines that travel through this airport
        global ap_degree     #Gets the number of airports an airport is connected to (+1 per flight)
        global ap_full_name  #Gets the full name for the airport based on the code (used in tooltip later)
        
        ap_names = {} 
        ap_importance = {} 
        ap_NoF = {} 
        ap_NoF_Count = {} 
        ap_degree = {} 
        ap_full_name = {} 

        self.NoF = 1 #Starting Min NoF for edge slider
        self.imp = 1 #Starting Min Importance for airport slider

        self.df_imp = airports[["IATA", "Longitude", "Latitude"]] #Gets the IATA/Long/Lat (importance added later) for easy access in the sliders

        #Initalizes all the dictionaries used in the program
        for i in range(len(airports)):
            ap_names[airports.at[i, 'IATA']] = (airports.at[i, 'Longitude'], airports.at[i, 'Latitude'])
            ap_importance[airports.at[i, 'IATA']] = 0 #Creates all the enteries for the next loop
            ap_NoF[airports.at[i, 'IATA']] = [] 
            ap_NoF_Count[airports.at[i, 'IATA']] = 0
            ap_degree[airports.at[i, 'IATA']] = 0
            ap_full_name[airports.at[i, 'IATA']] = airports.at[i, 'Airport name']
        
        #Gets the importance for every airport
        for i in range(len(flights)):
            ap_importance[flights.at[i, 'origin']] += flights.at[i, 'number_of_flights']
            ap_importance[flights.at[i, 'destination']] += flights.at[i, 'number_of_flights']

            ap_degree[flights.at[i, 'origin']] += 1 #For every flight through an airport, add 1
            ap_degree[flights.at[i, 'destination']] += 1
            
            #Gets the number of airlines that travel through the airports
            for j in flights.at[i, 'airlines']:
                if j not in ap_NoF[flights.at[i, 'origin']] :
                    ap_NoF[flights.at[i, 'origin']].append(j)
                    ap_NoF_Count[flights.at[i, 'origin']] += 1
                if j not in ap_NoF[flights.at[i, 'destination']]:
                    ap_NoF[flights.at[i, 'destination']].append(j)
                    ap_NoF_Count[flights.at[i, 'destination']] += 1

        #Sort the dict based on the airport names, then put the importance values in an array
        ap_importance_sorted = dict(sorted(ap_importance.items()))
        ap_imp_sort_df = np.fromiter(ap_importance_sorted.values(), dtype=int)

        ap_NoF_sorted = dict(sorted(ap_NoF_Count.items()))
        ap_NoF_sort_df = np.fromiter(ap_NoF_sorted.values(), dtype=int)

        ap_degree_sorted = dict(sorted(ap_degree.items()))
        ap_degree_df = np.fromiter(ap_degree_sorted.values(), dtype=int)

        airports_sorted = airports.sort_values("IATA")

        self.df_imp.sort_values("IATA", inplace=True)
        self.df_imp.insert(3, "Importance", ap_imp_sort_df, True)
        self.df_imp.insert(4, "NoF", ap_NoF_sort_df, True)
        self.df_imp.insert(5, "Airport name", airports_sorted["Airport name"], True)
        self.df_imp.insert(6, "City", airports_sorted["City"], True)
        self.df_imp.insert(7, "Province", airports_sorted["Province"], True)
        self.df_imp.insert(8, "Country", airports_sorted["Country"], True)
        self.df_imp.insert(9, "Degree", ap_degree_df, True)


        minR = 1
        maxR = 100
        self.minV = self.df_imp["Importance"].min()
        self.maxV = self.df_imp["Importance"].max()
        
        maxC = float('-inf')
        for i in ap_NoF_Count: #Because its an array you have to search through it for max/min by hand
            if ap_NoF_Count[i] > maxC:
                maxC = ap_NoF_Count[i]

        #Normalize the size of the different points
        norm_size = minR + ((ap_imp_sort_df - self.minV)/(self.maxV - self.minV)) * (maxR - minR)
        
        self.minNoF = self.flight_sorted_subset['number_of_flights'].min() #Min Number of Flights
        self.maxNoF = self.flight_sorted_subset['number_of_flights'].max() #Max Number of Flights
        self.maxSize = 10
        norm_width = minR + ((self.flight_sorted_subset['number_of_flights'] - self.minNoF)/(self.maxNoF - self.minNoF)) * (self.maxSize - minR)

        
        #Colorcode the points
        self.cmap = mpl.colormaps["plasma"]
        norm_points = ap_NoF_sort_df/maxC
        colors = self.cmap(norm_points)

        #Create the figure
        self.mpl_canvas = FigureCanvas(Figure(figsize=(10, 6)))
        print(self.maxV)

        #Initialize the sliders
        self.sliderNode = QSlider(self.main_widget)
        self.sliderNode.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.sliderNode.setTracking(False)
        self.sliderNode.setMinimum(1)
        self.sliderNode.setMaximum(self.maxV)

        self.sliderEdge = QSlider(self.main_widget)
        self.sliderEdge.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.sliderNode.setTracking(False)
        self.sliderEdge.setMinimum(1)
        self.sliderEdge.setMaximum(self.maxNoF)

        self.labelNode = QLabel('Node value: 1')
        self.labelEdge = QLabel('Edge value: 1')


        layout.addWidget(NavigationToolbar(self.mpl_canvas, self),     0, 0, 1, 6)
        layout.addWidget(self.mpl_canvas,                              1, 0, 4, 4)
        layout.addWidget(self.labelNode,                               5, 0, 1, 1)
        layout.addWidget(self.sliderNode,                              5, 1, 1, 4)
        layout.addWidget(self.labelEdge,                               6, 0, 1, 1)
        layout.addWidget(self.sliderEdge,                              6, 1, 1, 4)

        self.ax = self.mpl_canvas.figure.subplots()

        maps.plot(ax=self.ax, color='white', edgecolor='black', zorder=0)
        self.airports_sorted = airports.sort_values('IATA')
        self.airports_sorted_subset = self.df_imp
        self.air_plot = self.ax.scatter(self.airports_sorted["Longitude"], self.airports_sorted["Latitude"], s=norm_size, color=colors, marker='o', edgecolors='black', zorder=10)

        #Making the legends
        size_legend = make_size_legend(minR, maxR, self.minV, self.maxV, (1, 1.2), self.ax)
        color_legend = make_color_legend(maxC, self.cmap, (1, .79), self.ax)
        third_legend = make_line_width_legend(minR, self.minNoF, self.maxNoF, self.maxSize, (1, 0.3), self.ax)

        self.ax.add_artist(size_legend)
        self.ax.add_artist(color_legend)
        self.ax.add_artist(third_legend)
        self.ax.set_position([0.1, 0.1, 0.6, 0.8])

        #Normalize the colors for the edges
        
        #maxNoF = minR + ((self.maxNoF - self.minNoF)/(self.maxNoF - self.minNoF)) * (self.maxSize - minR)
        
        lines = []
        for i in range(0, len(self.flight_sorted_subset)): #Range of the flights 200 heaviest flights
            ap1x, ap1y = ap_names[self.flight_sorted_subset.at[i, 'origin']] #Coords for the start airport
            ap2x, ap2y = ap_names[self.flight_sorted_subset.at[i, 'destination']] #cords for the end airport
            lines.append([(ap1x,ap1y),(ap2x,ap2y)])
        norm_width = 1 + ((self.flight_sorted_subset['number_of_flights'] - self.minNoF)/(self.maxNoF - self.minNoF)) * (self.maxSize - 1)

        cmapBlues = mpl.colormaps["Blues"]
        self.lineColors = cmapBlues(norm_width/(10))

        self.air_plot_flights = LineCollection(lines, color=self.lineColors, linewidth=norm_width, zorder=5)
        self.ax.add_collection(self.air_plot_flights)
        

        #Taking the heaviest 200 flights and plotting them using the dict

        self.ax.set_title("Major Air Routes")

        self.sliderNode.valueChanged.connect(self.redraw_airports)
        self.sliderEdge.valueChanged.connect(self.redraw_flights)

        #Tooltips yee
        #If -notooltip is included this wont activate
        if args.notooltip == True:
            self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"), zorder=20)
            self.annot.set_visible(False)
            self.mpl_canvas.figure.canvas.mpl_connect("motion_notify_event", self.hover)

    

    #When slider is updated, redraw the airports shown
    def redraw_airports(self, importance):
        self.air_plot.remove() #Clear the origional airports
        self.imp = importance

        #Get the importance
        self.airports_sorted_subset = self.df_imp[self.df_imp["Importance"] >= importance]
        self.airports_sorted_subset.sort_values(by="Importance", inplace=True)
        self.airports_sorted_subset = self.airports_sorted_subset.reset_index(drop=True)

        print("NoF ",self.NoF)
        self.redraw_flights(self.NoF)

        #maxC = self.airports_sorted_subset["NoF"].max()
        norm_points = self.airports_sorted_subset["NoF"]/self.df_imp["NoF"].max()
        colors = self.cmap(norm_points)
        
        norm_size = ((self.airports_sorted_subset["Importance"] - self.minV)/(self.maxV - self.minV)) * (100)
        self.air_plot = self.ax.scatter(self.airports_sorted_subset["Longitude"], self.airports_sorted_subset["Latitude"], s=norm_size, color=colors, marker='o', edgecolors='black', zorder=10)
        
        self.labelNode.setText(f"Node Value: {importance}")

        
    def redraw_flights(self, NoF):
        self.air_plot_flights.remove() #Clear the original flights
        self.NoF = NoF

        lines = []
        temp_flight_ss = []
        self.flight_sorted_subset = self.update_flights(NoF) #Obtain the subsection of Flights Sorted that you need
        for i in range(0, len(self.flight_sorted_subset)): #Range of the flights 200 heaviest flights
            if self.airports_sorted_subset["IATA"].isin([self.flight_sorted_subset.at[i, 'origin']]).any().any() and self.airports_sorted_subset["IATA"].isin([self.flight_sorted_subset.at[i, 'destination']]).any().any():
                temp_flight_ss.append(1)
                ap1x, ap1y = ap_names[self.flight_sorted_subset.at[i, 'origin']] #Coords for the start airport
                ap2x, ap2y = ap_names[self.flight_sorted_subset.at[i, 'destination']] #cords for the end airport
                lines.append([(ap1x,ap1y),(ap2x,ap2y)])
            else:
                temp_flight_ss.append(0)
        self.flight_sorted_subset = self.flight_sorted_subset[np.array(temp_flight_ss,dtype=bool)]
        norm_width = 1 + ((self.flight_sorted_subset['number_of_flights'] - self.minNoF)/(self.maxNoF - self.minNoF)) * (self.maxSize - 1)
        cmapBlues = mpl.colormaps["Blues"]
        self.lineColors = cmapBlues(norm_width/(10))
        self.air_plot_flights = LineCollection(lines, color=self.lineColors, linewidth=norm_width, zorder=5)
        self.ax.add_collection(self.air_plot_flights)

        self.labelEdge.setText(f"Edge Value: {NoF}")

    #Get the top X flights
    def update_flights(self, numb):
        #Getting the 200 largest number of flights
        self.flight_sorted_subset = self.flight_sorted[self.flight_sorted["number_of_flights"] >= numb]
        self.flight_sorted_subset = self.flight_sorted_subset.reset_index(drop=True)
        print(self.flight_sorted_subset)
        return self.flight_sorted_subset
    
                #Update Annot for airports
    def update_annot_airports(self, ind, diff, pos):
            self.annot.xy = pos

            #Get each text beforehand and then join it all together in one big text string
            ind_index = ind["ind"][0]

            if diff == 1: #Airport?
                #airport_code = self.airports_sorted_subset.iloc[ind_index, 2]

                text_name = self.airports_sorted_subset.iloc[ind_index, 5] #Airport Name
                text_city = self.airports_sorted_subset.iloc[ind_index, 6] #City Airport is in
                text_province = self.airports_sorted_subset.iloc[ind_index, 8] #Province Airport is in
                text_country = self.airports_sorted_subset.iloc[ind_index, 7] #Country Airport is in
                text_degree = self.airports_sorted_subset.iloc[ind_index, 9] #Degree
                text_importance = self.airports_sorted_subset.iloc[ind_index, 3] #Importance
                text_str = "Name: {}\n City: {}\n Province: {}\n Country: {}\n Degree: {}\n Importance: {}"
                text = text_str.format(text_name, text_city, text_province, text_country, text_degree, text_importance)
            
            elif diff == 2: #Flight path
                apt1 = self.flight_sorted_subset.iloc[ind_index, 0]
                apt2 = self.flight_sorted_subset.iloc[ind_index, 1]

                text_airport1 = ap_full_name[apt1]
                text_airport2 = ap_full_name[apt2]
                text_flights = self.flight_sorted_subset.iloc[ind_index, 2]
                text_airlines = ", ".join(self.flight_sorted_subset.iloc[ind_index, 4])
                text_str = "Airport1: {}\n Airport2: {}\n Flights: {}\n Airlines: {}"
                text = text_str.format(text_airport1, text_airport2, text_flights, text_airlines)

            self.annot.set_text(text)
            self.annot.get_bbox_patch().set_facecolor("pink")
            self.annot.get_bbox_patch().set_alpha(1)

        #Hover func
    def hover(self, event):
        #print("ap: ",air_plot)
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            pos = [event.xdata,event.ydata]
            cont, ind = self.air_plot.contains(event)
            cont2, ind2 = self.air_plot_flights.contains(event)
            if cont:
                self.update_annot_airports(ind, 1, pos)
                self.annot.set_visible(True)
                self.mpl_canvas.figure.canvas.draw_idle()
            elif cont2:
                self.update_annot_airports(ind2, 2, pos)
                self.annot.set_visible(True)
                self.mpl_canvas.figure.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.mpl_canvas.figure.canvas.draw_idle()

if __name__ == '__main__':
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    parser = ap.ArgumentParser(description='CS439: Part 1, Bargraph')
    parser = ap.ArgumentParser(description='CS439: Simple Scatter Plot Example')
    parser.add_argument('-m', '--map', type=str, required=True, help='Map of the world in GeoJSON format')
    parser.add_argument('-a', '--airports', type=str, required=True, help='Airports and their geolocation in an Excel spreadsheet')
    parser.add_argument('-f', '--flights', type=str, required=True, help='List of all the flights in a JSON format')
    parser.add_argument('-notooltip', action="store_false", required=False, help='Include to turn off tooltip')
    args = parser.parse_args()

    global airports
    global flights
    global maps
    airports = pd.read_excel(args.airports)
    flights = pd.read_json(args.flights)
    maps = geopandas.read_file(args.map)

        
    app = ApplicationWindow()

    #plt.show()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()
