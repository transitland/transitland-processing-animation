# Visualizing Transit Frequency

Urban planner Jarrett Walker emphasizes the importance of **transit frequency**:

> Transit frequency is the elapsed time between consecutive buses (or trains, or ferries) on a line, which determines the maximum waiting time.  People who are used to getting around by a private vehicle (car or bike) often underestimate the importance of frequency, because there isn’t an equivalent to it in their experience.  A private vehicle is ready to go when you are, but transit is not going until it comes.  High frequency means transit is coming soon, which means that it approximates the feeling of liberty you have with your private vehicle – that you can go anytime.  Frequency is freedom! http://humantransit.org/2015/07/mega-explainer-the-ridership-recipe.html

This makes intuitive sense. Transit networks with higher trip frequencies and shorter waiting times will yield a better, more empowering experience for passengers than those with lower frequencies and longer waiting times.

Analyzing transit frequency in an intuitive way, however, can be difficult. Traditional, static transit maps provide geographic context but do not give any information about trip frequency. Daily or weekly timetables provide information about trip frequency but can be overwhelming, unintuitive and lacking geographic context. Perhaps we can use spatial-temporal visualization to combine the spatial information of a static transit map with the temporal information of a timetable, and make it easer to talk and think about transit frequency!

This is the motivation behind *TransitFlow*, an experimental set of tools that can be used to generate spatial-temporal transit network datasets and visualizations from the command line.

![IMAGE ALT TEXT](http://i.imgur.com/cMDfgkQ.png)

*Mmmm... timetables. Provided by the San Francisco Municipal Transportation Agency.*

*TransitFlow* consists of two parts:
  1) A few python scripts to retrieve and wrangle transit schedule data from the [Transitland API](https://transit.land/), an open-source project sponsored by [Mapzen](mapzen.com)

  2) A template to generate a [Processing](processing.org) script to animate that data.

Let's look at a few examples of what you can do with *TransitFlow*.

# Examples

## San Francisco BART
You can visualize a single transit operator by passing in the operator's onestop_id. You can look up an operator's onestop_id using the [Transitland Feed Registery](https://transit.land/feed-registry/). For example, the onestop_id for San Francisco BART is `o-9q9-bart`.

Visualize one day of BART transit flows:

- `python transitflow.py --name=bart --operator=o-9q9-bart`

[![IMAGE ALT TEXT](http://i.imgur.com/cssT1Vq.png)](https://vimeo.com/230364702 "One Day of BART Trips")

## Chicago Metra

Here's another example of visualizing a single operator, this time the Chicago Metra (onestop_id: `o-dp3-metra`).

- `python transitflow.py --name=chicago_metra --operator=o-dp3-metra`

[![IMAGE ALT TEXT](http://i.imgur.com/Vzt1aaj.jpg)](https://vimeo.com/230506003 "Chicago Metra")

It's interesting to note how much more bimodal the distribution of vehicles en route is for the Chicago Metra than BART.

## Bay Area Transit Flows
You can also visualize all operators within a bounding box. I like using bboxfinder.com to draw a bbox.

Visualize all transit flows in the (greater) San Francisco Bay Area with:

- `python transitflow.py --name=bay_area --bbox=-123.280334,37.011326,-120.607910,38.955137, --clip_to_bbox --exclude=o-9-amtrak,o-9-amtrakcharteredvehicle`

[![IMAGE ALT TEXT](http://i.imgur.com/twYVa47.jpg)](https://vimeo.com/226987064 "Bay Area Transit Flows")

## San Francisco Transit Flows
Increase frames to 7,200 for a two minute video (60 fps * 120 seconds = 7,200 frames).

- `python transitflow.py --name=san_francisco --bbox=-122.515411,37.710714,-122.349243,37.853983 --clip_to_bbox --frames=7200`

[![IMAGE ALT TEXT](http://i.imgur.com/3zF4uE7.png)](https://vimeo.com/230629960 "San Francisco Transit Flows")

## Los Angeles Transit Flows

- `python transitflow.py --name=los_angeles --bbox=-119.448853,32.925707,-116.768188,34.664841 --clip_to_bbox`

[![IMAGE ALT TEXT](http://i.imgur.com/wHlD0OU.jpg)](https://vimeo.com/230629960 "Los Angeles Transit Flows")


## Boston Transit Flows

- `python transitflow.py --name=boston --bbox=-71.386414,42.194951,-70.753326,42.600609 --clip_to_bbox`

[![IMAGE ALT TEXT](http://i.imgur.com/vbQ9Exj.png)](https://vimeo.com/230631173 "Boston Transit Flows")


## Vancouver Transit Flows

- `python transitflow.py  --name=vancouver --bbox=-123.441010,49.007249,-122.632141,49.426160 --clip_to_bbox`

[![IMAGE ALT TEXT](http://i.imgur.com/TYvyn1m.jpg)](https://vimeo.com/230689642)

## Atlanta Transit Flows

- `python transitflow.py --name=atlanta --bbox=-84.880371,33.321349,-83.908081,34.198173 --clip_to_bbox`

[![IMAGE ALT TEXT](http://i.imgur.com/749hhoE.png)](https://vimeo.com/230490552 "Atlanta Transit Flows")


# How it works

To get the data, the `transitflow.py` makes use of three Transitland API endpoints:

1) **Stops** to get transit stop locations
2) **Routes** to get operator vehicle types
3) **ScheduleStopPairs** to get origin -> destination schedule stop pairs, including timestamps and geolocations.

The `ScheduleStopPairs` endpoint does the bulk of the work. Each `ScheduleStopPair` is an edge between an origin stop and a destination stop. Each `ScheduleStopPair` also includes origin departure time and destination arrival time, and a service calendar which tells you which days a trip is possible. *TransitFlow* searches for all `ScheduleStopPairs` for a specified operator or within a specified bounding box. It then concatenates these `ScheduleStopPairs` into a table and outputs a single output csv file which will drive the animation. The Processing sketch reads in this output csv file, uses the [Unfolding Maps](http://unfoldingmaps.org/) library to convert geolocations into screen positions, and animates vehicle movements from origin stop to destination stop using linear interpolation.

# How to use it

There are two ways to go about using this tool:

### 1) Search by transit operator onestop_id

To animate a particular transit operator, find that operator's `onestop_id` using the [Transitland Feed Registery](https://transit.land/feed-registry/). The `onestop_id` for BART, for example, is `o-9q9-bart`.

Then, you can download the data and create an animation for that operator with a single command line argument, such as:

`python transitflow.py --name=bay_area --operator=o-9q9-bart`

### 2) Search by bounding box

To animate every operator in a bounding box, you may pass in the bounding box as a command line argument. You may also decide to clip the results to that bounding box, or exclude particular operators.

For example, this command line argument will produce an animation of every transit operator in the "greater" Bay Area, excluding Amtrak.

`python transitflow.py --name=bay_area --bbox=37.011326,-123.280334,38.955137,-120.607910 --clip_to_bbox --exclude=o-9-amtrak`

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

# Command line arguments

**Key**|**Status**|**Description**|**Example**
-----|-----|-----|-----
--name|required|The name of your project|--name=boston
--date|optional|Defaults to today's date|--date=2017-08-15
--operator|optional|Operator onestop_id|--operator=o-drt-mbta
--bbox|optional|West, South, East, North| --bbox=-71.4811,42.1135,-70.6709,42.6157
--clip\_to\_bbox|optional|Clip results to bounding box|--clip\_to\_bbox
--exclude|optional|Operators to be excluded|--exclude=o-9-amtrak
--apikey|optional|Mapzen API key|--apikey=mapzen-abc1234
