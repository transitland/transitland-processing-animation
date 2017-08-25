import pandas as pd
import numpy as np
import datetime as dt
import glob
import os
import argparse
import math
import shutil
from string import Template

from transitland_api import TransitlandRequest

TLAPI = None
OUTPUT_NAME = None
DATE = None
FRAMES = None
PER_PAGE = 10000

# Time
def time_to_seconds(value):
    h, m, s = map(int, value.split(':'))
    return (h * 60 * 60) + (m * 60) + s

def seconds_to_time(value):
    return '%02d:%02d:%02d'%(seconds_to_hms(value))

def seconds_to_hms(value):
    m, s = divmod(value, 60)
    h, m = divmod(m, 60)
    return h, m, s

# Helper functions
def get_vehicle_types(operator_onestop_id):
    """This function will get all **vehicle types** for an operator, by route. So we can ask *"what vehicle type is this particular trip?"* and color code trips by vehicle type."""
    routes_request = TLAPI.request('routes', operated_by=operator_onestop_id, per_page=PER_PAGE)
    lookup_vehicle_types = {i['onestop_id']: i['vehicle_type'] for i in routes_request}
    return lookup_vehicle_types

# Get stops
def get_stop_lat_lons(operator_onestop_id):
    """Get stop lats and stop lons for a particular operator."""
    stops_request = TLAPI.request('stops', served_by=operator_onestop_id, per_page=PER_PAGE)
    lookup_stop_lats = {}
    lookup_stop_lons = {}
    for stop in stops_request:
      lookup_stop_lats[stop['onestop_id']] = stop['geometry']['coordinates'][1]
      lookup_stop_lons[stop['onestop_id']] = stop['geometry']['coordinates'][0]
    return lookup_stop_lats, lookup_stop_lons

# Get Schedule data
def get_schedule_stop_pairs(operator_onestop_id, date):
    """This function gets origin-destination pairs and timestamps from the schedule stop pairs API. This is the most important function and the largest API request."""
    ssp_request = TLAPI.request('schedule_stop_pairs', operator_onestop_id=operator_onestop_id, date=date, per_page=PER_PAGE, sort_min_id=0)
    origin_times = []
    destination_times = []
    origin_stops = []
    destination_stops = []
    route_ids = []
    count=0
    for i in ssp_request:
        count+=1
        if count % 10000 == 0:
            print count
        if i['frequency_start_time']:
            start = time_to_seconds(i['frequency_start_time'])
            now = start
            end = time_to_seconds(i['frequency_end_time'])
            incr = i['frequency_headway_seconds']
            while now <= end:
                print "freq: start %s now %s end %s incr %s"%(start, now, end, incr)
                odt = (time_to_seconds(i['origin_departure_time']) - start) + now
                dat = (time_to_seconds(i['destination_arrival_time']) - start) + now
                now += incr
                origin_times.append(seconds_to_time(odt))
                destination_times.append(seconds_to_time(dat))
                origin_stops.append(i['origin_onestop_id'])
                destination_stops.append(i['destination_onestop_id'])
                route_ids.append(i['route_onestop_id'])
        else:
            origin_times.append(i['origin_departure_time'])
            destination_times.append(i['destination_arrival_time'])
            origin_stops.append(i['origin_onestop_id'])
            destination_stops.append(i['destination_onestop_id'])
            route_ids.append(i['route_onestop_id'])

    return origin_times, destination_times, origin_stops, destination_stops, route_ids

def calculate_durations(origin_times, destination_times):
    """This function calculates durations between origin and destination pairs (in seconds)."""
    origin_since_epoch = map(time_to_seconds, origin_times)
    destination_since_epoch = map(time_to_seconds, destination_times)
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
    lookup_stop_lats, lookup_stop_lons = get_stop_lat_lons(operator_onestop_id)
    origin_times, destination_times, origin_stops, destination_stops, route_ids = get_schedule_stop_pairs(operator_onestop_id, date)
    durations = calculate_durations(origin_times, destination_times)
    origin_times_clean, destination_times_clean = clean_times(origin_times, destination_times)
    origin_datetimes, destination_datetimes = add_dates(date, origin_times_clean, destination_times_clean)
    output = generate_output(operator_onestop_id, origin_datetimes, destination_datetimes, durations, origin_stops, destination_stops, route_ids, lookup_stop_lats, lookup_stop_lons, lookup_vehicle_types)
    output = output.sort_values(by='start_time').reset_index(drop=True)
    return output

def animate_operators(operators, date):
    """Main."""
    results = []
    failures = []

    length = len(operators)
    count = 1

    for i in operators:
        i = i.encode('utf-8')
        print i, count, "/", length
        try:
            output = animate_one_day(i, date)
            results.append(output)
            print "success!"
            print ""
            output.to_csv("sketches/{}/{}/data/indiv_operators/{}.csv".format(OUTPUT_NAME, DATE, i))
        except StandardError as e:
            failures.append(i)
            print "failed:"
            print e
        count += 1

    return results, failures

# Calculate bearing
# See: https://gis.stackexchange.com/questions/29239/calculate-bearing-between-two-decimal-gps-coordinates/48911
def calc_bearing_between_points(startLat, startLong, endLat, endLong):

    startLat = math.radians(startLat)
    startLong = math.radians(startLong)
    endLat = math.radians(endLat)
    endLong = math.radians(endLong)
    dLong = endLong - startLong
    dPhi = math.log(math.tan(endLat/2.0+math.pi/4.0)/math.tan(startLat/2.0+math.pi/4.0))
    if abs(dLong) > math.pi:
        if dLong > 0.0:
            dLong = -(2.0 * math.pi - dLong)
        else:
            dLong = (2.0 * math.pi + dLong)
    bearing = (math.degrees(math.atan2(dLong, dPhi)) + 360.0) % 360.0;
    return bearing

# Stacked bar chart functions
def count_vehicles_on_screen(concatenated_df, date, frames):
    number_of_vehicles = []
    number_of_buses = []
    number_of_trams = []
    number_of_cablecars = []
    number_of_metros = []
    number_of_trains = []
    number_of_ferries = []

    day = dt.datetime.strptime(date, "%Y-%m-%d")
    thisday = dt.datetime.strftime(day, "%Y-%m-%d")

    chunks = float(frames) / (60*24)
    increment = float(60.0 / chunks)

    the_day = [pd.to_datetime(thisday) + dt.timedelta(seconds = i*increment) for i in range(int(60 * 24 * chunks))]

    count = 0
    for increment in the_day:

        vehicles_on_the_road = concatenated_df[(concatenated_df['end_time'] > increment) & (concatenated_df['start_time'] <= increment)]
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

        if count % (60*chunks) == 0:
            print increment

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
    todays_date = str(dt.datetime.today()).split(" ")[0]

    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=todays_date, help="Animation day")
    parser.add_argument("--apikey", help="Mapzen API Key")
    parser.add_argument(
      "--name",
      help="Output directory name",
      default="output"
    )
    parser.add_argument(
      "--bbox",
      help="Bounding box"
    )
    parser.add_argument(
      "--frames",
      help="Number of frames in animation. 3600 frames = 60 second animation.",
      default=3600
    )
    parser.add_argument(
      "--exclude",
      help="Exclude particular operators by operator onestop_id"
    )
    parser.add_argument(
      "--operator",
      help="Download data for a single operator by operator onestop_id",
    )
    parser.add_argument(
      "--clip_to_bbox",
      help="Clip trips to bounding box",
      action="store_true"
    )
    parser.add_argument(
      "--recording",
      help="Records sketch to mp4",
      action="store_true"
    )

    args = parser.parse_args()

    if not args.date:
      raise Exception('date required')

    OUTPUT_NAME = args.name
    DATE = args.date
    FRAMES = args.frames
    RECORDING = args.recording

    TLAPI = TransitlandRequest(
      host='http://transit.land',
      apikey=args.apikey
    )

    print ""
    print "INPUTS:"
    print "date: ", DATE
    print "name: ", OUTPUT_NAME
    print "API key: ", args.apikey

    timer_start = dt.datetime.now()

    if args.bbox:
        west, south, east, north = args.bbox.split(",")
        # west, south, east, north = args.bbox.split(",")
        # bbox = true

    operators = set()
    if args.operator:
        operators |= set(args.operator.split(","))

    exclude_operators = set()
    if args.exclude:
        exclude_operators |= set(args.exclude.split(","))
        print "exclude: ", list(exclude_operators)

    if args.bbox:
        print "bbox: ", west, south, east, north
        print ""
        # First, let's get a list of the onestop id's for every operator in our bounding box.
        operators_request = TLAPI.request('operators', bbox=','.join([west,south,east,north]), per_page=PER_PAGE)
        operators_in_bbox = {i['onestop_id'] for i in operators_request}
        print len(operators_in_bbox), "operators in bounding box."
        operators |= operators_in_bbox

    # I.e. you may want to exclude national Amtrak trips from the visualizaton
    # and vehicle counts: 'o-9-amtrak'
    operators -= exclude_operators
    print len(operators), "operators to be downloaded."
    print ""
    ############

    if not os.path.exists("sketches/{}/{}/data/indiv_operators".format(OUTPUT_NAME, DATE)):
        os.makedirs("sketches/{}/{}/data/indiv_operators".format(OUTPUT_NAME, DATE))
    results, failures = animate_operators(operators, DATE)
    print len(results), "operators successfully downloaded."
    print len(failures), "operators failed."
    if len(failures): print "failed operators:", failures

    # ### Concatenate all individual operator csv files into one big dataframe
    print "Concatenating individual operator outputs."
    df = concatenate_csvs("sketches/{}/{}/data/indiv_operators".format(OUTPUT_NAME, DATE))
    print "Calculating trip segment bearings."
    df['bearing'] = df.apply(lambda row: calc_bearing_between_points(row['start_lat'], row['start_lon'], row['end_lat'], row['end_lon']), axis=1)

    # Clip to bbox. Either the start stop is within the bbox OR the end stop is within the bbox
    if args.bbox and args.clip_to_bbox:
        df = df[
            ((df['start_lat'] >= float(south)) & (df['start_lat'] <= float(north)) & (df['start_lon'] >= float(west)) & (df['start_lon'] <= float(east))) |
            ((df['end_lat'] >= float(south)) & (df['end_lat'] <= float(north)) & (df['end_lon'] >= float(west)) & (df['end_lon'] <= float(east)))
        ]

    # Save to csv.
    df.to_csv("sketches/{}/{}/data/output.csv".format(OUTPUT_NAME, DATE))
    print "Total rows: ", df.shape[0]

    # ### That's it for the trip data!

    # ### Next step:  Count number of vehicles in transit at every 15 second interval
    # In order to add a stacked area chart to the animation showing the number
    # of vehicles on the road, we will do some counting here in python and save
    # the results in six separate csv files (one for each mode of transit in
    # SF Bay Area: bus, tram, cablecar, metro, rail, ferry.
    # The Processing sketch will read in each file and use them to plot a
    # stacked area chart.

    print "Counting number of vehicles in transit."
    vehicles, buses, trams, metros, cablecars, trains, ferries = count_vehicles_on_screen(df, DATE, FRAMES)

    # ### Save vehicle counts to csv (3600 frame version)
    # Our Processing sketch has 3,600 frames (at 60 frames per second makes
    # a one minute video). One day has 5,760 15-second intervals. So to make
    # things easy we will select the vehicle counts at 3,600 of the 15-second
    # intervals throughout the day. We will select them randomly, but will
    # maintain chronological order by sorting and also consistency between
    # vehicle types by using a consitent set of random indices to select
    # counts for different vehicle types.

    random_indices = np.sort(np.random.choice(vehicles.index, int(FRAMES), replace=False))

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
    if not os.path.exists("sketches/{}/{}/data/vehicle_counts".format(OUTPUT_NAME, DATE)):
        os.makedirs("sketches/{}/{}/data/vehicle_counts".format(OUTPUT_NAME, DATE))
    vehicles_counts_output.to_csv("sketches/{}/{}/data/vehicle_counts/vehicles_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))
    buses_counts_output.to_csv("sketches/{}/{}/data/vehicle_counts/buses_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))
    trams_counts_output.to_csv("sketches/{}/{}/data/vehicle_counts/trams_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))
    metros_counts_output.to_csv("sketches/{}/{}/data/vehicle_counts/metros_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))
    cablecars_counts_output.to_csv("sketches/{}/{}/data/vehicle_counts/cablecars_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))
    trains_counts_output.to_csv("sketches/{}/{}/data/vehicle_counts/trains_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))
    ferries_counts_output.to_csv("sketches/{}/{}/data/vehicle_counts/ferries_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))

    # Hacky way to center the sketch
    if not args.bbox:
        south, west, north, east = df['start_lat'][0], df['start_lon'][0], df['start_lat'][1], df['start_lon'][1]

    ## Use processing sketch template to create processing sketch file
    module_path = os.path.join(os.path.dirname(__file__))
    template_path = os.path.join(module_path, 'templates', 'template.pde')
    with open(template_path) as f:
        data = f.read()
    s = Template(data)

    if not os.path.exists("sketches/{}/{}/sketch".format(OUTPUT_NAME, DATE)):
        os.makedirs("sketches/{}/{}/sketch".format(OUTPUT_NAME, DATE))

    for asset in ['calendar_icon.png', 'clock_icon.png']:
      shutil.copyfile(
        os.path.join(module_path, 'assets', asset),
        os.path.join('sketches', OUTPUT_NAME, DATE, "sketch", asset)
      )

    with open("sketches/{}/{}/sketch/sketch.pde".format(OUTPUT_NAME, DATE), "w") as f:
        f.write(
            s.substitute(
                DIRECTORY_NAME=OUTPUT_NAME,
                DATE=DATE,
                TOTAL_FRAMES=FRAMES,
                RECORDING=str(RECORDING).lower(),
                AVG_LAT=(float(south) + float(north))/2.0,
                AVG_LON=(float(west) + float(east))/2.0
            )
        )

    timer_finish = dt.datetime.now()
    time_delta = timer_finish - timer_start
    print "Time elapsed: ", str(time_delta)
