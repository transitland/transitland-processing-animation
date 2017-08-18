# Visualizing Transit Frequency with *TransitLand*

Urban planner Jarrett Walker emphasizes the importance of **transit frequency**:

> Transit frequency is the elapsed time between consecutive buses (or trains, or ferries) on a line, which determines the maximum waiting time.  People who are used to getting around by a private vehicle (car or bike) often underestimate the importance of frequency, because there isn’t an equivalent to it in their experience.  A private vehicle is ready to go when you are, but transit is not going until it comes.  High frequency means transit is coming soon, which means that it approximates the feeling of liberty you have with your private vehicle – that you can go anytime.  Frequency is freedom! http://humantransit.org/2015/07/mega-explainer-the-ridership-recipe.html

This makes intuitive sense. Transit networks with higher trip frequencies and shorter waiting times will yield a better, more empowering experience for passengers than those with lower frequencies and longer waiting times.

Analyzing transit frequency in an intuitive way, however, can be difficult. Traditional, static transit maps provide geographic context to a transit network but do not give any information about trip frequency. Daily or weekly timetables provide information about trip frequency but can be overwhelming, unintuitive and lacking geographic context. Thus, I am interested in the potential for spatial-temporal visualization to make it easier to think and talk about transit frequency. This is the motivation behind *TransitFlow*, an experimental software package that can be used to easily animate transit networks.

*TransitFlow* contains two parts: a python script to retrieve and wrangle data from the [Transitland API](https://transit.land/), an open-source project sponsored by [Mapzen](mapzen.com), and a [Processing](processing.org) script to create an animation from that data.

In particular, we will make use of Mapzen's `ScheduleStopPair` representation. Each `ScheduleStopPair` contains an origin stop, a destination stop, a route, an operator, and arrival and departure times. Each `ScheduleStopPair` also includes a service calendar, describing which days a trip is possible. Accessibility information for wheelchair and bicycle riders is included, if available.

The python script `transitflow.py` uses the [schedule stop pairs API](http://transit.land/api/v1/schedule_stop_pairs) endpoint to search for all `ScheduleStopPair`s for a specified operator or within a specified bounding box. It then concatenates these `ScheduleStopPair`s into a table and outputs a single output csv file which will drive the animation. The Processing sketch reads in this output csv file, uses the [Unfolding Maps](http://unfoldingmaps.org/) by Till Nagel to convert geolocations to pixels, and animates vehicle movements using linear interpolation.

### Animate a particular operator

To animate a particular transit operator, search for that operator's `onestop_id` using the [Transitland Feed Registery](https://transit.land/feed-registry/). The `onestop_id` for BART, for example, is `o-9q9-bart`.

Then, you can download the data and create an animation for that operator using *TransitFlow* with a single command line argument, such as:

`python transitflow.py --date=2017-08-15 --name=bay_area --operator=o-9q9-bart`

### Animate all operators in a bounding box

To animate every operator in a bounding box, you may pass in the bounding box as a command line argument. You may also decide to clip the results to that bounding box, or exclude particular operators.

For example, this command line argument will produce an animation of every transit operator in the "greater" Bay Area, excluding Amtrak.

`python transitflow.py --date=2017-08-15 --apikey=mapzen-ai1duha --name=bay_area --bbox=37.011326,-123.280334,38.955137,-120.607910 --clip_to_bbox --exclude=o-9-amtrak,o-9-amtrakcharteredvehicle,o-9q-amtrakcalifornia`


Here is the resulting Bay Area animation:

[![IMAGE ALT TEXT](http://i.imgur.com/kkOxCil.png)](https://vimeo.com/226987064 "Transit Flow Map of San Francisco Bay Area")

Please try out the code yourself, and let us know about any visualizations you create!
