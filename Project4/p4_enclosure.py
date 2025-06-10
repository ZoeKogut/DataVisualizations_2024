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
labels = False
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
        return import_tree_from_dict(ax, data, depth=0)

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
        #self.ax.set_xlim(0, 956129)
        #self.ax.set_ylim(0, 956129)
        plt.tight_layout()
        # turn vertical layout to horizontal layout
        #This is what we change to change it to a radial layout
        nodes = []
        colorArray = ['#fea0a0', '#fecba0', '#feeca0', '#c0fea0', '#a0fed6', '#a0e3fe', '#a0a5fe',
                      '#c6a0fe', '#eea0fe', '#fea0dd']
        
        self.calcLayered(self.ax, self.root,(0,0), 'grey', self.root.value, self.root.value, 1, colorArray=colorArray)
        #self.colors = colorsG
            
        self.canvas.draw()

    def calcLayered(self, ax, node, startingPoint, color, mainval, rootVal, rotation, colorArray=None):
        bL = startingPoint
        #print(colorArray)
        """if node.depth == 5:
            rec = plt.Rectangle(bL, (node.value), (node.value), color='grey', ec='white', lw=6-(node.depth))
        else:"""
        rec = plt.Rectangle(bL, (node.value), (node.value), color=color, ec='white', lw=3/(node.depth))
        ax.add_patch(rec)
        
        #print(ax.transData.transform((bL[0], node.value)))
        #print("=================")
        if labels:
            if not node.children or node.depth == maxDepth+1:
                print(startingPoint)
                if (not startingPoint[0]>.57 or not startingPoint[1]>.73) and (not startingPoint[0]>.75 or not .33>startingPoint[1]>.17):
                    txt = ax.annotate(f'{node.name}:\n {node.value}', 
                                    [startingPoint[0], startingPoint[1]], 
                                    color='black', fontsize=4, 
                                    horizontalalignment='left', verticalalignment='bottom',
                                    xytext=(2, 2), textcoords='offset points')
        #sort children based on value?
        #call them in ascending order of value
        if node.children:
            sortedChildren  = sorted(node.children, key= lambda x: x.value)
            #startingPointX = startingPointX+(1/5)
            if node.depth <= maxDepth:
                #print(node.depth)
                if node.depth == 1:
                    for c, col in zip(sortedChildren, colorArray):
                        ax = self.calcLayered(ax, c, startingPoint, col, node.value, rootVal,0)
                        startingPoint = (0,(startingPoint[1] + (c.value/node.value)))
                elif node.depth == 2:
                    incriment = (mainval/rootVal)/len(sortedChildren)
                    x = startingPoint[0]
                    for c in sortedChildren:
                        ax = self.calcLayered(ax, c, startingPoint, color, node.value, rootVal, 1)
                        x = x + (c.value/node.value)
                        startingPoint = (x,startingPoint[1])
                elif node.depth ==3:    
                    space = (mainval/rootVal) #Subsection of graph to work with
                    for c in sortedChildren:
                        ax = self.calcLayered(ax, c, startingPoint, color, node.value, rootVal, mainval)
                        startingPoint = (startingPoint[0],(startingPoint[1] + ((c.value/node.value)*space)))
                            
                else: #Vertical
                    space = (mainval/rotation) #Subsection of graph to work with
                    #print(node.depth)
                    for c in sortedChildren:
                        print(c.name)
                            #print(startingPoint)
                        ax = self.calcLayered(ax, c, startingPoint, color, node.value, rootVal, 1)
                        print(startingPoint)
                        startingPoint = (startingPoint[0] + ((c.value/node.value)*space),startingPoint[1])
                        
        
        return ax

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='CS439: Part 1, Horizontal Node-Link Representation')
    parser.add_argument('-i', '--input', type=str, required=True, help='List the desired Tree in a JSON format')
    #parser.add_argument('-i', '--input', type=str, default='flare.json', help='Filename of tree dataset')
    parser.add_argument('--maxdepth', type=int, default=3, required=False, help='Max depth that nodes decend to [default 3]')
    parser.add_argument('--tags', action="store_true", required=False, help='Adds labels (they do not look good)')
    args = parser.parse_args()

    maxDepth = args.maxdepth
    print(maxDepth)
    labels = args.tags
    print(labels)

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
