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
- `git clone https://github.com/transitland/transitland-processing-animation.git`

To run with virtualenv (optional, recommended):
- `virtualenv virtualenv`
- `source virtualenv/bin/activate`

Install python requirements:
- `python virtualenv/bin/pip install -r requirements.txt`

Navigate to folder:
- `cd transitflow`

Now, you are ready to download transit schedule data and generate visualizations.

To visualize transit flows by operator onestop_id (BART):
- `python transitflow.py --date=2017-08-15 --name=bart --operator=o-9q9-bart`

To visualize transit flows by bounding box (Vancouver):
- `python transitflow.py --date=2017-08-15 --name=vancouver --bbox=-123.441010,49.007249,-122.632141,49.426160 --clip_to_bbox`

### Credits:
- Will Geary for Mapzen, August 2017
- Data: [Mapzen](https://mapzen.com/), [Transitland](https://transit.land/)
- Basemaps: Carto, Stamen, OpenStreetMap, ESRI
- Visualization: The Processing code in this project builds off [this workshop](https://github.com/juanfrans-courses/DataScienceSocietyWorkshop) by [Juan Francisco Saldarriaga](http://juanfrans.com/), a researcher at the Center for Spatial Research at Columbia University and an adjunct assistant professor of urban planning and architecture. It also relies on the [Unfolding Maps](http://unfoldingmaps.org/) library for converting geolocations to screen positions. Unfolding Maps was created and is primarily maintained by [Till Nagel](http://tillnagel.com/), a professor of visual analytics at University of Applied Sciences Mannheim.

### Sources of inspiration:
- *[Shanghai Metro Flow](http://tillnagel.com/2013/12/shanghai-metro-flow/)*, Till Nagel
- *[Barcelona Cycle Challenge](http://juanfrans.com/projects/barcelonaCycleChallenge.html)*, Juan Francisco Saldarriaga
- *[Seven Days of Carsharing in Milan](http://labs.densitydesign.org/carsharing/))*, Matteo Azzi, Daniele Ciminieri, others
- *[NYC Taxis: A Day in the Life](http://chriswhong.github.io/nyctaxi/)*, Chris Whong
- *[Analyzing 1.1 Billion NYC Taxi and Uber Trips](http://toddwschneider.com/posts/analyzing-1-1-billion-nyc-taxi-and-uber-trips-with-a-vengeance/)*, Todd Schneider

And here are a few more visualizations I've made in the past using similar methods:
- *[Multimodal Symphony: 24 Hours of Transit in New York City](https://vimeo.com/212484620)*, Will Geary
- *[Los Angeles Transit Flows](https://vimeo.com/227178693)*, Will Geary
- *[California Transit Flows](https://vimeo.com/227178693)*, Will Geary
- *[New York City Taxi Flows](https://vimeo.com/210264431)*, Will Geary
- *[New York City Subway Flows](https://vimeo.com/194378581)*, Will Geary
