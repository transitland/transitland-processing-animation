import requests
import pandas as pd
import numpy as np
import datetime as dt
import glob
import os
import argparse

MAPZEN_APIKEY = None
OUTPUT_NAME = None

# Helper functions

def transitland_request(url):
    """This is a helper function to paginate through Transitland api responses with multiple pages."""
    next_url = url
    while next_url:
        # next url in 'meta'
        data = requests.get(next_url).json()
        meta = data.get('meta', {})
        next_url = meta.get('next')
        # transitland responses will have one main key that isn't "meta"
        main_key = (set(data.keys()) - set(['meta'])).pop()
        for item in data[main_key]:
            yield item

def get_vehicle_types(operator_onestop_id):
    """This function will get all **vehicle types** for an operator, by route. So we can ask *"what vehicle type is this particular trip?"* and color code trips by vehicle type."""
    routes_url = "http://transit.land/api/v1/routes?operated_by={}&per_page=1000&api_key={}".format(operator_onestop_id, MAPZEN_APIKEY)
    lookup_vehicle_types = {i['onestop_id']: i['vehicle_type'] for i in transitland_request(routes_url)}
    return lookup_vehicle_types

# Get stops

def get_stop_lats(operator_onestop_id):
    """Get stop lats for a particular operator."""
    stops_url = "http://transit.land/api/v1/stops?served_by={}&per_page=1000&api_key={}".format(operator_onestop_id, MAPZEN_APIKEY)
    lookup_stop_lats = {i['onestop_id']: i['geometry']['coordinates'][1] for i in transitland_request(stops_url)}
    return lookup_stop_lats

def get_stop_lons(operator_onestop_id):
    """Get stop lons for a particular operator."""
    stops_url = "http://transit.land/api/v1/stops?served_by={}&per_page=1000&api_key={}".format(operator_onestop_id, MAPZEN_APIKEY)
    lookup_stop_lons = {i['onestop_id']: i['geometry']['coordinates'][0] for i in transitland_request(stops_url)}
    return lookup_stop_lons

# Get Schedule data

def get_schedule_stop_pairs(operator_onestop_id, date):
    """This function gets origin-destination pairs and timestamps from the schedule stop pairs API. This is the most important function and the largest API request."""
    schedule_stop_pairs_url = "http://transit.land/api/v1/schedule_stop_pairs?date={}&operator_onestop_id={}&per_page=1000&api_key={}".format(date, operator_onestop_id, MAPZEN_APIKEY)
    print schedule_stop_pairs_url
    origin_times = []
    destination_times = []
    origin_stops = []
    destination_stops = []
    route_ids = []
    count=0
    for i in transitland_request(schedule_stop_pairs_url):
        count+=1
        if count % 10000 == 0:
            print count
        origin_times.append(i['origin_departure_time'])
        destination_times.append(i['destination_arrival_time'])
        origin_stops.append(i['origin_onestop_id'])
        destination_stops.append(i['destination_onestop_id'])
        route_ids.append(i['route_onestop_id'])

    return origin_times, destination_times, origin_stops, destination_stops, route_ids

def calculate_durations(origin_times, destination_times):
    """This function calculates durations between origin and destination pairs (in seconds)."""
    origin_since_epoch = [int(i.split(':')[0])*60*60 + int(i.split(':')[1])*60 + int(i.split(':')[2]) for i in origin_times]
    destination_since_epoch = [int(i.split(':')[0])*60*60 + int(i.split(':')[1])*60 + int(i.split(':')[2]) for i in destination_times]
    durations = [b - a for a, b in zip(origin_since_epoch, destination_since_epoch)]
    return durations

def clean_times(origin_times, destination_times):
    """This function cleans origin and destination times. This is a bit tricky because operators will often include non-real times such as "26:00:00" to indicate 2am the next day."""
    # Modulo away the > 24 hours
    origin_times_clean = [":".join([str(int(i.split(':')[0]) % 24), i.split(':')[1], i.split(':')[2]]) for i in origin_times]
    destination_times_clean = [":".join([str(int(i.split(':')[0]) % 24), i.split(':')[1], i.split(':')[2]]) for i in destination_times]
    return origin_times_clean, destination_times_clean

def add_dates(date, origin_times_clean, destination_times_clean):
    """This function appends destination and origin dates to times, so that times become datetimes."""
    date1 = dt.datetime.strptime(date, "%Y-%m-%d").date()
    date2 = date1 + dt.timedelta(days=1)

    origin_datetimes = []
    destination_datetimes = []

    for i in range(len(origin_times_clean)):
        if int(destination_times_clean[i].split(":")[0]) < int(origin_times_clean[i].split(":")[0]):
            origin_datetime = str(date1) + " " + origin_times_clean[i]
            destination_datetime = str(date2) + " " + destination_times_clean[i]
        else:
            origin_datetime = str(date1) + " " + origin_times_clean[i]
            destination_datetime = str(date1) + " " + destination_times_clean[i]

        origin_datetimes.append(origin_datetime)
        destination_datetimes.append(destination_datetime)

    return origin_datetimes, destination_datetimes

# Output

def generate_output(operator_onestop_id, origin_datetimes, destination_datetimes, durations, origin_stops, destination_stops, route_ids, lookup_stop_lats, lookup_stop_lons, lookup_vehicle_types):
    """This function generates the output table, to be saved later as a csv."""
    origin_stop_lats = [lookup_stop_lats[i] for i in origin_stops]
    origin_stop_lons = [lookup_stop_lons[i] for i in origin_stops]
    destination_stop_lats = [lookup_stop_lats[i] for i in destination_stops]
    destination_stop_lons = [lookup_stop_lons[i] for i in destination_stops]
    vehicle_types = []
    for i in route_ids:
        try:
            vehicle_type = lookup_vehicle_types[i]
            vehicle_types.append(vehicle_type)
        except:
            vehicle_types.append("NA")

    output = pd.DataFrame({
        'route_type': vehicle_types,
        'start_time': origin_datetimes,
        'start_lat': origin_stop_lats,
        'start_lon': origin_stop_lons,
        'end_time': destination_datetimes,
        'end_lat': destination_stop_lats,
        'end_lon': destination_stop_lons,
        'duration': durations
    })
    output = output[['start_time', 'start_lat', 'start_lon', 'end_time', 'end_lat', 'end_lon', 'duration', 'route_type']]
    return output

# Combine data

def concatenate_csvs(path):
    all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent
    df_from_each_file = (pd.read_csv(f) for f in all_files) # generators
    concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)
    del concatenated_df['Unnamed: 0'] # delete the blank column that gets added
    concatenated_df['start_time'] = pd.to_datetime(concatenated_df['start_time'])
    concatenated_df['end_time'] = pd.to_datetime(concatenated_df['end_time'])
    concatenated_df = concatenated_df.sort_values(by="start_time").reset_index(drop=True)
    return concatenated_df

def animate_one_day(operator_onestop_id, date):
    """This is the main function that ties all of the above together!"""
    lookup_vehicle_types = get_vehicle_types(operator_onestop_id)
    lookup_stop_lats = get_stop_lats(operator_onestop_id)
    lookup_stop_lons = get_stop_lons(operator_onestop_id)
    origin_times, destination_times, origin_stops, destination_stops, route_ids = get_schedule_stop_pairs(operator_onestop_id, date)
    durations = calculate_durations(origin_times, destination_times)
    origin_times_clean, destination_times_clean = clean_times(origin_times, destination_times)
    origin_datetimes, destination_datetimes = add_dates(date, origin_times_clean, destination_times_clean)
    output = generate_output(operator_onestop_id, origin_datetimes, destination_datetimes, durations, origin_stops, destination_stops, route_ids, lookup_stop_lats, lookup_stop_lons, lookup_vehicle_types)
    output = output.sort_values(by='start_time').reset_index(drop=True)
    return output

def animate_many_operators(operators, date):
    """Main."""
    starttime = dt.datetime.now()
    print starttime

    results = []
    failures = []

    length = len(operators)
    count = 1

    for i in operators:
        print i, count, "/", length
        try:
            output = animate_one_day(i, date)
            results.append(output)
            print "success!"
            print ""
            output.to_csv("data/indiv_operators/{}/{}.csv".format(OUTPUT_NAME,i))
        except StandardError:
            failures.append(i)
            print "failed"
            print ""
        count += 1

    endtime = dt.datetime.now()
    print endtime
    print "Time taken:", endtime - starttime
    return results, failures

# Stacked bar chart functions

def count_vehicles_on_screen(concatenated_df, date):
    number_of_vehicles = []
    number_of_buses = []
    number_of_trams = []
    number_of_cablecars = []
    number_of_metros = []
    number_of_trains = []
    number_of_ferries = []

    day = dt.datetime.strptime(date, "%Y-%m-%d")
    thisday = dt.datetime.strftime(day, "%Y-%m-%d")

    # Every minute in the day
    the_day = [pd.to_datetime(thisday) + dt.timedelta(seconds = i*15) for i in range(60 * 24 * 4)]

    count = 0
    for minute in the_day:

        vehicles_on_the_road = concatenated_df[(concatenated_df['end_time'] > minute) & (concatenated_df['start_time'] <= minute)]
        number_vehicles_on_the_road = len(vehicles_on_the_road)
        number_of_vehicles.append(number_vehicles_on_the_road)

        for route_type in ['bus', 'tram', 'cablecar', 'metro', 'rail', 'ferry']:
            just_this_mode = vehicles_on_the_road[vehicles_on_the_road['route_type'] == route_type]
            number_of_this_mode = len(just_this_mode)
            if route_type == 'bus':
                number_of_buses.append(number_of_this_mode)
            elif route_type == 'tram':
                number_of_trams.append(number_of_this_mode)
            elif route_type == 'cablecar':
                number_of_cablecars.append(number_of_this_mode)
            elif route_type == 'metro':
                number_of_metros.append(number_of_this_mode)
            elif route_type == 'rail':
                number_of_trains.append(number_of_this_mode)
            elif route_type == 'ferry':
                number_of_ferries.append(number_of_this_mode)

        if count % (60*4) == 0:
            print minute

        count += 1

    vehicles = pd.DataFrame(zip(the_day, number_of_vehicles))
    buses = pd.DataFrame(zip(the_day, number_of_buses))
    trams = pd.DataFrame(zip(the_day, number_of_trams))
    cablecars = pd.DataFrame(zip(the_day, number_of_cablecars))
    metros = pd.DataFrame(zip(the_day, number_of_metros))
    trains = pd.DataFrame(zip(the_day, number_of_trains))
    ferries = pd.DataFrame(zip(the_day, number_of_ferries))

    for df in [vehicles, buses, trams, metros, cablecars, trains, ferries]:
        df.columns = ['time', 'count']

    return vehicles, buses, trams, metros, cablecars, trains, ferries


if __name__ == "__main__":
    # Sign up for a [Mapzen API key](https://mapzen.com/developers/sign_up) if you don't already have one.
    name = r"bay_area" # this determines how to name output csv files

    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Animation day") # default=TODAY
    parser.add_argument("--apikey", help="Mapzen API Key")
    parser.add_argument(
      "--name",
      help="Output directory name",
      default="bay_area"
    )
    parser.add_argument(
      "--bbox",
      help="Bounding box",
      default="37.011326,-123.280334,38.955137,-120.607910"
    )
    # parser.add_argument("operator", nargs=1, help="Operator Onestop ID")

    args = parser.parse_args()

    if not args.date:
      raise Exception('date required')

    if not args.apikey:
      raise Exception('api key required')

    MAPZEN_APIKEY = args.apikey
    OUTPUT_NAME = args.name
    date = args.date
    south, west, north, east = args.bbox.split(",")

    print "date: ", date
    print "name: ", OUTPUT_NAME
    print "apikey: ", MAPZEN_APIKEY
    print "south, west, north, east", south, west, north, east

    # First, let's get a list of the onestop id's for every operator in our bounding box.
    operators_url = "http://transit.land/api/v1/operators?bbox={},{},{},{}&per_page=1000&api_key={}".format(west, south, east, north, MAPZEN_APIKEY)
    operators_in_bbox = {i['onestop_id'] for i in transitland_request(operators_url)}
    print len(operators_in_bbox), "operators in bounding box."

    # We will exclude national Amtrak trips from the visualizaiton and vehicle counts.
    operators_in_bbox -= {'o-9-amtrak'}
    print len(operators_in_bbox), "operators to be downloaded."

    # ### Run script on every operator and save each operator's results to a separate csv
    if not os.path.exists("data/indiv_operators/{}".format(OUTPUT_NAME)):
        os.makedirs("data/indiv_operators/{}".format(OUTPUT_NAME))
    results, failures = animate_many_operators(operators_in_bbox, date)
    print len(results), "operators successfully downloaded."
    print len(failures), "operators failed."
    if len(failures): print "failed operators:", failures

    # ### Concatenate all individual operator csv files into one big dataframe
    concatenated_df = concatenate_csvs("data/indiv_operators/{}".format(OUTPUT_NAME))
    concatenated_df.head()
    concatenated_df.to_csv("data/output/{}.csv".format(OUTPUT_NAME))

    print concatenated_df.shape

    # ### That's it for the trip data!

    # ### Next step:  Count number of vehicles in transit at every 15 second interval
    # In order to add a stacked area chart to the animation showing the number
    # of vehicles on the road, we will do some counting here in python and save
    # the results in six separate csv files (one for each mode of transit in
    # SF Bay Area: bus, tram, cablecar, metro, rail, ferry.
    # The Processing sketch will read in each file and use them to plot a
    # stacked area chart.

    # Vehicle counting logic:
    #
    # At any given time t, every vehicle on the road will have started its
    # current trip before $t$ and will end its current trip after t. So we
    # can filter our data by end time and start time to calculate the number
    # of vehicles scheduled to be on the road at any given time. We will be
    # inclusive on the start date but exclusive on the end date to avoid
    # double counting a trip -- i.e. if a trip starts at 10:00am then it
    # is "on the road" at 10:00am, but if a trip ends at 10:15am, then it is
    # not considered "on the road" at 10:15am. This way, we avoid double
    # counting vehicles.

    print "Counting number of vehicles in transit."
    vehicles, buses, trams, metros, cablecars, trains, ferries = count_vehicles_on_screen(concatenated_df, date)

    # ### Save vehicle counts to csv (3600 frame version)
    # Our Processing sketch has 3,600 frames (at 60 frames per second makes
    # a one minute video). One day has 5,760 15-second intervals. So to make
    # things easy we will select the vehicle counts at 3,600 of the 15-second
    # intervals throughout the day. We will select them randomly, but will
    # maintain chronological order by sorting and also consistency between
    # vehicle types by using a consitent set of random indices to select
    # counts for different vehicle types.

    frames = 3600
    random_indices = np.sort(np.random.choice(vehicles.index, frames, replace=False))

    vehicles_counts_output = vehicles.loc[random_indices].reset_index(drop=True)
    vehicles_counts_output['frame'] = vehicles_counts_output.index

    buses_counts_output = buses.loc[random_indices].reset_index(drop=True)
    buses_counts_output['frame'] = buses_counts_output.index

    trams_counts_output = trams.loc[random_indices].reset_index(drop=True)
    trams_counts_output['frame'] = trams_counts_output.index

    metros_counts_output = metros.loc[random_indices].reset_index(drop=True)
    metros_counts_output['frame'] = metros_counts_output.index

    cablecars_counts_output = cablecars.loc[random_indices].reset_index(drop=True)
    cablecars_counts_output['frame'] = cablecars_counts_output.index

    trains_counts_output = trains.loc[random_indices].reset_index(drop=True)
    trains_counts_output['frame'] = trains_counts_output.index

    ferries_counts_output = ferries.loc[random_indices].reset_index(drop=True)
    ferries_counts_output['frame'] = ferries_counts_output.index

    # Save these vehicle count stats to csv's.
    if not os.path.exists("data/vehicle_counts/{}".format(OUTPUT_NAME)):
        os.makedirs("data/vehicle_counts/{}".format(OUTPUT_NAME))
    vehicles_counts_output.to_csv("data/vehicle_counts/{}/vehicles_count_{}.csv".format(OUTPUT_NAME, frames))
    buses_counts_output.to_csv("data/vehicle_counts/{}/buses_count_{}.csv".format(OUTPUT_NAME, frames))
    trams_counts_output.to_csv("data/vehicle_counts/{}/trams_count_{}.csv".format(OUTPUT_NAME, frames))
    metros_counts_output.to_csv("data/vehicle_counts/{}/metros_count_{}.csv".format(OUTPUT_NAME, frames))
    cablecars_counts_output.to_csv("data/vehicle_counts/{}/cablecars_count_{}.csv".format(OUTPUT_NAME, frames))
    trains_counts_output.to_csv("data/vehicle_counts/{}/trains_count_{}.csv".format(OUTPUT_NAME, frames))
    ferries_counts_output.to_csv("data/vehicle_counts/{}/ferries_count_{}.csv".format(OUTPUT_NAME, frames))
