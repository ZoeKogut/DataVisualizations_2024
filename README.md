# DataVisualizations_2024
Repository of classwork for CS439  
<ins>**Any data (except for the final project) was compiled and cleaned by Xavier Tricoche**</ins>

## Project 1
This was the beginning project and my first step into making and designing graphs. 
The folders in there work with simple bubble and bar charts, along with a splom graph

### p1_bars
API: python p1_bars.py -i evs_assignment1.xlsx

### p1_bubbles
API: python p1_bubbles.py -i evs_assignment1.xlsx  
There are a handful of attributes that can change the size, x/y-axis, and color of the graph.  
The possible attributes are: Model, Year, Weight, Top Speed, Range, Acceleration, Efficiency, Price, Country

### p1_splom
API: python p1_splom.py -i evs_assignment1.xlsx -a attribute  
ie. To run the program comparing both weight and range together, you would run:  
    <ins>python p1_splom.py -i evs_assignment1.xlsx -a Weight -a Range</ins>  
Attributes will be listed if you add the **-h** or **--help** tag before **-i**  


## Project 2
A scatterplot graph that shows the correlation between the four chosen attributes.  
The IPA should be the same for all four  
IPA: python FILE -i CIA_world_factbook_2023.xlsx  


### p2_bubbles
The start of this projecct, it is just a static scatterplot comparing 4 attributes.


### p2_widgets
First upgrade to the graph, allowing you to change the attributes being compared.

### p2_brushing
Another graph is added, allowing you to "brush" or highlight specific sections to compare nodes between both graphs.

### p2_tooltip
Now, hovering over nodes gives a tooltip that points to the same node between both graphs. 


## Project 3
A map of the globe with all of the given airports plotted on it. Lines between each airports represent flights  
IPA: python FILE -m custom.geo.json -a worldwide_airports.xlsx -f flight.json  

### p3_geospatial
Basic map plotting all the airports and the given flights.  
<img src="https://github.com/user-attachments/assets/1b7eb331-e6b1-4361-8096-d14d789973f2" width="600">

### p3_attributes
The airports are now sized and colored based on how often they are visited and how many airlines visit them, respectivly.  
<img src="https://github.com/user-attachments/assets/af283d3a-7d9d-433c-810e-a4b32aa0f323" width="600">

### p3_tooltip
Hovering over the airport gives you details on that airport.
<img src="https://github.com/user-attachments/assets/de34d35d-ffb4-418d-9a75-a8bea09978aa" width="600">

### p3_filtering
There are sliders at the bottom that you can use to filter out nodes and lines of specific size  
_This might be a little laggy, as instead of only the top 200 flights, it shows all of them at first._
<img src="https://github.com/user-attachments/assets/64bb75e9-f124-405a-8f49-85c2868cb090" width="600">


### p3_geodesic
The lines now take their intended path across the globe, and you can also filter based on the airline you want.  
_Note: I was given the skeleton code of how to make these lines curved, then worked from there._  
<img src="https://github.com/user-attachments/assets/f6e943c1-2362-455a-a27e-8e496baf71c8" width="600">


## Project 4
This project has its own Readme detailing some of the issues I came accross while doing the project.

Project 4 deals with desplaying data through different datastructures such as trees (regular and radial) and tree maps.  
API: python FILE -i flare.json

### p4_NodeLink
- Red means that the node is expanded and has children (Internal node)
- Blue means the node has no children, or is a collapsed node (Leaf)
<img src="https://github.com/user-attachments/assets/cd676673-aaf7-4205-95b0-ba604b39f234" width="600">


### p4_radial_layout
Basic radial tree graph.  
<img src="https://github.com/user-attachments/assets/6ba01a56-a033-40e2-9f80-8bc920d1f010" width="600">


### p4_layered
Layered tree map.  
<img src="https://github.com/user-attachments/assets/77de7df5-7f79-48ce-bcf5-dfcd41b9f222" width="600">


### p4_enclosure
Recursive tree map.  
As noted in the Project4 README, the lables for this are fairly ugly.  
<img src="https://github.com/user-attachments/assets/8dc8d9e1-359f-4b1a-8e1d-e12418c53f86" width="600">


