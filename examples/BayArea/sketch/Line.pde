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