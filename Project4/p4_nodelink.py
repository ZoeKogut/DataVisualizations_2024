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
#Key:Name = {Color, list of children, collapsed (T/F)}
colorsG = []
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
    if len(tempChildList) > 0: 
        if anode.depth <= 3:
            #colorsG.append('red')
            nameDict[path] = ['red', anode.children, False] #Color, list of children, collapsed (T/F)
        else:
            #colorsG.append('blue')
            anode.collapsed = True
            nameDict[path] = ['blue', anode.children, True] #Color, list of children, collapsed (T/F)
    else:
        #colorsG.append('blue')
        nameDict[path] = ['blue', anode.children, False] #Color, list of children, collapsed (T/F)
    #print(anode.get_attr(attr_name='parent'))
    #print("parent: ", anode.name)
    #print("children: ", anode.children)
    return anode

def update_Tree(self, node, name, colors, path=""):
    currName = node.name
    path = path + "/" + (currName)
    if (path == self.clicked.path): #If the paths match
        if nameDict[path][2]: #If the node is currently collapsed, and was just clicked
            node.collapsed = False
            nameDict[path][2] = False
            nameDict[path][0] = 'red'
            colors.append(nameDict[path][0])
            node.children = copy.deepcopy(nameDict[path][1])
            
            if node.children: #If there are children, call this funtion again to make them
                for c in node.children:
                    #cPath = path + "/" + c.name
                    #if not nameDict[cPath][2]: #If the children aren't collapsed, put them back
                    update_Tree(self, c, name, colors, path)
                    #else: #If they are collapsed, don't redraw them
                    #    colors.append(nameDict[cPath][0])
           
        else: #If the node isn't collapsed, collapse it
            node.collapsed = True
            nameDict[path][2] = True
            nameDict[path][0] = 'blue'
            colors.append(nameDict[path][0])
            if node.children: 
                nameDict[path][1] = node.children
                node.children = []
        
    else: #If it isn't the node clicked, append color and call its children
        colors.append(nameDict[path][0])
        if not nameDict[path][2]: #If node isn't collapsed, call its children
            if node.children: #If there are children, call this funtion again to make them
                for c in node.children:
                    #cPath = path + "/" + c.name
                    #if not nameDict[cPath][2]: #If the children aren't collapsed, put them back
                    update_Tree(self, c, name, colors, path)
                    #else: #If they are collapsed, don't redraw them
                    #    colors.append(nameDict[cPath][0])
            else:
                node.collapsed = True
    return node

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
    
    #Updates the X/Y pos of the children after they are rotated
    def update_children(self, node, path=""):
        path = path + "/" + (node.name)
        if node.children:
            for c in node.children:
                notused = self.update_children(c, path=path)
        tempChildList = copy.deepcopy(node.children)
        if len(tempChildList) > 0: 
            nameDict[path][1] = tempChildList #to Update the x/y values of the children
        else:
            nameDict[path][1] = tempChildList #to Update the x/y values of the children
        return node

    def collapse_Nodes(self, node):
        if node.collapsed: #If collapsed and still has children (this is from depth>3 only)
            colorsG.append('blue')
            if len(node.children) > 0:
                node.children = []
        else:
            if len(node.children) > 0: #If interior node depth <= 3
                colorsG.append('red')
                for c in node.children:
                    self.collapse_Nodes(c)
            else: #If leaf node
                colorsG.append('blue')
        return node

    def draw2(self):
        print("draw")
        self.ax.clear()
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.set_axis_off()
        reingold_tilford(self.root, 
                         sibling_separation=self.separations['sibling'], 
                         subtree_separation=self.separations['subtree'], 
                         level_separation=self.separations['level'])
        # turn vertical layout to horizontal layout
        #This is what we change to change it to a radial layout
        nodes = []
        
        for node in iterators.preorder_iter(self.root):
            node.x, node.y = -node.y, node.x
            #nodes.append((node.x , node.y))
            #Annotation===============================
            if node.collapsed:
                txt = ax.annotate(f'{node.name}: {node.value}', 
                        [node.x, node.y], 
                        color='black', fontsize='x-small', 
                        horizontalalignment='left', verticalalignment='center',
                        xytext=(10, 0), textcoords='offset points',
                        bbox=dict(facecolor='white', alpha=0, edgecolor='white'))
            else:
                txt = ax.annotate(f'{node.name}: {node.value}', 
                        [node.x, node.y], 
                        color='black', fontsize='x-small', 
                        horizontalalignment='right', verticalalignment='center',
                        xytext=(-10, 0), textcoords='offset points',
                        bbox=dict(facecolor='white', alpha=0.9, edgecolor='white'))
            #Annotation===============================
        self.update_children(self.root)
        self.editRoot = self.root.copy()
        self.editRoot = self.collapse_Nodes(self.editRoot)
        for node in iterators.preorder_iter(self.editRoot):
            #node.x, node.y = -node.y, node.x
            nodes.append((node.x , node.y))
        #print(len(nodes))
        #print(nameDict)
        #print("root", self.root)
        #print(self.editRoot)


        plot_tree(self.editRoot, ax=ax, color='black', markersize=1, marker='o')
        ax.scatter(list(zip(*nodes))[0], list(zip(*nodes))[1], s=25, edgecolors='black', c=colorsG, zorder=10)
        self.colors = colorsG
            
        self.canvas.draw()

    def redraw(self):
        self.ax.clear()
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.set_axis_off()
        reingold_tilford(self.root, 
                         sibling_separation=self.separations['sibling'], 
                         subtree_separation=self.separations['subtree'], 
                         level_separation=self.separations['level'])
        # turn vertical layout to horizontal layout
        #This is what we change to change it to a radial layout
        nodes = []
        #print("click ", self.clicked)
        if self.clicked is not None:
            #print(self.clicked)
            
            newTree = self.editRoot.copy() #Make a copy of the tree
            clickedName = self.clicked.name
            self.colors = []
            self.editRoot = update_Tree(self, newTree, clickedName, self.colors)
            #print("clicked node: ",self.editRoot.children)
            #print("children+==========\n", self.clicked.children)

            #print(self.colors)
            #print(self.editRoot)
            for node in iterators.preorder_iter(self.editRoot):
                #node.x, node.y = -node.y, node.x
                #print(node)
                #print(node)
                
                nodes.append((node.x , node.y))
                #Annotation===============================
                if node.collapsed:
                    txt = ax.annotate(f'{node.name}: {node.value}', 
                        [node.x, node.y], 
                        color='black', fontsize='x-small', 
                        horizontalalignment='left', verticalalignment='center',
                        xytext=(10, 0), textcoords='offset points',
                        bbox=dict(facecolor='white', alpha=0, edgecolor='white'))
                else:
                    txt = ax.annotate(f'{node.name}: {node.value}', 
                        [node.x, node.y], 
                        color='black', fontsize='x-small', 
                        horizontalalignment='right', verticalalignment='center',
                        xytext=(-10, 0), textcoords='offset points',
                        bbox=dict(facecolor='white', alpha=0.9, edgecolor='white'))
                #Annotation===============================
            #print("editroot ", self.editRoot)
            #print(len(nodes))

            plot_tree(self.editRoot, ax=ax, color='black', markersize=1, marker='o')
            ax.scatter(list(zip(*nodes))[0], list(zip(*nodes))[1], s=25, edgecolors='black', c=self.colors, zorder=10)
        """else:
            for node in iterators.preorder_iter(self.editRoot):
                #node.x, node.y = -node.y, node.x
                nodes.append((node.x , node.y))
                #Annotation===============================
                if node.collapsed:
                    txt = ax.annotate(f'{node.name}: {node.value}', 
                        [node.x, node.y], 
                        color='black', fontsize='x-small', 
                        horizontalalignment='right', verticalalignment='center',
                        xytext=(5, 0), textcoords='offset points')
                    txt.set_bbox(dict(facecolor='white', alpha=0.9, edgecolor='white'))
                else:
                    txt = ax.annotate(f'{node.name}: {node.value}', 
                        [node.x, node.y], 
                        color='black', fontsize='x-small', 
                        horizontalalignment='right', verticalalignment='center',
                        xytext=(-10, 0), textcoords='offset points')
                    txt.set_bbox(dict(facecolor='white', alpha=0.9, edgecolor='white'))
                #Annotation===============================
                
            plot_tree(self.editRoot, ax=ax, color='black', markersize=10, marker='o')
            #print(self.colors)
            ax.scatter(list(zip(*nodes))[0], list(zip(*nodes))[1], s=75, edgecolors='black', c=self.colors, zorder=10)
        """
        self.canvas.draw()
        #print(root)
        #print("============")
        
        """for node in iterators.preorder_iter(self.editRoot):
            node.x, node.y = node.y, -node.x"""

    def onclick(self, event): 
        #swapped x,y to -y,x to see if it would fix, is still either
            #Clicking once then not again
            #or rotating on click, with points being as consistant as ever
        self.clicked = None
        q = np.array([event.xdata, event.ydata])
        #print("Q: ", q)
        _min = np.inf
        for node in iterators.postorder_iter(self.editRoot):
            #print(node)
            p = np.array([node.x, node.y])
            #print(p)
            d = np.linalg.norm(p-q, ord=np.inf)
            if d < 1:
                self.clicked = node 
                break
        #print("===============")
        if self.clicked is not None:
            self.redraw()

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='CS439: Part 1, Horizontal Node-Link Representation')
    parser.add_argument('-i', '--input', type=str, required=True, help='List the desired Tree in a JSON format')
    #parser.add_argument('-i', '--input', type=str, default='flare.json', help='Filename of tree dataset')
    args = parser.parse_args()


    fig, ax = plt.subplots(1,1, figsize=(8, 6))

    root = read_tree(ax, args.input)

    inter = Interaction(root, root, ax=ax, canvas=fig.canvas) #Editroot is same here, will be different in every other call
            
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_axis_off()
    ax.set_aspect('equal') 
    plt.tight_layout()
    cid = fig.canvas.mpl_connect('button_press_event', inter.onclick)
    plt.show()
