from bottle import Bottle

class WebServer(Bottle):
    def __init__(self):
        super(WebServer, self).__init__()
        self.route('/', callback=self.index)

    def index(self):
        with open("traffic-heat-map.html", "r") as html:
            return html.read()

app = WebServer()
app.run(host='0.0.0.0', port=80)
