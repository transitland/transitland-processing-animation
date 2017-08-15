// Credits:
//
// This class builds off of Juan Francisco Saldarriaga's
// Citibike animation processing sketch:
// https://github.com/juanfrans-courses/DataScienceSocietyWorkshop
// 
// And integrates it with Unfolding Maps library
// Till Nagel, creator of the Unfolding Maps Library
// https://github.com/tillnagel/unfolding

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
       } else if (z == 256.0){ s = 2;
       } else if (z == 512.0){ s = 3;
       } else if (z == 1024.0){ s = 4;
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
}