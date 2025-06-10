import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

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

    #Making a dictionary of the airport and its lat/long
    ap_names = {}
    ap_importance = {}
    ap_NoF = {}
    ap_NoF_Count = {}
    for i in range(len(airports)):
        ap_names[airports.at[i, 'IATA']] = (airports.at[i, 'Longitude'], airports.at[i, 'Latitude'])
        ap_importance[airports.at[i, 'IATA']] = 0 #Creates all the enteries for the next loop
        ap_NoF[airports.at[i, 'IATA']] = [] 
        ap_NoF_Count[airports.at[i, 'IATA']] = 0
    
    #Gets the importance for every airport
    for i in range(len(flights)):
        ap_importance[flights.at[i, 'origin']] += flights.at[i, 'number_of_flights']
        ap_importance[flights.at[i, 'destination']] += flights.at[i, 'number_of_flights']
        
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
    print(maxC)
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
    ax.scatter(airports_sorted["Longitude"], airports_sorted["Latitude"], s=norm_size, color=colors, marker='o', edgecolors='black', zorder=10)
    
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
    lineColors = cmapBlues(norm_width/(maxNoF))

    #Taking the heaviest 200 flights and plotting them using the dict
    for i in range(0, len(flight_sorted)): #Range of the flights 200 heaviest flights
        ap1x, ap1y = ap_names[flight_sorted.at[i, 'origin']] #Coords for the start airport
        ap2x, ap2y = ap_names[flight_sorted.at[i, 'destination']] #cords for the end airport
        ax.plot([ap1x, ap2x], [ap1y, ap2y], 'b-', mfc='C1', mec='C1', zorder=5, linewidth=norm_width[i], color=lineColors[i]) 
                                                                                        #mfc, marker face color; mec, marker edge color
                                                                                        #zorder, the order of items being drawn on a graph
    
    ax.set_title("World Airports and the 200 Busiest Routes")

    plt.show()