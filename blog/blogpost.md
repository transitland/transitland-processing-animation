# Visualizing Transit Frequency

Urban planner Jarrett Walker emphasizes the importance of transit **frequency**:

> Transit frequency is the elapsed time between consecutive buses (or trains, or ferries) on a line, which determines the maximum waiting time.  People who are used to getting around by a private vehicle (car or bike) often underestimate the importance of frequency, because there isn’t an equivalent to it in their experience.  A private vehicle is ready to go when you are, but transit is not going until it comes.  High frequency means transit is coming soon, which means that it approximates the feeling of liberty you have with your private vehicle – that you can go anytime.  Frequency is freedom! http://humantransit.org/2015/07/mega-explainer-the-ridership-recipe.html

This makes intuitive sense. Transit networks with higher trip frequencies and shorter waiting times will yield a better, more empowering experience for passengers than those with lower frequencies and longer waiting times.

Analyzing transit frequency in an intuitive way, however, can be difficult. Traditional, static transit maps provide geographic context to a transit network but do not give any information about trip frequency. Daily or weekly timetables provide information about trip frequency but can be overwhelming, unintuitive and lacking geographic context. Thus, I am interested in the potential for spatial-temporal visualization to make it easier to think and talk about transit frequency. This is the motivation behind *TransitFlow*, a software library to easily visualize transit networks from the command line.

*TransitFlow* contains two parts: a python script to retrieve and wrangle data from the [Transitland API](https://transit.land/), and a [Processing](processing.org) script to visualize that data.

Bay Area:
[![IMAGE ALT TEXT](http://i.imgur.com/kkOxCil.png)](https://vimeo.com/226987064 "Transit Flow Map of San Francisco Bay Area")

[Insert comments / observations about bay area transit frequency]

London:

There are two main parts to creating an animation like these:

1. Use a python script to download transit schedule data from Transitland, an open-source project sponsored by Mapzen.

2. Use Processing with the Unfolding Maps library to visualize scheduled transit trips.

[Insert more comments about the process...?]
