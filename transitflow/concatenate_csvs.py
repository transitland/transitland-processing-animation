import pandas as pd
import glob
import os
import argparse
import math
import datetime as dt
import numpy as np

def concatenate_csvs(path):
    all_files = glob.glob(os.path.join(path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent
    df_from_each_file = (pd.read_csv(f) for f in all_files) # generators
    concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)
    del concatenated_df['Unnamed: 0'] # delete the blank column that gets added
    concatenated_df['start_time'] = pd.to_datetime(concatenated_df['start_time'])
    concatenated_df['end_time'] = pd.to_datetime(concatenated_df['end_time'])
    concatenated_df = concatenated_df.sort_values(by="start_time").reset_index(drop=True)
    return concatenated_df

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Animation day")
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
      "--clip_to_bbox",
      help="Clip trips to bounding box",
      action="store_true"
    )
    parser.add_argument(
      "--frames",
      help="Number of frames in animation. 3600 frames = 60 second animation.",
      default=3600
    )
    args = parser.parse_args()

    if not args.date:
      raise Exception('date required')

    if not args.apikey:
      raise Exception('api key required')

    MAPZEN_APIKEY = args.apikey
    OUTPUT_NAME = args.name
    DATE = args.date
    south, west, north, east = 0, 0, 0, 0 #null island!
    FRAMES = args.frames

    print ""
    print "INPUTS:"
    print "date: ", DATE
    print "name: ", OUTPUT_NAME
    print "API key: ", MAPZEN_APIKEY

    if args.bbox:
        south, west, north, east = args.bbox.split(",")
        # west, south, east, north = args.bbox.split(",")
        # bbox = true

    df = concatenate_csvs("data/{}/{}/indiv_operators".format(OUTPUT_NAME, DATE))

    print "Calculating trip segment bearings."
    df['bearing'] = df.apply(lambda row: calc_bearing_between_points(row['start_lat'], row['start_lon'], row['end_lat'], row['end_lon']), axis=1)

    if args.bbox and args.clip_to_bbox:
        df = df[
            ((df['start_lat'] >= float(south)) & (df['start_lat'] <= float(north)) & (df['start_lon'] >= float(west)) & (df['start_lon'] <= float(east))) |
            ((df['end_lat'] >= float(south)) & (df['end_lat'] <= float(north)) & (df['end_lon'] >= float(west)) & (df['end_lon'] <= float(east)))
        ]

    # Save to csv.
    df.to_csv("data/{}/{}/output.csv".format(OUTPUT_NAME, DATE))
    print "Total rows: ", df.shape[0]

    print "Counting number of vehicles in transit."
    vehicles, buses, trams, metros, cablecars, trains, ferries = count_vehicles_on_screen(df, DATE)

    # ### Save vehicle counts to csv (3600 frame version)
    # Our Processing sketch has 3,600 frames (at 60 frames per second makes
    # a one minute video). One day has 5,760 15-second intervals. So to make
    # things easy we will select the vehicle counts at 3,600 of the 15-second
    # intervals throughout the day. We will select them randomly, but will
    # maintain chronological order by sorting and also consistency between
    # vehicle types by using a consitent set of random indices to select
    # counts for different vehicle types.

    random_indices = np.sort(np.random.choice(vehicles.index, FRAMES, replace=False))

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
    if not os.path.exists("data/{}/{}/vehicle_counts".format(OUTPUT_NAME, DATE)):
        os.makedirs("data/{}/{}/vehicle_counts".format(OUTPUT_NAME, DATE))
    vehicles_counts_output.to_csv("data/{}/{}/vehicle_counts/vehicles_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))
    buses_counts_output.to_csv("data/{}/{}/vehicle_counts/buses_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))
    trams_counts_output.to_csv("data/{}/{}/vehicle_counts/trams_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))
    metros_counts_output.to_csv("data/{}/{}/vehicle_counts/metros_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))
    cablecars_counts_output.to_csv("data/{}/{}/vehicle_counts/cablecars_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))
    trains_counts_output.to_csv("data/{}/{}/vehicle_counts/trains_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))
    ferries_counts_output.to_csv("data/{}/{}/vehicle_counts/ferries_{}.csv".format(OUTPUT_NAME, DATE, FRAMES))
