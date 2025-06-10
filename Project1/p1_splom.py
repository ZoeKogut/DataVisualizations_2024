import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse as ap

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='CS439: Part 1, Bargraph')
    parser = ap.ArgumentParser(description='CS439: Simple Scatter Plot Example')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path of Excel workbook')
    parser.add_argument('-a', type=str, action='append' , help='Include an attribute')
    args = parser.parse_args()

    df = pd.read_excel(args.input)
    fig, axs = plt.subplots(len(args.a),len(args.a), figsize= (10,8))

    for x in range(0,len(args.a)):
        #Get/Update Asia Subplot
        df_AsX = df[df['Region'].str.contains("Asia")]
        df_AsX = df_AsX[args.a[x]]
        df_AsY = df[df['Region'].str.contains("Asia")]
        df_AsY = df_AsY[args.a[0]]

        #Get/Update America Subplot
        df_AmX = df[df['Region'].str.contains("America")]
        df_AmX = df_AmX[args.a[x]]
        df_AmY = df[df['Region'].str.contains("America")]
        df_AmY = df_AmY[args.a[0]]

        #Get/Update Europe Subplot
        df_EuX = df[df['Region'].str.contains("Europe")]
        df_EuX = df_EuX[args.a[x]]
        df_EuY = df[df['Region'].str.contains("Europe")]
        df_EuY = df_EuY[args.a[0]]

        #Make the scatterplot
        axs[0,x].scatter(df_AmX, df_AmY, label = "Ameria", color='#618c91', edgecolor='black')
        axs[0,x].scatter(df_AsX, df_AsY, label = "Asia", color='#16373a', edgecolor='black')
        axs[0,x].scatter(df_EuX, df_EuY, label = "Europe", color='#0b995c', edgecolor='black')

        #Include graph lines, set the lines below the data
        axs[0,x].set_axisbelow(True)
        axs[0,x].grid()

        for y in range(1,len(args.a)):
            
            #Get/Update Asia Subplot
            df_AsX = df[df['Region'].str.contains("Asia")]
            df_AsX = df_AsX[args.a[x]]
            df_AsY = df[df['Region'].str.contains("Asia")]
            df_AsY = df_AsY[args.a[y]]

            #Get/Update America Subplot
            df_AmX = df[df['Region'].str.contains("America")]
            df_AmX = df_AmX[args.a[x]]
            df_AmY = df[df['Region'].str.contains("America")]
            df_AmY = df_AmY[args.a[y]]

            #Get/Update Europe Subplot
            df_EuX = df[df['Region'].str.contains("Europe")]
            df_EuX = df_EuX[args.a[x]]
            df_EuY = df[df['Region'].str.contains("Europe")]
            df_EuY = df_EuY[args.a[y]]

            #Make the scatterplot
            axs[y,x].scatter(df_AmX, df_AmY, label = "Ameria", color='#618c91', edgecolor='black')
            axs[y,x].scatter(df_AsX, df_AsY, label = "Asia", color='#16373a', edgecolor='black')
            axs[y,x].scatter(df_EuX, df_EuY, label = "Europe", color='#0b995c', edgecolor='black')
            
            #Include graph lines, set the lines below the data
            axs[y,x].set_axisbelow(True)
            axs[y,x].grid()
    
    #Set the x-axis labels
    for x in range(0,len(args.a)):
        axs[len(args.a)-1, x].set(xlabel=args.a[x])

    #Set the y-axis labels
    for y in range(0,len(args.a)):
        axs[y, 0].set(ylabel=args.a[y])

    # Get rid of all the ticks except for the outside
    for x in axs.flat:
        x.label_outer()
    
    fig.suptitle("Scatteplot Matrix of " + str(len(args.a)) + " EV attributes")
    plt.legend()
    plt.show()
