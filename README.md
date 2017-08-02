# Transitland Processing Animation
Animating scheduled transit trips using the [Transitland API](https://transit.land/) from Mapzen and the [Processing](https://processing.org/) language with the [Unfolding Maps](http://unfoldingmaps.org/) library.

This repository contains two examples:

`1_LongIslandRailRoad` is a simple example of animating a single transit operator (the Long Island Rail Road).
`2_BayArea` is a slightly more complex example of animating every transit operator in a given bounding box, the "greater" Bay Area, in this case, along with a stacked area chart to indicate # of vehicles on the road at a given time.

Each example contains four things:

1. Python notebook used to download, clean and wrangle data from the Transitland API and output your "trip table" as a tidy csv, which will be used to drive the animation
2. Python executable file that does the same exact thing as the notebook, you can use either one.
3. `Data` folder to store the csv output files
4. `Sketch` folder containing the Processing sketch

### Set up Processing:
1. Download [Processing 3](https://processing.org/)
2. Download [Unfolding Maps version 0.9.9 for Processing 3](http://services.informatik.hs-mannheim.de/~nagel/GDV/Unfolding_for_processing_0.9.9beta.zip).
3. Navigate to `~/Documents/Processing/libraries` on your machine
4. Drag and drop the unzipped Unfolding Maps folder into `~/Documents/Processing/libraries`

### Python libraries used:
- Required: requests, pandas, numpy, datetime, glob, os
- Optional (for plotting): matplotlib, plotly

### Instructions:
- If you only want to run the Processing sketches you can simply open `01_LIRR/sketch/sketch.pde` or `02_BayArea/sketch/sketch.pde` and hit play. Be sure to unzip the `02_BayArea/data/csv` file first.

- If you want to use the python scripts to download data from transitland for either example, `cd` to either example folder and enter `python LIRR.py` or `python bay_area.py` into your terminal. This will download the csv. Once the csv has downloaded, open the appropriate `sketch.pde` file and hit play. Note: LIRR script should be very fast. The Bay Area script takes 1.5 hours for me.

Hopefully the examples are easy enough to follow that either can be repurposed for new cities without too much effort.

### Room for future improvments...
- The Processing sketch currently uses simple linear interpolation to animate a point from stop A to stop B given the departure and arrival times. It does not show vehicles following their actual, real-life routes. The sketch would be more meaningful if vehicles actually followed their routes. This seems entirely possible to do for operators that provide route shapes... just haven't gotten there yet!

- Known isses: Python script is runnning into API timeouts and failing to process the biggest transit operators, including NYC MTA and Chicago Transit Authority. 

### Credits:
- Data: [Mapzen](https://mapzen.com/), [Transitland](https://transit.land/)
- Basemap: Carto, OpenStreetMap
- Processing Code: 

The processing code builds off of code from [this workshop](https://github.com/juanfrans-courses/DataScienceSocietyWorkshop) by [Juan Francisco Saldarriaga](http://juanfrans.com/), a researcher at the Center for Spatial Research at Columbia University and an adjunct assistant professor of urban planning and architecture at the Graduate School of Architecture, Planning and Preservation (GSAPP). It also relies heavily on the fantastic [Unfolding Maps](http://unfoldingmaps.org/) library and its many useful examples. Unfolding Maps was created and is primarily maintained by [Till Nagel](http://tillnagel.com/), a professor of visual analytics at University of Applied Sciences Mannheim and previously a postdoc at the FHP Urban Complexity Lab.

### Inspirations:
- *[NYC Taxis: A Day in the Life](http://chriswhong.github.io/nyctaxi/)*, Chris Whong
- *[Shanghai Metro Flow](http://tillnagel.com/2013/12/shanghai-metro-flow/)*, Till Nagel
- *[Barcelona Cycle Challenge](http://juanfrans.com/projects/barcelonaCycleChallenge.html)*, Juan Francisco Saldarriaga
- *[Global Sea Ice Area Spiral](https://github.com/kjpluck/GlobalSeaIceAreaSpiral)*, Kevin Pluck


### To Do's:
- Add Transitland, Mapzen, Carto, OSM attributions into animation

