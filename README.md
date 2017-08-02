# transitland-processing-animation
Animating scheduled transit trips using the Transitland API and Processing.

This repository contains two examples:

`1_LongIslandRailRoad` is a simple example of animating a single transit operator (the Long Island Railroad).
`2_BayArea` is a slightly more complex example of animating every transit operator in a given bounding box, the "greater" Bay Area, in this case, along with a stacked area chart to indicate # of vehicles on the road at a given time.

Each example contains four things:

1. Python notebook used to download, clean and wrangle data from the Transitland API and output your "trip table" as a tidy csv, which will be used to drive the animation
2. Python executable file that does the same exact thing as the notebook, you can use either one.
3. `Data` folder to store the csv output files
4. `Sketch` folder containing the Processing sketch

### Set up Processing:

1. Download [Processing 3](https://processing.org/)
2. Download [Unfolding Maps version 0.9.9 for Processing 3](http://services.informatik.hs-mannheim.de/~nagel/GDV/Unfolding_for_processing_0.9.9beta.zip). You can read more about [Unfolding Maps](http://unfoldingmaps.org/).
3. Navigate to `~/Documents/Processing/libraries` on your machine
4. Drag and drop the unzipped Unfolding Maps folder into `~/Documents/Processing/libraries`


### Python libraries used:
Required: requests, pandas, numpy, datetime, glob, os
Optional (for plotting): matplotlib, plotly

### Instructions:
- 


### To Do's:
- Add Transitland, Mapzen, Carto, OSM attributions into animation

