#!/usr/bin/env python

import os
import gmplot
from trafficfeed import TrafficFeed


class Scraper(object):

    def __init__(self):
        #If the seen_items file doesn't exist, lets create it!
        writepath = "seen_items"
        if not os.path.exists(writepath):
            with open(writepath, "w") as f:
                pass

        #If the traffic_data file doesn't exist, lets create it!
        writepath = "traffic_data"
        if not os.path.exists(writepath):
            with open(writepath, "w") as f:
                pass


    def run(self):
        """Run the scrape
        """
        #Intiate the TrafficFeed object
        traffic = TrafficFeed(
            "http://m.highways.gov.uk/feeds/rss/UnplannedEvents.xml"
                             )

        #Load the traffic items from the feed
        items = traffic.items_within(9999,
                                     -1.464854,
                                     52.561928)
        #Get the items we have already seen
        seen = self.check_seen()

        for item in items:
            if item.find("guid").text not in seen:
                with open("traffic_data", "a") as f:
                    f.write(
                        "{}, {}\n".format(item.find("longitude").text,
                                          item.find("latitude").text)
                    )
                self.update_seen(item.find("guid").text)

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


    def update_seen(self, item_id):
        """Updates the seen_items

        Args:
            item_id (str): A unique identifier for the item.
        """
        with open("seen_items", "a+") as f:
            f.write(item_id + "\n")


    def check_seen(self):
        """Get the items from seen_items

        Returns:
            (list): A list of the items in seen_items
        """
        with open("seen_items", "r") as f:
            return f.read().splitlines()


if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()
