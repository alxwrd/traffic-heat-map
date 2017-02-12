import gmplot
from bottle import Bottle

class WebServer(Bottle):
    def __init__(self):
        super(WebServer, self).__init__()
        self.route('/', callback=self.index)

    def index(self):
        gmap = gmplot.GoogleMapPlotter(52.561928, -1.464854, 7)

        with open("traffic_data", "r") as f:
            points = f.readlines()

        heat_lats = []
        heat_lngs = []
        for point in points:
            lng, lat = point.split(",")
            heat_lngs.append(float(lng))
            heat_lats.append(float(lat))

        gmap.heatmap(heat_lats, heat_lngs)
        gmap.draw("traffic-heat-map.html")
        with open("traffic-heat-map.html", "r") as html:
            return html.read()

app = WebServer()
app.run(host='0.0.0.0', port=80)
