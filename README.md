# Transitland Processing Animation (work in progress)
Animating scheduled transit trips using the [Transitland API](https://transit.land/) from Mapzen and the [Processing](https://processing.org/) language with the [Unfolding Maps](http://unfoldingmaps.org/) library.

Here is an example animation generated for the Bay Area:

[![IMAGE ALT TEXT](http://i.imgur.com/SSqpoQB.png)](https://vimeo.com/226987064 "Bay Area Transit Flows")

### Set up Processing:
1. Download [Processing 3](https://processing.org/).
2. Download [Unfolding Maps version 0.9.9 for Processing 3](http://services.informatik.hs-mannheim.de/~nagel/GDV/Unfolding_for_processing_0.9.9beta.zip).
3. Navigate to `~/Documents/Processing/libraries` on your machine.
4. Drag and drop the unzipped Unfolding Maps folder into `~/Documents/Processing/libraries`.
5. Open Processing, navigate to Sketch > Import Library > Add Libary. Search for "Video Export" and click Install.
6. Quit and re-open Processing.

### Instructions:
- Download the repository, unzip it and `cd` into it.

To run within a virtual environment (optional, recommended):
- `virtualenv virtualenv`
- `source virtualenv/bin/activate`
- `python virtualenv/bin/pip install -r requirements.txt`

Without a virtual environment:
- `pip install -r requirements.txt`

Navigate to the main directory:
- `cd transitflow`

Now, you are ready to download transit schedule data and generate visualizations.

You can visualize transit flows for a particular operator or set of operators by searching by operator onestop_id. Here's the command to visualize BART in San Francisco (onestop_id = `o-9q9-bart`):

- `python transitflow.py --name=bart --operator=o-9q9-bart`

You can also visualize transit flows by searching for all operators within a bounding box (west, south, east, north). I like using bboxfinder.com to draw rectangular bounding boxes. Here's the command to visualize transit flows in Vancouver):
- `python transitflow.py --name=vancouver --bbox=-123.441010,49.007249,-122.632141,49.426160 --clip_to_bbox`

Note, the optional use of `--clip_to_bbox`. This command will clip the dataset to only include transit vehicle trips within the specified bounding box, both in the geo-visualization and in the calculations that drive the stacked bar chart. You may also specify a date with `--date=2017-08-01`, for example. If you do not specify a date, the program will use today's date by default.

### Credits:
- Will Geary, Ian Rees for Mapzen, August 2017
- Data: [Mapzen](https://mapzen.com/), [Transitland](https://transit.land/)
- Basemaps: Carto, Stamen, OpenStreetMap, ESRI
- Visualization: The Processing code in this project builds off [this workshop](https://github.com/juanfrans-courses/DataScienceSocietyWorkshop) by [Juan Francisco Saldarriaga](http://juanfrans.com/), a researcher at the Center for Spatial Research at Columbia University and an adjunct assistant professor of urban planning and architecture. It also relies on the [Unfolding Maps](http://unfoldingmaps.org/) library for converting geolocations to screen positions. Unfolding Maps was created and is primarily maintained by [Till Nagel](http://tillnagel.com/), a professor of visual analytics at University of Applied Sciences Mannheim.

### Sources of inspiration:
- *[Shanghai Metro Flow](http://tillnagel.com/2013/12/shanghai-metro-flow/)*, Till Nagel
- *[Barcelona Cycle Challenge](http://juanfrans.com/projects/barcelonaCycleChallenge.html)*, Juan Francisco Saldarriaga
- *[Seven Days of Car-Sharing in Milan](http://labs.densitydesign.org/carsharing/))*, Matteo Azzi, Daniele Ciminieri, others
- *[NYC Taxis: A Day in the Life](http://chriswhong.github.io/nyctaxi/)*, Chris Whong
- *[Analyzing 1.1 Billion NYC Taxi and Uber Trips](http://toddwschneider.com/posts/analyzing-1-1-billion-nyc-taxi-and-uber-trips-with-a-vengeance/)*, Todd Schneider

And here are a few more visualizations Will made in the past using similar methods:
- *[Multimodal Symphony: 24 Hours of Transit in New York City](https://vimeo.com/212484620)*, Will Geary
- *[Los Angeles Transit Flows](https://vimeo.com/227178693)*, Will Geary
- *[California Transit Flows](https://vimeo.com/227178693)*, Will Geary
- *[New York City Taxi Flows](https://vimeo.com/210264431)*, Will Geary
- *[New York City Subway Flows](https://vimeo.com/194378581)*, Will Geary
