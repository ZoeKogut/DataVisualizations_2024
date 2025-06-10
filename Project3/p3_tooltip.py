import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

import pandas as pd
import numpy as np
import argparse as ap
import geopandas

import math



def make_size_legend(minR, maxR, minV, maxV, bb_to_achor, shape='o', spacing=0.5):
    size_text = ['10','100','1000','1800']
    size_values = [10,100,1000,1800]
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

def make_color_legend(maxC, cmap, bb_to_achor, shape='o', spacing=0.5):
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

def make_line_width_legend(minR, minNoF, maxNoF, maxSize, bb_to_achor, spacing=0.5):
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

#Update Annot for airports
def update_annot_airports(ind, diff, pos):
    annot.xy = pos

    #Get each text beforehand and then join it all together in one big text string
    ind_index = ind["ind"][0]

    if diff == 1: #Airport?
        airport_code = airports_sorted.iloc[ind_index, 2]

        text_name = airports_sorted.iloc[ind_index, 4] #Airport Name
        text_city = airports_sorted.iloc[ind_index, 6] #City Airport is in
        text_province = airports_sorted.iloc[ind_index, 8] #Province Airport is in
        text_country = airports_sorted.iloc[ind_index, 7] #Country Airport is in
        text_degree = ap_degree[airport_code] #Degree
        text_importance = ap_importance[airport_code] #Importance
        text_str = "Name: {}\n City: {}\n Province: {}\n Country: {}\n Degree: {}\n Importance: {}"
        text = text_str.format(text_name, text_city, text_province, text_country, text_degree, text_importance)
    
    elif diff == 2: #Flight path
        apt1 = flight_sorted.iloc[ind_index, 0]
        apt2 = flight_sorted.iloc[ind_index, 1]

        text_airport1 = ap_full_name[apt1]
        text_airport2 = ap_full_name[apt2]
        text_flights = flight_sorted.iloc[ind_index, 2]
        text_airlines = ", ".join(flight_sorted.iloc[ind_index, 4])
        text_str = "Airport1: {}\n Airport2: {}\n Flight: {}\n Airlines: {}"
        text = text_str.format(text_airport1, text_airport2, text_flights, text_airlines)

    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor("pink")
    annot.get_bbox_patch().set_alpha(1)

#Hover func
def hover(event):
    #print("ap: ",air_plot)
    vis = annot.get_visible()
    if event.inaxes == ax:
        pos = [event.xdata,event.ydata]
        cont, ind = air_plot.contains(event)
        cont2, ind2 = air_plot_flights.contains(event)
        if cont:
            update_annot_airports(ind, 1, pos)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        elif cont2:
            update_annot_airports(ind2, 2, pos)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='CS439: Part 1, Bargraph')
    parser = ap.ArgumentParser(description='CS439: Simple Scatter Plot Example')
    parser.add_argument('-m', '--map', type=str, required=True, help='Map of the world in GeoJSON format')
    parser.add_argument('-a', '--airports', type=str, required=True, help='Airports and their geolocation in an Excel spreadsheet')
    parser.add_argument('-f', '--flights', type=str, required=True, help='List of all the flights in a JSON format')
    args = parser.parse_args()

    airports = pd.read_excel(args.airports)
    flights = pd.read_json(args.flights)
    map = geopandas.read_file(args.map)

    #Getting the 200 largest number of flights
    flight_sorted = flights.sort_values("number_of_flights")
    flight_sorted = flight_sorted.tail(200)
    flight_sorted = flight_sorted.reset_index(drop=True)

    
    ap_names = {} #Dictionary of all the Airport Names and their Lat/Long (Used in ploting the flights later)
    ap_importance = {} #Number of flights that go through this airport (used in tooltip)
    ap_NoF = {} #Gets all of the airlines that travel through this airport
    ap_NoF_Count = {} #Gets the number of different airlines that travel through this airport
    ap_degree = {} #Gets the number of airports an airport is connected to (+1 per flight)
    ap_full_name = {} #Gets the full name for the airport based on the code (used in tooltip later)

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

    minR = 1
    maxR = 100
    minV = float('inf')
    maxV = float('-inf')
    for i in ap_importance: #Because its an array you have to search through it for max/min by hand
        if ap_importance[i] > maxV:
            maxV = ap_importance[i]
        elif ap_importance[i] < minV:
            minV = ap_importance[i]
    
    maxC = float('-inf')
    for i in ap_NoF_Count: #Because its an array you have to search through it for max/min by hand
        if ap_NoF_Count[i] > maxC:
            maxC = ap_NoF_Count[i]

    #Normalize the size of the different points
    norm_size = minR + ((ap_imp_sort_df - minV)/(maxV - minV)) * (maxR - minR)
    
    minNoF = flight_sorted['number_of_flights'].min() #Min Number of Flights
    maxNoF = flight_sorted['number_of_flights'].max() #Max Number of Flights
    maxSize = 10
    norm_width = minR + ((flight_sorted['number_of_flights'] - minNoF)/(maxNoF - minNoF)) * (maxSize - minR)
    norm_alpha = flight_sorted['number_of_flights']/(maxNoF)

    #Colorcode the points
    cmap = mpl.colormaps["plasma"]
    norm_points = ap_NoF_sort_df/maxC
    colors = cmap(norm_points)

    #Create the figure
    fig, ax = plt.subplots(figsize=(10, 6))
    map.plot(ax=ax, color='white', edgecolor='black', zorder=0)
    airports_sorted = airports.sort_values('IATA')
    air_plot = ax.scatter(airports_sorted["Longitude"], airports_sorted["Latitude"], s=norm_size, color=colors, marker='o', edgecolors='black', zorder=10)

    #Making the legends
    size_legend = make_size_legend(minR, maxR, minV, maxV, (1, 1.2))
    color_legend = make_color_legend(maxC, cmap, (1, .79))
    third_legend = make_line_width_legend(minR, minNoF, maxNoF, maxSize, (1, 0.3))

    ax.add_artist(size_legend)
    ax.add_artist(color_legend)
    ax.add_artist(third_legend)
    ax.set_position([0.1, 0.1, 0.6, 0.8])

    #Normalize the colors for the edges
    cmapBlues = mpl.colormaps["Blues"]
    maxNoF = minR + ((maxNoF - minNoF)/(maxNoF - minNoF)) * (maxSize - minR)
    lineColors = cmapBlues(norm_width/(maxSize))
    
    lines = []
    
    #air_plot_flights = []

    #Taking the heaviest 200 flights and plotting them using the dict
    for i in range(0, len(flight_sorted)): #Range of the flights 200 heaviest flights
        ap1x, ap1y = ap_names[flight_sorted.at[i, 'origin']] #Coords for the start airport
        ap2x, ap2y = ap_names[flight_sorted.at[i, 'destination']] #cords for the end airport
        lines.append([(ap1x,ap1y),(ap2x,ap2y)])
        #ax.plot([ap1x, ap2x], [ap1y, ap2y], 'b-', mfc='C1', mec='C1', zorder=5, linewidth=norm_width[i], color=lineColors[i])
                                                                                        #mfc, marker face color; mec, marker edge color
                                                                                        #zorder, the order of items being drawn on a graph
    air_plot_flights = LineCollection(lines, color=lineColors, linewidth=norm_width, zorder=5)
    ax.add_collection(air_plot_flights)
    #Save ax.plot return similar to air_plot

    ax.set_title("World Airports and the 200 Busiest Routes")

    #Tooltips yee
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"), zorder=20)
    annot.set_visible(False)
    
    fig.canvas.mpl_connect("motion_notify_event", hover)
    

    plt.show()
