# Visualizing transit freqency from the command line

Using Mapzen's [Transitland API](transit.land) to download transit schedule data and [Processing](processing.org) with [Unfolding Maps](http://unfoldingmaps.org/) to create spatial-temporal visualizations.

Here is an example animation generated for the Bay Area with a single command:

[![IMAGE ALT TEXT](http://i.imgur.com/SSqpoQB.png)](https://vimeo.com/226987064 "Bay Area Transit Flows")

## Set up Processing:
1. Download [Processing 3](https://processing.org/).
2. Download [Unfolding Maps version 0.9.9 for Processing 3](http://services.informatik.hs-mannheim.de/~nagel/GDV/Unfolding_for_processing_0.9.9beta.zip).
3. Navigate to `~/Documents/Processing/libraries` on your machine.
4. Drag and drop the unzipped Unfolding Maps folder into `~/Documents/Processing/libraries`.
5. Open Processing, navigate to Sketch > Import Library > Add Libary. Search for "Video Export" and click Install.
6. Quit and re-open Processing.

## Instructions:
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

There are two ways to go about using this tool:

### 1) Search by transit operator onestop_id

To animate a particular transit operator, find that operator's `onestop_id` using the [Transitland Feed Registery](https://transit.land/feed-registry/). The `onestop_id` for BART, for example, is `o-9q9-bart`.

Here's the command to visualize BART in San Francisco (onestop_id = `o-9q9-bart`):

- `python transitflow.py --name=bart --operator=o-9q9-bart`

### 2) Search by bounding box

You can also visualize transit flows by searching for all operators within a bounding box (west, south, east, north). I like using [bboxfinder](bboxfinder.com) to draw rectangular bounding boxes. Here's the command to visualize transit flows in Vancouver):

- `python transitflow.py --name=vancouver --bbox=-123.441010,49.007249,-122.632141,49.426160 --clip_to_bbox`

Note, the optional use of `--clip_to_bbox`. This command will clip the dataset to only include transit vehicle trips within the specified bounding box, both in the geo-visualization and in the calculations that drive the stacked bar chart. You may also specify a date with `--date=2017-08-01`, for example. If you do not specify a date, the program will use today's date by default.

### Play your animation

Navigate to `sketches\bay_area\2017-08-15\sketch` and open the `sketch.pde` file.

This should open the Processing application. Simply click Play or `command + r` to play the animation.

### Change map providers

Cycle through the first two rows on the keyboard (1 to 0, q to u) to see the built in map provider options.

Read more about Unfolding Maps map providers here: http://unfoldingmaps.org/tutorials/mapprovider-and-tiles.html

### Exporting to video

Open `sketch.pde` file.

- Faster, lower quality: set `boolean recording = true;`. Generates a medium quality mp4 file.
- Slower, high quality: set `boolean recording = true;` and `boolean HQ = true;`. Generates 3,600 .tiff images. You can use then ffmpeg or Processing's built in movie maker to stitch them together.

### Command line arguments:

**Key**|**Status**|**Description**|**Example**
-----|-----|-----|-----
--name|required|The name of your project|--name=boston
--date|optional|Defaults to today's date|--date=2017-08-15
--operator|optional|Operator onestop_id|--operator=o-drt-mbta
--bbox|optional|West, South, East, North| --bbox=-71.4811,42.1135,-70.6709,42.6157
--clip\_to\_bbox|optional|Clip results to bounding box|--clip\_to\_bbox
--exclude|optional|Operators to be excluded|--exclude=o-9-amtrak
--apikey|optional|Mapzen API key|--apikey=mapzen-abc1234

## Credits:
- Will Geary, Ian Rees for Mapzen, August 2017
- Data: [Mapzen](https://mapzen.com/), [Transitland](https://transit.land/)
- Basemaps: [Carto](http://carto.com/), [Stamen](https://stamen.com/), [OpenStreetMap](http://www.openstreetmap.org/), [ESRI](http://www.esri.com/)
- Visualization: The Processing code in this project builds off [this workshop](https://github.com/juanfrans-courses/DataScienceSocietyWorkshop) by [Juan Francisco Saldarriaga](http://juanfrans.com/). It also relies on the [Unfolding Maps](http://unfoldingmaps.org/) library by [Till Nagel](http://tillnagel.com/) for converting geolocations to screen positions and other functions.

## Sources of inspiration:
- *[Shanghai Metro Flow](http://tillnagel.com/2013/12/shanghai-metro-flow/)*, Till Nagel
- *[Barcelona Cycle Challenge](http://juanfrans.com/projects/barcelonaCycleChallenge.html)*, Juan Francisco Saldarriaga
- *[Seven Days of Car-Sharing in Milan](http://labs.densitydesign.org/carsharing/))*, Matteo Azzi, Daniele Ciminieri, others
- *[NYC Taxis: A Day in the Life](http://chriswhong.github.io/nyctaxi/)*, Chris Whong
- *[Analyzing 1.1 Billion NYC Taxi and Uber Trips](http://toddwschneider.com/posts/analyzing-1-1-billion-nyc-taxi-and-uber-trips-with-a-vengeance/)*, Todd Schneider

And here are a few more visualizations that Will made in the past using similar methods:
- *[Multimodal Symphony: 24 Hours of Transit in New York City](https://vimeo.com/212484620)*, Will Geary
- *[Los Angeles Transit Flows](https://vimeo.com/227178693)*, Will Geary
- *[California Transit Flows](https://vimeo.com/227178693)*, Will Geary
- *[New York City Taxi Flows](https://vimeo.com/210264431)*, Will Geary
- *[New York City Subway Flows](https://vimeo.com/194378581)*, Will Geary
