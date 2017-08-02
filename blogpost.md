# Visualizing Transit Frequency

Urban planner Jarrett Walker emphasizes the importance of transit **frequency**:

> First, you really must understand transit frequency.  It’s the elapsed time between consecutive buses (or trains, or ferries) on a line, which determines the maximum waiting time.  People who are used to getting around by a private vehicle (car or bike) often underestimate the importance of frequency, because there isn’t an equivalent to it in their experience.  A private vehicle is ready to go when you are, but transit is not going until it comes.  High frequency means transit is coming soon, which means that it approximates the feeling of liberty you have with your private vehicle – that you can go anytime.  Frequency is freedom! http://humantransit.org/2015/07/mega-explainer-the-ridership-recipe.html

This makes intuitive sense. Transit networks with higher trip frequencies and shorter waiting times will yield a better experience for the rider than those with lower frequencies and longer waiting times.

Communicating about frequency in an intuitive way, however, can be difficult. Traditional, static transit maps give geographic context to a transit network but do not give any information about trip frequency. Daily timetables provide information about trip frequency but can be overwhelming, unintuitive and lacking geographic context. Thus, I am interested in the potential for spatial-temporal visualization to make it more easier to analyze and communicate about transit frequency.

I created the below animation to investigate transit frequency in the San Francisco "greater" Bay Area.

[![IMAGE ALT TEXT](http://i.imgur.com/kkOxCil.png)](https://vimeo.com/226987064 "Transit Flow Map of San Francisco Bay Area")

[Insert comments / observations about bay area transit frequency]

There are two steps to creating this visualization:

1. Download transit trip data from the Transitland Datastore API, which brings together transit data from authoritative sources (listed in the [Feed Registry](https://transit.land/feed-registry/)) with contributions, edits, and fixes from transit enthusiasts and developers.

2. Animate every trip using Processing and Unfolding Maps. 

[Insert more comments about the process...?]
