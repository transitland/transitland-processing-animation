# Visualizing Transit Frequency

Urban planner Jarrett Walker emphasizes the importance of **transit frequency**:

> Transit frequency is the elapsed time between consecutive buses (or trains, or ferries) on a line, which determines the maximum waiting time.  People who are used to getting around by a private vehicle (car or bike) often underestimate the importance of frequency, because there isn’t an equivalent to it in their experience.  A private vehicle is ready to go when you are, but transit is not going until it comes.  High frequency means transit is coming soon, which means that it approximates the feeling of liberty you have with your private vehicle – that you can go anytime.  Frequency is freedom! http://humantransit.org/2015/07/mega-explainer-the-ridership-recipe.html

This makes intuitive sense. Transit networks with higher trip frequencies and shorter waiting times will yield a better, more empowering experience for passengers than those with lower frequencies and longer waiting times.

Analyzing transit frequency in an intuitive way, however, can be difficult. Traditional, static transit maps provide geographic context but do not give any information about trip frequency. Daily or weekly timetables provide information about trip frequency but can be overwhelming, unintuitive and lacking geographic context. Perhaps we can use spatial-temporal visualization to combine the spatial information of a static transit map with the temporal information of a timetable, and make it easer to talk and think about transit frequency!

This is the motivation behind *TransitFlow*, an experimental set of tools that can be used to generate spatial-temporal transit network visualizations from the command line.

![IMAGE ALT TEXT](http://i.imgur.com/cMDfgkQ.png)

*Mmmm... timetables. Provided by the San Francisco Municipal Transportation Agency.*

*TransitFlow* consists of two parts:
  1) A few python scripts to retrieve and wrangle transit schedule data from the [Transitland API](https://transit.land/), an open-source project sponsored by [Mapzen](mapzen.com)

  2) A template to generate a [Processing](processing.org) script to animate that data.

Let's look at a few examples of what you can do with *TransitFlow*.

## Bay Area

- `python transitflow.py --date=2017-08-15 --apikey=mapzen-ai1duha --name=bay_area --bbox=37.011326,-123.280334,38.955137,-120.607910 --clip_to_bbox --exclude=o-9-amtrak,o-9-amtrakcharteredvehicle`

[![IMAGE ALT TEXT](http://i.imgur.com/c8PAnuD.png)](https://vimeo.com/226987064 "Transit Flow Map of San Francisco Bay Area")

## Los Angeles

- `python transitflow.py --date=2017-08-15 --apikey=mapzen-ai1duha --name=los_angeles --bbox=32.925707,-119.448853,34.664841,-116.768188 --clip_to_bbox`

[![IMAGE ALT TEXT](http://i.imgur.com/749hhoE.png)](https://vimeo.com/226987064 "Transit Flow Map of San Francisco Bay Area")

## Atlanta

- `python transitflow.py --date=2017-08-15 --apikey=mapzen-ai1duha --name=atlanta --bbox=33.321349,-84.880371,34.198173,-83.908081 --clip_to_bbox`

[![IMAGE ALT TEXT](http://i.imgur.com/749hhoE.png)](https://vimeo.com/226987064 "Transit Flow Map of San Francisco Bay Area")


## New Zealand

## Boston / Chicago, New York, DC, Vancouver

## How it works

To get the data, the `transitflow.py` makes use of three Transitland API endpoints:

- 1) **Stops** to get transit stop locations
- 2) **Routes** to get operator vehicle types
- 3) **ScheduleStopPairs** to get scheduled origin -> destination stop pairs, including timestamps and geolocations.

The `ScheduleStopPairs` endpoint does the bulk of the work. Each `ScheduleStopPair` contains an origin stop, a destination stop, a route, an operator, and arrival and departure times. Each `ScheduleStopPair` also includes a service calendar, describing which days a trip is possible. Accessibility information for wheelchair and bicycle riders is included, if available.

The python script `transitflow.py` uses the [schedule stop pairs API](http://transit.land/api/v1/schedule_stop_pairs) endpoint to search for all `ScheduleStopPair`s for a specified operator or within a specified bounding box. It then concatenates these `ScheduleStopPair`s into a table and outputs a single output csv file which will drive the animation. The Processing sketch reads in this output csv file, uses the [Unfolding Maps](http://unfoldingmaps.org/) by Till Nagel to convert geolocations to pixels, and animates vehicle movements using linear interpolation.

## How to use it

There are two ways to go about using this tool:

#### 1) Search by transit operator onestop_id

To animate a particular transit operator, search for that operator's `onestop_id` using the [Transitland Feed Registery](https://transit.land/feed-registry/). The `onestop_id` for BART, for example, is `o-9q9-bart`.

Then, you can download the data and create an animation for that operator using *TransitFlow* with a single command line argument, such as:

`python transitflow.py --date=2017-08-15 --name=bay_area --operator=o-9q9-bart`

#### 2) Search by bounding box

To animate every operator in a bounding box, you may pass in the bounding box as a command line argument. You may also decide to clip the results to that bounding box, or exclude particular operators.

For example, this command line argument will produce an animation of every transit operator in the "greater" Bay Area, excluding Amtrak.

`python transitflow.py --date=2017-08-15 --apikey=mapzen-ai1duha --name=bay_area --bbox=37.011326,-123.280334,38.955137,-120.607910 --clip_to_bbox --exclude=o-9-amtrak,o-9-amtrakcharteredvehicle,o-9q-amtrakcalifornia`

### Command line arguments

**Key **|**Status**|**Description**
:-----:|:-----:|:-----:
--date|required|The data that you want to animate
--name|required|The name of your project.
--operator|optional|Operator onestop, id
--bbox|optional|Bounding box
--clip\_to\_bbox|optional|Clip results to bounding box
