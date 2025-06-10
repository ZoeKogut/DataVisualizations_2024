import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse as ap
import geopandas
import json


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

    fig, ax = plt.subplots()
    map.plot(ax=ax, color='white', edgecolor='black', zorder=0)
    ax.scatter(airports["Longitude"], airports["Latitude"], s=5, marker='o', color='red', edgecolors='black', zorder=10)

    flight_sorted = flights.sort_values("number_of_flights")
    flight_sorted = flight_sorted.tail(200)
    flight_sorted = flight_sorted.reset_index(drop=True)

    #Making a dictionary of the airport and its lat/long
    ap_names = {}
    for i in range(len(airports)):
        ap_names[airports.at[i, 'IATA']] = (airports.at[i, 'Longitude'], airports.at[i, 'Latitude'])

    #Taking the heaviest 200 flights and plotting them using the dict
    for i in range(0, len(flight_sorted)): #Range of the flights 200 heaviest flights
        ap1x, ap1y = ap_names[flight_sorted.at[i, 'origin']] #Coords for the start airport
        ap2x, ap2y = ap_names[flight_sorted.at[i, 'destination']] #cords for the end airport
        ax.plot([ap1x, ap2x], [ap1y, ap2y], 'b-', alpha=.6, mfc='C1', mec='C1', zorder=5) #mfc, marker face color; mec, marker edge color
                                                                                          #zorder, the order of items being drawn on a graph
    
    ax.set_title("World Airports and the 200 Busiest Routes")

    plt.show()