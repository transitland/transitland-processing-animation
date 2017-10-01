/*
TransitFlow
https://github.com/transitland/transitland-processing-animation
Will Geary (@wgeary) for Mapzen, 2017

Attribution:
Juan Francisco Saldarriaga's workshop on Processing: https://github.com/juanfrans-courses/DataScienceSocietyWorkshop
Till Nagel's Unfolding Maps library: http://unfoldingmaps.org/
*/

////// MAIN INPUTS ///////
String directoryName = "${DIRECTORY_NAME}";
String date = "${DATE}";
String inputFile = "../data/output.csv";
int totalFrames = ${TOTAL_FRAMES};
Location center = new Location(${AVG_LAT}, ${AVG_LON});
Integer zoom_start = 9;
String date_format = "M/d/yy";
String day_format = "EEEE";
String time_format = "h:mm a";
boolean recording = ${RECORDING};
boolean HQ = false;
boolean rotateBearing = true;
//////////////////////////

// Import Unfolding Maps
import de.fhpotsdam.unfolding.*;
import de.fhpotsdam.unfolding.core.*;
import de.fhpotsdam.unfolding.data.*;
import de.fhpotsdam.unfolding.events.*;
import de.fhpotsdam.unfolding.geo.*;
import de.fhpotsdam.unfolding.interactions.*;
import de.fhpotsdam.unfolding.mapdisplay.*;
import de.fhpotsdam.unfolding.mapdisplay.shaders.*;
import de.fhpotsdam.unfolding.marker.*;
import de.fhpotsdam.unfolding.providers.*;
import de.fhpotsdam.unfolding.texture.*;
import de.fhpotsdam.unfolding.tiles.*;
import de.fhpotsdam.unfolding.ui.*;
import de.fhpotsdam.unfolding.utils.*;
import de.fhpotsdam.utils.*;

// Import some Java utilities
import java.util.Date;
import java.text.SimpleDateFormat;

// Import video export
import com.hamoid.*;
VideoExport videoExport;

// Declare Global Variables

UnfoldingMap map;

// Statistics input files (for stacked area chart)
String vehicleCountFile = "../data/vehicle_counts/vehicles_" + totalFrames + ".csv";
String busCountFile = "../data/vehicle_counts/buses_" + totalFrames + ".csv";
String tramCountFile = "../data/vehicle_counts/trams_" + totalFrames + ".csv";
String cablecarCountFile = "../data/vehicle_counts/cablecars_" + totalFrames + ".csv";
String metroCountFile = "../data/vehicle_counts/metros_" + totalFrames + ".csv";
String trainCountFile = "../data/vehicle_counts/trains_" + totalFrames + ".csv";
String ferryCountFile = "../data/vehicle_counts/ferries_" + totalFrames + ".csv";

int totalSeconds;
Table tripTable;

ArrayList<Trips> trips = new ArrayList<Trips>();
ArrayList<String> operators = new ArrayList<String>();
ArrayList<String> vehicle_types = new ArrayList<String>();
ArrayList<Float> bearings = new ArrayList<Float>();

Table vehicleCount;
IntList vehicleCounts;
int maxVehicleCount;
float hscale = float(totalFrames) / float(width)*0.12;

Table busCount;
ArrayList<Line> busLines = new ArrayList<Line>();
ArrayList<Integer> busFrames = new ArrayList<Integer>();
ArrayList<Integer> busCounts = new ArrayList<Integer>();
ArrayList<Float> busHeights = new ArrayList<Float>();

Table tramCount;
ArrayList<Line> tramLines = new ArrayList<Line>();
ArrayList<Integer> tramFrames = new ArrayList<Integer>();
ArrayList<Integer> tramCounts = new ArrayList<Integer>();
ArrayList<Float> tramHeights = new ArrayList<Float>();

Table metroCount;
ArrayList<Line> metroLines = new ArrayList<Line>();
ArrayList<Integer> metroFrames = new ArrayList<Integer>();
ArrayList<Integer> metroCounts = new ArrayList<Integer>();
ArrayList<Float> metroHeights = new ArrayList<Float>();

Table cablecarCount;
ArrayList<Line> cablecarLines = new ArrayList<Line>();
ArrayList<Integer> cablecarFrames = new ArrayList<Integer>();
ArrayList<Integer> cablecarCounts = new ArrayList<Integer>();
ArrayList<Float> cablecarHeights = new ArrayList<Float>();

Table trainCount;
ArrayList<Line> trainLines = new ArrayList<Line>();
ArrayList<Integer> trainFrames = new ArrayList<Integer>();
ArrayList<Integer> trainCounts = new ArrayList<Integer>();
ArrayList<Float> trainHeights = new ArrayList<Float>();

Table ferryCount;
ArrayList<Line> ferryLines = new ArrayList<Line>();
ArrayList<Integer> ferryFrames = new ArrayList<Integer>();
ArrayList<Integer> ferryCounts = new ArrayList<Integer>();
ArrayList<Float> ferryHeights = new ArrayList<Float>();
 
boolean bus_label = false;
boolean tram_label = false;
boolean metro_label = false;
boolean train_label = false;
boolean cablecar_label = false;
boolean ferry_label = false;

ScreenPosition startPos;
ScreenPosition endPos;
Location startLocation;
Location endLocation;
Date minDate;
Date maxDate;
Date startDate;
Date endDate;
Date thisStartDate;
Date thisEndDate;
PImage clock;
PImage calendar;
PImage airport;
PFont raleway;
PFont ralewayBold;
Integer screenfillalpha = 120;


Float firstLat;
Float firstLon;
color c;

// define date format of raw data
SimpleDateFormat myDateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
SimpleDateFormat hour = new SimpleDateFormat("h:mm a");
//SimpleDateFormat day = new SimpleDateFormat("MMMM dd, yyyy");
SimpleDateFormat weekday = new SimpleDateFormat("EEEE");

// Basemap providers
AbstractMapProvider provider1;
AbstractMapProvider provider2;
AbstractMapProvider provider3;
AbstractMapProvider provider4;
AbstractMapProvider provider5;
AbstractMapProvider provider6;
AbstractMapProvider provider7;
AbstractMapProvider provider8;
AbstractMapProvider provider9;
AbstractMapProvider provider0;
AbstractMapProvider providerq;
AbstractMapProvider providerw;
AbstractMapProvider providere;
AbstractMapProvider providerr;
AbstractMapProvider providert;
AbstractMapProvider providery;
AbstractMapProvider provideru;
AbstractMapProvider provideri;

String provider1Attrib;
String provider2Attrib;
String provider3Attrib;
String provider4Attrib;
String provider5Attrib;
String provider6Attrib;
String provider7Attrib;
String provider8Attrib;
String provider9Attrib;
String provider0Attrib;
String providerqAttrib;
String providerwAttrib;
String providereAttrib;
String providerrAttrib;
String providertAttrib;
String provideryAttrib;
String provideruAttrib;

boolean monday = false;
boolean tuesday = false;
boolean wednesday = false;
boolean thursday = false;
boolean friday = false;
boolean saturday = false;
boolean sunday = false;

String attrib;
Float attribWidth;

void setup() {
  size(1000, 800, P3D);
  //size(1000, 960, P3D);
  //fullScreen(P3D);

  provider1 = new StamenMapProvider.TonerLite();
  provider2 = new StamenMapProvider.TonerBackground();
  provider3 = new CartoDB.Positron();
  provider4 = new Microsoft.AerialProvider();
  provider5 = new OpenStreetMap.OpenStreetMapProvider();
  provider6 = new OpenStreetMap.OSMGrayProvider();
  provider7 = new EsriProvider.WorldStreetMap();
  provider8 = new EsriProvider.DeLorme();
  provider9 = new EsriProvider.WorldShadedRelief();
  provider0 = new EsriProvider.NatGeoWorldMap();
  providerq = new EsriProvider.OceanBasemap();
  providerw = new EsriProvider.WorldGrayCanvas();
  providere = new EsriProvider.WorldPhysical();
  providerr = new EsriProvider.WorldStreetMap();
  providert = new EsriProvider.WorldTerrain();
  providery = new EsriProvider.WorldTopoMap();
  provideru = new Google.GoogleMapProvider();

  provider1Attrib = "Stamen Design";
  provider2Attrib = "Stamen Design";
  provider3Attrib = "Carto";
  provider4Attrib = "Bing Maps";
  provider5Attrib = "OpenStreetMap";
  provider6Attrib = "OpenStreetMap";
  provider7Attrib = "ESRI";
  provider8Attrib = "ESRI";
  provider9Attrib = "ESRI";
  provider0Attrib = "ESRI";
  providerqAttrib = "ESRI";
  providerwAttrib = "ESRI";
  providereAttrib = "ESRI";
  providerrAttrib = "ESRI";
  providertAttrib = "ESRI";
  provideryAttrib = "ESRI";
  provideruAttrib = "Google Maps";

  smooth();

  loadData();

  map = new UnfoldingMap(this, provider1);
  MapUtils.createDefaultEventDispatcher(this, map);

  attrib = "© Mapzen | Transitland | Unfolding Maps | Basemap by " + provider1Attrib;
  attribWidth = textWidth(attrib);

  map.zoomAndPanTo(zoom_start, center);

  // Fonts and icons
  raleway  = createFont("Raleway-Heavy", 32);
  ralewayBold  = createFont("Raleway-Bold", 28);
  clock = loadImage("clock_icon.png");
  clock.resize(0, 35);
  calendar = loadImage("calendar_icon.png");
  calendar.resize(0, 35);

  videoExport = new VideoExport(this);
  videoExport.setFrameRate(60);
  if (recording == true) videoExport.startMovie();
}

float h_offset;

void loadData() {
  tripTable = loadTable(inputFile, "header");
  println(str(tripTable.getRowCount()) + " records loaded...");

  // calculate min start time and max end time (must be sorted ascending)
  String first = tripTable.getString(0, "start_time");
  String last = tripTable.getString(tripTable.getRowCount()-1, "end_time");

  println("Min departure time: ", first);
  println("Max departure time: ", last);

  try {
    minDate = myDateFormat.parse(first); //first "2017-07-17 9:59:00"
    maxDate = myDateFormat.parse(last); //last
    totalSeconds = int(maxDate.getTime()/1000) - int(minDate.getTime()/1000);
  }
  catch (Exception e) {
    println("Unable to parse date stamp");
  }
  println("Min starttime:", minDate, ". In epoch:", minDate.getTime()/1000);
  println("Max starttime:", maxDate, ". In epoch:", maxDate.getTime()/1000);
  println("Total seconds in dataset:", totalSeconds);
  println("Total frames:", totalFrames);

  firstLat = tripTable.getFloat(0, "start_lat");
  firstLon = tripTable.getFloat(0, "start_lon");

  for (TableRow row : tripTable.rows()) {
    String vehicle_type = row.getString("route_type");
    vehicle_types.add(vehicle_type);

    Float bearing = row.getFloat("bearing");
    bearings.add(bearing);

    int tripduration = row.getInt("duration");
    int duration = round(map(tripduration, 0, totalSeconds, 0, totalFrames));

    try {
      thisStartDate = myDateFormat.parse(row.getString("start_time"));
      thisEndDate = myDateFormat.parse(row.getString("end_time"));
    }
    catch (Exception e) {
      println("Unable to parse destination");
    }

    int startFrame = floor(map(thisStartDate.getTime()/1000, minDate.getTime()/1000, maxDate.getTime()/1000, 0, totalFrames));
    int endFrame = floor(map(thisEndDate.getTime()/1000, minDate.getTime()/1000, maxDate.getTime()/1000, 0, totalFrames));

    float startLat = row.getFloat("start_lat");
    float startLon = row.getFloat("start_lon");
    float endLat = row.getFloat("end_lat");
    float endLon = row.getFloat("end_lon");
    startLocation = new Location(startLat, startLon);
    endLocation = new Location(endLat, endLon);
    trips.add(new Trips(duration, startFrame, endFrame, startLocation, endLocation, bearing));
  }


  int lineAlpha = 80;
  // total vehicle counts
  vehicleCount = loadTable(vehicleCountFile, "header");
  vehicleCounts = new IntList();
  for (int i = 0; i < vehicleCount.getRowCount(); i++) {
    TableRow row = vehicleCount.getRow(i);
    int count = row.getInt("count");
    vehicleCounts.append(count);
  }
  maxVehicleCount = int(vehicleCounts.max());
  println("Max vehicles on road: " + maxVehicleCount);

  // maximum height of stacked bar chart in pixels
  int maxPixels = 140;

  // bus stacked bar
  busCount = loadTable(busCountFile, "header");
  for (int i = 0; i < busCount.getRowCount(); i++) {
    TableRow row = busCount.getRow(i);
    int frame = row.getInt("frame");
    int count = row.getInt("count");
    busFrames.add(frame);
    busCounts.add(count);
    float h = busCounts.get(i);
    c = color(0, 173, 253, lineAlpha);
    int xmargin = 50;
    int ymargin = 40;
    int xaxisoffset = 5;
    float lineHeight = map(h, 0, maxVehicleCount, 0, maxPixels);
    busHeights.add(lineHeight);
    Line line = new Line(xmargin + i/hscale, height-ymargin, xmargin + i/hscale, height-ymargin-lineHeight, c);
    busLines.add(line);
  }

  // tram stacked bar
  tramCount = loadTable(tramCountFile, "header");
  for (int i = 0; i < tramCount.getRowCount(); i++) {
    TableRow row = tramCount.getRow(i);
    int frame = row.getInt("frame");
    int count = row.getInt("count");
    tramFrames.add(frame);
    tramCounts.add(count);
    float h = tramCounts.get(i);
    float lineHeight = map(h, 0, maxVehicleCount, 0, maxPixels);
    tramHeights.add(lineHeight);
    h_offset = busHeights.get(i);
    c = color(124, 252, 0, lineAlpha);
    int xmargin = 50;
    int ymargin = 40;
    Line line = new Line(xmargin + i/hscale, height-ymargin-(h_offset), xmargin + i/hscale, height-ymargin-(lineHeight+h_offset), c);
    tramLines.add(line);
  }

  // Metro stacked bar
  metroCount = loadTable(metroCountFile, "header");
  for (int i = 0; i < metroCount.getRowCount(); i++) {
    TableRow row = metroCount.getRow(i);
    int frame = row.getInt("frame");
    int count = row.getInt("count");
    metroFrames.add(frame);
    metroCounts.add(count);
    float h = metroCounts.get(i);
    float lineHeight = map(h, 0, maxVehicleCount, 0, maxPixels);
    metroHeights.add(lineHeight);
    h_offset = busHeights.get(i) + tramHeights.get(i);
    c = color(255, 0, 0, lineAlpha);
    int xmargin = 50;
    int ymargin = 40;
    Line line = new Line(xmargin + i/hscale, height-ymargin-(h_offset), xmargin + i/hscale, height-ymargin-(lineHeight+h_offset), c);
    metroLines.add(line);
  }

  // Train stacked bar
  trainCount = loadTable(trainCountFile, "header");
  for (int i = 0; i < trainCount.getRowCount(); i++) {
    TableRow row = trainCount.getRow(i);
    int frame = row.getInt("frame");
    int count = row.getInt("count");
    trainFrames.add(frame);
    trainCounts.add(count);
    float h = trainCounts.get(i);
    float lineHeight = map(h, 0, maxVehicleCount, 0, maxPixels);
    trainHeights.add(lineHeight);
    h_offset = busHeights.get(i)+ tramHeights.get(i)+ metroHeights.get(i);
    c = color(255, 215, 0, lineAlpha);
    int xmargin = 50;
    int ymargin = 40;
    Line line = new Line(xmargin + i/hscale, height-ymargin-(h_offset), xmargin + i/hscale, height-ymargin-(lineHeight+h_offset), c);
    trainLines.add(line);
  }

  // Cablecar stacked bar
  cablecarCount = loadTable(cablecarCountFile, "header");
  for (int i = 0; i < cablecarCount.getRowCount(); i++) {
    TableRow row = cablecarCount.getRow(i);
    int frame = row.getInt("frame");
    int count = row.getInt("count");
    cablecarFrames.add(frame);
    cablecarCounts.add(count);
    float h = cablecarCounts.get(i);
    float lineHeight = map(h, 0, maxVehicleCount, 0, maxPixels);
    cablecarHeights.add(lineHeight);
    h_offset = busHeights.get(i) + tramHeights.get(i) + metroHeights.get(i) + trainHeights.get(i);
    c = color(255,140,0, lineAlpha);
    int xmargin = 50;
    int ymargin = 40;
    Line line = new Line(xmargin + i/hscale, height-ymargin-(h_offset), xmargin + i/hscale, height-ymargin-(lineHeight+h_offset), c);
    cablecarLines.add(line);
  }

  // Ferry stacked bar
  ferryCount = loadTable(ferryCountFile, "header");
  for (int i = 0; i < ferryCount.getRowCount(); i++) {
    TableRow row = ferryCount.getRow(i);
    int frame = row.getInt("frame");
    int count = row.getInt("count");
    ferryFrames.add(frame);
    ferryCounts.add(count);
    float h = ferryCounts.get(i);
    float lineHeight = map(h, 0, maxVehicleCount, 0, maxPixels);
    ferryHeights.add(lineHeight);
    h_offset = busHeights.get(i) + tramHeights.get(i) + metroHeights.get(i) + cablecarHeights.get(i) + trainHeights.get(i);
    c = color(255, 105, 180, lineAlpha);
    int xmargin = 50;
    int ymargin = 40;
    Line line = new Line(xmargin + i/hscale, height-ymargin-(h_offset), xmargin + i/hscale, height-ymargin-(lineHeight+h_offset), c);
    ferryLines.add(line);
  }
}

void draw() {

  if (frameCount < totalFrames) {
    map.draw();
    noStroke();
    fill(0, screenfillalpha);
    rect(0, 0, width, height);

    // draw stacked bar chart with a bunch of skinny lines
    for (int i = 0; i < frameCount; i++) {
      Line busLine = busLines.get(i);
      busLine.plot();

      Line trainLine = trainLines.get(i);
      trainLine.plot();

      Line tramLine = tramLines.get(i);
      tramLine.plot();

      Line metroLine = metroLines.get(i);
      metroLine.plot();

      Line cablecarLine = cablecarLines.get(i);
      cablecarLine.plot();

      Line ferryLine = ferryLines.get(i);
      ferryLine.plot();
    }

    // handle time
    float epoch_float = map(frameCount, 0, totalFrames, int(minDate.getTime()/1000), int(maxDate.getTime()/1000));
    int epoch = int(epoch_float);

    String date = new java.text.SimpleDateFormat(date_format).format(new java.util.Date(epoch * 1000L));
    String day = new java.text.SimpleDateFormat(day_format).format(new java.util.Date(epoch * 1000L));
    String time = new java.text.SimpleDateFormat(time_format).format(new java.util.Date(epoch * 1000L));

    // draw labels
    textFont(ralewayBold, 12);
    int xmargin = 60;
    int ymargin = 40;

    //fill(255, 255, 255);

    int h_bus = busCounts.get(frameCount);
    int h_tram = tramCounts.get(frameCount);
    int h_metro = metroCounts.get(frameCount);
    int h_train = trainCounts.get(frameCount);
    int h_cablecar = cablecarCounts.get(frameCount);
    int h_ferry = ferryCounts.get(frameCount);
    
    int ymargin_adjust = 30;
    
    if (h_bus != 0 || bus_label == true) ymargin_adjust = ymargin_adjust + 15;
    if (h_tram != 0 || tram_label == true) ymargin_adjust = ymargin_adjust + 15;
    if (h_metro != 0 || metro_label == true) ymargin_adjust = ymargin_adjust + 15;
    if (h_train != 0 || train_label == true) ymargin_adjust = ymargin_adjust + 15;
    if (h_cablecar != 0 || cablecar_label == true) ymargin_adjust = ymargin_adjust + 15;
    if (h_ferry != 0 || ferry_label == true) ymargin_adjust = ymargin_adjust + 15;

    fill(0,150);
    noStroke();
    rect(xmargin + frameCount/hscale-5, height-ymargin - ymargin_adjust, 110, ymargin_adjust + 15, 7);
    fill(150, 220);
    rect(width-(attribWidth+10), height-18, (attribWidth+10), 18, 3);
    c = color(255,255,255,255);
    strokeWeight(1);
    stroke(c);
    line(xmargin + frameCount/hscale, height-ymargin-24, xmargin + frameCount/hscale+100, height-ymargin-24);

    noStroke();

    ymargin_adjust = ymargin_adjust - 15;

    if (h_bus != 0 || bus_label == true) {
      fill(0, 173, 253, 255);
      text("Buses: ", xmargin + frameCount/hscale, height - ymargin - ymargin_adjust);
      textAlign(RIGHT);
      text(nfc(h_bus), xmargin + frameCount/hscale + 100, height - ymargin - ymargin_adjust);
      textAlign(LEFT);
      ymargin_adjust = ymargin_adjust - 15;
      bus_label = true;
    }

    if (h_tram != 0 || tram_label == true) {
      fill(124, 252, 0, 255);
      text("Light Rail: ", xmargin + frameCount/hscale, height-ymargin - ymargin_adjust);
      textAlign(RIGHT);
      text(h_tram, xmargin + frameCount/hscale + 100, height-ymargin - ymargin_adjust);
      textAlign(LEFT);
      ymargin_adjust = ymargin_adjust - 15;
      tram_label = true;
    }

    if (h_metro != 0 || metro_label == true) {
      fill(255,51,51, 255);
      text("Subways: ", xmargin + frameCount/hscale, height-ymargin - ymargin_adjust);
      textAlign(RIGHT);
      text(h_metro, xmargin + frameCount/hscale + 100, height-ymargin - ymargin_adjust);
      textAlign(LEFT);
      ymargin_adjust = ymargin_adjust - 15;
      metro_label = true;
    }

    if (h_train != 0 || train_label == true) {
      fill(255, 215, 0, 255);
      text("Trains: ", xmargin + frameCount/hscale, height-ymargin - ymargin_adjust);
      textAlign(RIGHT);
      text(h_train, xmargin + frameCount/hscale + 100, height-ymargin - ymargin_adjust);
      textAlign(LEFT);
      ymargin_adjust = ymargin_adjust - 15;
      train_label = true;
    }

    if (h_cablecar != 0 || cablecar_label == true) {
      fill(255,140,0, 255);
      text("Cable Cars: ", xmargin + frameCount/hscale, height-ymargin - ymargin_adjust);
      textAlign(RIGHT);
      text(h_cablecar, xmargin + frameCount/hscale + 100, height-ymargin - ymargin_adjust);
      textAlign(LEFT);
      ymargin_adjust = ymargin_adjust - 15;
      cablecar_label = true;
    }
    
    if (h_ferry != 0 || ferry_label == true) {
      fill(255, 105, 180, 255);
      text("Ferries: ", xmargin + frameCount/hscale, height-ymargin - ymargin_adjust);
      textAlign(RIGHT);
      text(h_ferry, xmargin + frameCount/hscale + 100, height-ymargin - ymargin_adjust);
      textAlign(LEFT);
      ymargin_adjust = ymargin_adjust - 15;
      ferry_label = true;
    }

    fill(255);
    text("Total: ", xmargin + frameCount/hscale, height-ymargin-10);
    textAlign(RIGHT);
    text(nfc(h_bus + h_train + h_tram + h_metro + h_cablecar + h_ferry), xmargin + frameCount/hscale + 100, height-ymargin-10);
    textAlign(LEFT);

    if (day.equals("Monday")) monday = true;
    if (day.equals("Tuesday")) tuesday = true;
    if (day.equals("Wednesday")) wednesday = true;
    if (day.equals("Thursday")) thursday = true;
    if (day.equals("Friday")) friday = true;
    if (day.equals("Saturday")) saturday = true;
    if (day.equals("Sunday")) sunday = true;

    int xlabeloffset = 15;
    //int xlabeldist = 120;
    int xlabelmargin = 50;

    fill(255);
    if (monday == true) text("Monday", xlabelmargin, height-xlabeloffset);

    text(time, xmargin + frameCount/hscale, height - xlabeloffset-15);
    // X axis
    rect(xmargin-10, height-xlabeloffset-20, frameCount/hscale, 1);

    textFont(ralewayBold, 14);
    text("Number of Transit Vehicles in Motion", xlabelmargin, height-xlabeloffset-170);

    fill(0, screenfillalpha);

    // draw trips
    noStroke();
    for (int i=0; i < trips.size(); i++) {

      Trips trip = trips.get(i);
      String vehicle_type = vehicle_types.get(i);

      switch(vehicle_type) {
      case "bus":
        c = color(0, 173, 253);
        fill(c, 240);
        trip.plotBus();
        break;
      case "bus_service":
        c = color(0, 173, 253);
        fill(c, 240);
        trip.plotBus();
        break;
      case("tram"):
        c = color(124, 252, 0);
        fill(c, 245);
        trip.plotTram();
        break;
      case("metro"):
        c = color(255, 0, 0);
        fill(c, 245);
        trip.plotSubway();
        break;
      case("rail"):
        c = color(255, 215, 0);
        fill(c, 200);
        trip.plotTrain();
        break;
      case("ferry"):
        c = color(255, 105, 180);
        fill(c, 200);
        trip.plotFerry();
        break;
      case("cablecar"):
        c = color(255,140,0);
        fill(c, 200);
        trip.plotRide();
      case("gondola"):
        c = color(255, 127, 80);
        fill(c, 200);
        trip.plotRide();
      case("funicular"):
        c = color(0, 173, 253);
        fill(c, 255);
        trip.plotRide();
      }
    }
    // Time and icons
    textSize(32);
    fill(255, 255, 255, 255);
    image(clock, 30, 25);
    stroke(255, 255, 255, 255);
    line(30, 70, 210, 70);
    image(calendar, 30, 80 );

    textFont(raleway);
    noStroke();
    text(time, 75, 55);
    textFont(ralewayBold);
    text(day, 75, 107);

    textSize(16);
    text(date, 75, 128);

    textSize(12);
    text(attrib, width-(attribWidth+5), height-5);

    if (recording == true) {
      if (frameCount < totalFrames) {
        if (HQ == true) {
          saveFrame("frames/######.tiff");
        } else if (HQ == false) {
          videoExport.saveFrame();
          return;
        }
      } else {
        if (HQ == true) exit();
        if (HQ == false) videoExport.endMovie();
        exit();
      }
    }
  }
}

void keyPressed() {
  if (key == '1') {
    map.mapDisplay.setProvider(provider1);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + provider1Attrib;
    attribWidth = textWidth(attrib);
  } else if (key == '2') {
    map.mapDisplay.setProvider(provider2);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + provider2Attrib;
    attribWidth = textWidth(attrib);
  } else if (key == '3') {
    map.mapDisplay.setProvider(provider3);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + provider3Attrib;
    attribWidth = textWidth(attrib);
  } else if (key == '4') {
    map.mapDisplay.setProvider(provider4);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + provider4Attrib;
    attribWidth = textWidth(attrib);
  } else if (key == '5') {
    map.mapDisplay.setProvider(provider5);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + provider5Attrib;
    attribWidth = textWidth(attrib);
  } else if (key == '6') {
    map.mapDisplay.setProvider(provider6);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + provider6Attrib;
    attribWidth = textWidth(attrib);
  } else if (key == '7') {
    map.mapDisplay.setProvider(provider7);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + provider7Attrib;
    attribWidth = textWidth(attrib);
  } else if (key == '8') {
    map.mapDisplay.setProvider(provider8);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + provider8Attrib;
    attribWidth = textWidth(attrib);
  } else if (key == '9') {
    map.mapDisplay.setProvider(provider9);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + provider9Attrib;
    attribWidth = textWidth(attrib);
  } else if (key == '0') {
    map.mapDisplay.setProvider(provider0);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + provider0Attrib;
    attribWidth = textWidth(attrib);
  } else if (key == 'q') {
    map.mapDisplay.setProvider(providerq);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + providerqAttrib;
    attribWidth = textWidth(attrib);
  } else if (key == 'w') {
    map.mapDisplay.setProvider(providerw);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + providerwAttrib;
    attribWidth = textWidth(attrib);
  } else if (key == 'e') {
    map.mapDisplay.setProvider(providere);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + providereAttrib;
    attribWidth = textWidth(attrib);
  } else if (key == 'r') {
    map.mapDisplay.setProvider(providerr);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + providerrAttrib;
    attribWidth = textWidth(attrib);
  } else if (key == 't') {
    map.mapDisplay.setProvider(providert);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + providertAttrib;
    attribWidth = textWidth(attrib);
  } else if (key == 'y') {
    map.mapDisplay.setProvider(providery);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + provideryAttrib;
    attribWidth = textWidth(attrib);
  } else if (key == 'u') {
    map.mapDisplay.setProvider(provideru);
    attrib = "© Mapzen | Transitland | Unfolding Maps | " + provideruAttrib;
    attribWidth = textWidth(attrib);
  }
}

class Line {
  float startx, starty, endx, endy;
  color c;
  Line(float _startx, float _starty, float _endx, float _endy, color _c) {
    startx = _startx;
    starty = _starty;
    endx = _endx;
    endy = _endy;
    c = _c;
  }
  void plot() {

    strokeWeight(0.5);
    stroke(c);
    line(startx, starty, endx, endy);
  }
}


class Trips {

 int tripFrames;
 int startFrame;
 int endFrame;
 Location start;
 Location end;
 Location currentLocation;
 ScreenPosition currentPosition;
 int s;
 float bearing;
 float radians;
 float xscale = 1.8;
 float yscale = 0.8;

 // class constructor
 Trips(int duration, int start_frame, int end_frame, Location startLocation, Location endLocation, float _bearing) {
       tripFrames = duration;
       startFrame = start_frame;
       endFrame = end_frame;
       start = startLocation;
       end = endLocation;
       bearing = _bearing;
       radians = radians(bearing);
     }

   // function to draw each trip
   void plotRide(){
     if (frameCount >= startFrame && frameCount < endFrame){
       float percentTravelled = (float(frameCount) - float(startFrame)) / float(tripFrames);

       currentLocation = new Location(

         lerp(start.x, end.x, percentTravelled),
         lerp(start.y, end.y, percentTravelled));

       currentPosition = map.getScreenPosition(currentLocation);

       // Zoom dependent ellipse size
       float z = map.getZoom();
       if (z <= 32.0){ s = 2;
       } else if (z == 64.0){ s = 2;
       } else if (z == 128.0){ s = 2;
       } else if (z == 256.0){ s = 3;
       } else if (z == 512.0){ s = 4;
       } else if (z == 1024.0){ s = 5;
       } else if (z == 2048.0){ s = 6;
       } else if (z == 4096.0){ s = 7;
       } else if (z == 8192.0){ s = 8;
       } else if (z >= 16384.0){ s = 10;
       }


       if (rotateBearing == false) ellipse(currentPosition.x, currentPosition.y, s, s);
       else {
         pushMatrix();
         pushStyle();
           translate(currentPosition.x, currentPosition.y);
           rotate(radians + PI/2);
           rectMode(CENTER);
           rect(0, 0, s*xscale, s*yscale, 7);
         popStyle();
         popMatrix();
       }
    }
  }

  void plotBus(){
     if (frameCount >= startFrame && frameCount < endFrame){
       float percentTravelled = (float(frameCount) - float(startFrame)) / float(tripFrames);

       currentLocation = new Location(

         lerp(start.x, end.x, percentTravelled),
         lerp(start.y, end.y, percentTravelled));

       currentPosition = map.getScreenPosition(currentLocation);

       // Zoom dependent ellipse size
       float z = map.getZoom();
       if (z <= 32.0){ s = 2;
       } else if (z == 64.0){ s = 2;
       } else if (z == 128.0){ s = 2;
       } else if (z == 256.0){ s = 3;
       } else if (z == 512.0){ s = 4;
       } else if (z == 1024.0){ s = 5;
       } else if (z == 2048.0){ s = 5;
       } else if (z == 4096.0){ s = 6;
       } else if (z == 8192.0){ s = 7;
       } else if (z >= 16384.0){ s = 9;
       }
       if (rotateBearing == false) ellipse(currentPosition.x, currentPosition.y, s, s);
       else {
         pushMatrix();
         pushStyle();
           translate(currentPosition.x, currentPosition.y);
           rotate(radians + PI/2);
           rectMode(CENTER);
           rect(0, 0, s*xscale, s*yscale, 7);
         popStyle();
         popMatrix();
       }
   }
  }

  void plotSubway(){
     if (frameCount >= startFrame && frameCount < endFrame){
       float percentTravelled = (float(frameCount) - float(startFrame)) / float(tripFrames);

       currentLocation = new Location(

         lerp(start.x, end.x, percentTravelled),
         lerp(start.y, end.y, percentTravelled));

       currentPosition = map.getScreenPosition(currentLocation);

       // Zoom dependent ellipse size
       float z = map.getZoom();
       if (z <= 32.0){ s = 3;
       } else if (z == 64.0){ s = 3;
       } else if (z == 128.0){ s = 3;
       } else if (z == 256.0){ s = 4;
       } else if (z == 512.0){ s = 5;
       } else if (z == 1024.0){ s = 7;
       } else if (z == 2048.0){ s = 8;
       } else if (z == 4096.0){ s = 9;
       } else if (z == 8192.0){ s = 10;
       } else if (z >= 16384.0){ s = 11;
       }

       if (rotateBearing == false) ellipse(currentPosition.x, currentPosition.y, s, s);
       else {
         pushMatrix();
         pushStyle();
           translate(currentPosition.x, currentPosition.y);
           rotate(radians + PI/2);
           rectMode(CENTER);
           rect(0, 0, s*xscale, s*yscale, 7);
         popStyle();
         popMatrix();
       }
   }
  }

  void plotTrain(){
     if (frameCount >= startFrame && frameCount < endFrame){
       float percentTravelled = (float(frameCount) - float(startFrame)) / float(tripFrames);

       currentLocation = new Location(

         lerp(start.x, end.x, percentTravelled),
         lerp(start.y, end.y, percentTravelled));

       currentPosition = map.getScreenPosition(currentLocation);

       // Zoom dependent ellipse size
       float z = map.getZoom();
       if (z <= 32.0){ s = 4;
       } else if (z == 64.0){ s = 4;
       } else if (z == 128.0){ s = 5;
       } else if (z == 256.0){ s = 6;
       } else if (z == 512.0){ s = 7;
       } else if (z == 1024.0){ s = 9;
       } else if (z == 2048.0){ s = 10;
       } else if (z == 4096.0){ s = 11;
       } else if (z == 8192.0){ s = 12;
       } else if (z >= 16384.0){ s = 13;
       }

       if (rotateBearing == false) ellipse(currentPosition.x, currentPosition.y, s, s);
       else {
         pushMatrix();
         pushStyle();
           translate(currentPosition.x, currentPosition.y);
           rotate(radians + PI/2);
           rectMode(CENTER);
           rect(0, 0, s*xscale, s*yscale, 7);
         popStyle();
         popMatrix();
       }
   }
  }

  void plotTram(){
     if (frameCount >= startFrame && frameCount < endFrame){
       float percentTravelled = (float(frameCount) - float(startFrame)) / float(tripFrames);

       currentLocation = new Location(

         lerp(start.x, end.x, percentTravelled),
         lerp(start.y, end.y, percentTravelled));

       currentPosition = map.getScreenPosition(currentLocation);

       // Zoom dependent ellipse size
       float z = map.getZoom();
       if (z <= 32.0){ s = 3;
       } else if (z == 64.0){ s = 3;
       } else if (z == 128.0){ s = 3;
       } else if (z == 256.0){ s = 4;
       } else if (z == 512.0){ s = 5;
       } else if (z == 1024.0){ s = 6;
       } else if (z == 2048.0){ s = 7;
       } else if (z == 4096.0){ s = 8;
       } else if (z == 8192.0){ s = 9;
       } else if (z >= 16384.0){ s = 10;
       }

       if (rotateBearing == false) ellipse(currentPosition.x, currentPosition.y, s, s);
       else {
         pushMatrix();
         pushStyle();
           translate(currentPosition.x, currentPosition.y);
           rotate(radians + PI/2);
           rectMode(CENTER);
           rect(0, 0, s*xscale, s*yscale, 7);
         popStyle();
         popMatrix();
       }
   }
  }

  void plotFerry(){
     if (frameCount >= startFrame && frameCount < endFrame){
       float percentTravelled = (float(frameCount) - float(startFrame)) / float(tripFrames);

       currentLocation = new Location(

         lerp(start.x, end.x, percentTravelled),
         lerp(start.y, end.y, percentTravelled));

       currentPosition = map.getScreenPosition(currentLocation);

       // Zoom dependent ellipse size
       float z = map.getZoom();
       if (z <= 32.0){ s = 3;
       } else if (z == 64.0){ s = 3;
       } else if (z == 128.0){ s = 3;
       } else if (z == 256.0){ s = 4;
       } else if (z == 512.0){ s = 5;
       } else if (z == 1024.0){ s = 6;
       } else if (z == 2048.0){ s = 7;
       } else if (z == 4096.0){ s = 8;
       } else if (z == 8192.0){ s = 9;
       } else if (z >= 16384.0){ s = 10;
       }

       if (rotateBearing == false) ellipse(currentPosition.x, currentPosition.y, s, s);
       else {
         pushMatrix();
         pushStyle();
           translate(currentPosition.x, currentPosition.y);
           rotate(radians + PI/2);
           rectMode(CENTER);
           rect(0, 0, s*xscale*0.8, s*yscale, 7);
         popStyle();
         popMatrix();
       }
   }
  }

}
