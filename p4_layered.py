import numpy as np 
from matplotlib import pyplot as plt 
import matplotlib as mpl
import argparse as ap
import json 
from bigtree import Node, reingold_tilford, plot_tree, find_path
from bigtree.utils import iterators
import math
import copy

#======Global Vars======
nameDict = {} #Dict to keep track of if a node is collapsed, its children, and its color
annotDict = {} #Keeps track of annotations and their rotations
#Key:Name = {Color, list of children, collapsed (T/F)}
colorsG = []
radial = False
#=======================


#Check to see how many / are in the return from parent, if two- stop at this level
#actually make a diffferent function for this. This "root" will be the entire tree, anything else is just 
#a copy of the origional "root"
def import_tree_from_dict(ax, nodeinfo, parent=None, path="", depth=0):
    #print("=============================================")
    anode = Node(name=nodeinfo['name'], value=0, 
                parent=parent, children=[])
    tempChildList = []
    path = path + "/" + (nodeinfo['name'])
    if 'value' in nodeinfo.keys(): #Adds the node's value and sets collapsed to false
        anode.value = nodeinfo['value']
        anode.set_attrs({'collapsed': False})
        anode.set_attrs({'path': path})
        anode.set_attrs({'depth': depth})
    
    if 'children' in nodeinfo.keys(): #If there are children, call this funtion again to make them
        #print("Parent", anode.name)
        for c in nodeinfo['children']:
            #print("", c)
            #print(path)
            notused = import_tree_from_dict(ax, c, parent=anode, path=path, depth=(depth+1))
            #tempChildList.append(notused)
        tempChildList = anode.children
    else:
        anode.collapsed = True
    return anode

def read_tree(ax, filename): #Reads .json file and then calls the function to make the tree
    with open(filename, 'r') as fp:
        data = json.load(fp)
        return import_tree_from_dict(ax, data)

class Interaction:
    def __init__(self, root, editRoot, ax, canvas, separations={'subtree': .5, 'level': 50, 'sibling': .1}):
        self.root = root 
        self.editRoot = editRoot
        self.colors = ['red']
        self.ax = ax
        self.canvas = canvas
        self.separations = separations
        self.clicked = None
        self.draw2()
    
    def draw2(self):
        print("draw")
        self.ax.clear()
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.set_axis_off()
        plt.tight_layout()
        # turn vertical layout to horizontal layout
        #This is what we change to change it to a radial layout
        nodes = []
        colorArray = ['#fea0a0', '#fecba0', '#feeca0', '#c0fea0', '#a0fed6', '#a0e3fe', '#a0a5fe',
                      '#c6a0fe', '#eea0fe', '#fea0dd']
        if radial:
            self.calcLayeredRadial(ax, self.root, 0, 360, 2/20, 'grey', self.root.value, colorArray=colorArray)
        else:
            self.calcLayered(self.ax, self.root,0,0, 'grey', self.root.value, colorArray=colorArray)
        #self.colors = colorsG
            
        self.canvas.draw()

    def calcLayered(self, ax, node, startingPointX, startingPointY, color, mainval, colorArray=None):
        bL = [startingPointX, startingPointY]
        #print(colorArray)
        rec = plt.Rectangle(bL, 1/5, (node.value/mainval), color=color, ec='white')
        ax.add_patch(rec)

        if (node.value/mainval) > .015:
            txt = ax.annotate(f'{node.name}: {node.value}', 
                            [startingPointX, startingPointY], 
                            color='black', fontsize='x-small', 
                            horizontalalignment='left', verticalalignment='bottom',
                            xytext=(2, 0), textcoords='offset points',
                            annotation_clip=False)
        #sort children based on value?
        #call them in ascending order of value
        if node.children:
            sortedChildren  = sorted(node.children, key= lambda x: x.value)
            startingPointX = startingPointX+(1/5)
            if node.depth == 1:
                for c, col in zip(sortedChildren, colorArray):
                    ax = self.calcLayered(ax, c, startingPointX, startingPointY, col, mainval)
                    startingPointY = startingPointY + (c.value/mainval)
            else:
                for c in sortedChildren:
                    ax = self.calcLayered(ax, c, startingPointX, startingPointY, color, mainval)
                    startingPointY = startingPointY + (c.value/mainval)
        
        return ax
    
    def calcLayeredRadial(self, ax, node, theta1, theta2, radius, color, mainval, width=0, colorArray=None):
        #percent = node.value/mainval
        #print(colorArray)
        if node.depth == 1:
            rec = mpl.patches.Wedge((.5,.5), radius, theta1, theta2, 
                                    color='grey', fc='grey', ec='white',
                                    linewidth=.3, clip_on=False)
            txt = ax.annotate(f'{node.name}', 
                            [0.5, 0.5], 
                            color='black', fontsize=5, 
                            horizontalalignment='center', verticalalignment='center',
                            xytext=(2, 0), textcoords='offset points',
                            annotation_clip=False)
        else:
            rec = mpl.patches.Wedge((.5,.5), radius, theta1, theta2, 
                                    width=width, color=color, ec='white', 
                                    linewidth=.3, clip_on=False)
            if theta2 - theta1 > 3:
                diff = (theta2 + theta1)/2
                if 270 >= diff >= 90:
                    txt = ax.annotate(f'{node.name}', 
                            [.5+ (radius-.08)*math.cos((diff*(math.pi/180))), .5+(radius-.08)*math.sin((diff*(math.pi/180)))], 
                            color='black', fontsize=5, 
                            horizontalalignment='center', verticalalignment='center',
                            xytext=(0, 0), textcoords='offset points', rotation = 180+diff,
                            annotation_clip=False)
                else:
                    txt = ax.annotate(f'{node.name}', 
                            [.5+ (radius-.08)*math.cos((diff*(math.pi/180))), .5+(radius-.08)*math.sin((diff*(math.pi/180)))], 
                            color='black', fontsize=5, 
                            horizontalalignment='center', verticalalignment='center',
                            xytext=(0, 0), textcoords='offset points', rotation = diff,
                            annotation_clip=False)
        ax.add_patch(rec)

        if node.children:
            sortedChildren  = sorted(node.children, key= lambda x: x.value)
            width = width+.05
            diff = (theta2 - theta1)
            if node.depth == 1:
                for c, col in zip(sortedChildren, colorArray):
                    theta2 = theta1 + ((c.value/node.value) * diff)
                    ax = self.calcLayeredRadial(ax, c, theta1, theta2, 9/40, col, mainval, .15)
                    theta1 = theta2
            else:
                for c in sortedChildren:
                    if c.depth <= 5:
                        theta2 = theta1 + ((c.value/node.value) * diff)
                        ax = self.calcLayeredRadial(ax, c, theta1, theta2, (radius + 3/20), color, mainval, .15)
                        theta1 = theta2
        
        return ax

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='CS439: Part 1, Horizontal Node-Link Representation')
    parser.add_argument('-i', '--input', type=str, required=True, help='List the desired Tree in a JSON format')
    #parser.add_argument('-i', '--input', type=str, default='flare.json', help='Filename of tree dataset')
    parser.add_argument('--radial', action="store_true", required=False, help='Include to make the graph a Radial layout')
    args = parser.parse_args()

    radial = args.radial

    fig, ax = plt.subplots(1,1, figsize=(8, 6))

    root = read_tree(ax, args.input)

    inter = Interaction(root, root, ax=ax, canvas=fig.canvas) #Editroot is same here, will be different in every other call
            
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_axis_off()
    ax.set_aspect('equal') 
    plt.tight_layout()
    #cid = fig.canvas.mpl_connect('button_press_event', inter.onclick)
    plt.show()