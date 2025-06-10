import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse as ap

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='CS439: Part 1, Bargraph')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path of Excel workbook')
    args = parser.parse_args()

    df = pd.read_excel(args.input)
    df2 = df
    array_asia = [] #Array to store the number of each car in each 40-spaced effecicency
    array_america = []
    array_europe = []
    array_x = np.array([100,140,180,220,260]) #Make the 40-spaced groups for the graph

# First graph is the normal data, the second is the same data but all the numbers are divided by the total number of cars produced in that area.
    for x in range(100,280,40):
        df2 = df[(df['Efficiency'] >= x) & (df['Efficiency'] < x+40) & (df['Region'].str.contains("Asia"))]
        array_asia.append(len(df2))
        df2 = df[(df['Efficiency'] >= x) & (df['Efficiency'] < x+40) & (df['Region'].str.contains("America"))]
        array_america.append(len(df2))
        df2 = df[(df['Efficiency'] >= x) & (df['Efficiency'] < x+40) & (df['Region'].str.contains("Europe"))]
        array_europe.append(len(df2))

    len = 10 #Just to make it easier when I was assigning things over and over lol
    plt.figure(figsize=(8,8))
    
#=================First Bargraph===========================
    plt.subplot(121) #I found these numbers online, not sure what they do. I think the second number is # of charts in the graph, th 3rd number is which chart it is?
                     #perchance, unsure. need to consult the oracle
    plt.bar(array_x+(len), array_america, len, label = "America", color='#618c91')
    plt.bar(array_x+(len*2), array_asia, len, label = "Asia", color='#16373a')
    plt.bar(array_x+(len*3), array_europe, len, label = "Europe", color='#0b995c')
    plt.xticks([100,140,180,220,260], array_x)

    plt.ylabel("Number of EV Models")
    plt.xlabel("Effiency in Wh/km")

#=================Second Bargraph===========================
    plt.subplot(122)
    plt.bar(array_x+(len), array_america/np.sum(array_america), len, label = "America", color='#618c91')
    plt.bar(array_x+(len*2), array_asia/np.sum(array_asia), len, label = "Asia", color='#16373a')
    plt.bar(array_x+(len*3), array_europe/np.sum(array_europe), len, label = "Europe", color='#0b995c')
    plt.xticks([100,140,180,220,260], array_x)

    plt.legend()
    plt.ylabel("Proportion of EV Models")
    plt.xlabel("Effiency in Wh/km")
    plt.suptitle("Effeciency of EVs produced between 2010 and 2024")

    plt.show()
