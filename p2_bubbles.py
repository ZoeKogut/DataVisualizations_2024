import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import argparse as ap
import math
from scipy.interpolate import make_interp_spline
from matplotlib import cm, colors

## Start of legend.py code ========================================
    ## ==== I did the comments tho =====
def n_orders(_min, _max):
    mino = int(math.log10(_min))
    maxo = int(math.log10(_max))
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

def make_size_legend(values, sizes, nstops, shape='o', title='None', log_scale=True, spacing=0.5):
    value_stops, size_stops = legend_helper(values, sizes, nstops, log_scale=log_scale)
    size_text = make_size_text(value_stops)
    size_values = size_stops
    print(f'sizes are {size_values}')
    custom_circles = [ plt.Line2D(range(1), range(1), markersize=math.sqrt(s),
                                  color='white', marker=shape,
                                  markerfacecolor='white',
                                  markeredgecolor='black')
                       for s in size_values ]

    size_legend = plt.legend(custom_circles,
                         [ f"{s}" for s in size_text ],
                         title=title, title_fontproperties={'weight': 'bold'},loc='upper right',
                         bbox_to_anchor=(1, 1),
                         labelspacing=spacing)
    return size_legend
## End of legend.py code ========================================

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='CS439: Part 2, Bubble Chart')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path of Excel workbook')
    args = parser.parse_args()

    df = pd.read_excel(args.input)

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