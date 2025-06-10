import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse as ap

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='CS439: Part 1, Bargraph')
    parser = ap.ArgumentParser(description='CS439: Simple Scatter Plot Example')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path of Excel workbook')
    parser.add_argument('-x', type=str, default='Weight', help='Column to map to x axis')
    parser.add_argument('-y', type=str, default='Range', help='Column to map to y axis')
    parser.add_argument('-c', '--color', type=str, default='Top Speed', help='Column to map to color')
    parser.add_argument('-s', '--size', type=str, default='Price', help='Point size')
    args = parser.parse_args()

    df = pd.read_excel(args.input)

    minR = 10
    maxR = 500
    minV = df[args.size].min()
    maxV = df[args.size].max()

#Normalize the size so it isnt too large
    norm_size = minR + ((df[args.size] - minV)/(maxV - minV)) * (maxR - minR)

#Making the Grpah
    plt.figure(figsize=(8,6))
    plt.scatter(df[args.x], df[args.y], s=norm_size, c=df[args.color], cmap='plasma', alpha=0.6)
    plt.xlabel(args.x)
    plt.ylabel(args.y)
    cbar = plt.colorbar()
    cbar.set_label(args.color)
    plt.title("Bubble chart representation of " + args.x + ", " + args.y + ", " + args.color + ", " + args.size)

    plt.show()
