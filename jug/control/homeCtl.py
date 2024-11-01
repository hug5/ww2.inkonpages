# import logging
# logger = logging.getLogger(__name__)

from jug.lib.logger import logger
from flask import render_template
# from jug.lib.f import F
# import random
from jug.lib.gLib import G



class HomeCtl():

    def __init__(self):
        self.config = {}
        self.html = None

    def getHtml(self):
        return self.html

    def getConfig(self):
        # Called by router to set page title;
        return self.config

    def doConfig(self):




        # A tuple ternary operator;
        # x = (False, True)[condition]
        # If there is a tagline, then combine name with tagline; otherwise, just stie name;
        # site_title = ({'site_title' : f"{G.site['name']}"}, {'site_keywords' : f"{G.site['keyname']} | {G.site['tagline']}"}) [ G.site['tagline'] != "" ]
        site_title = (f"{G.site['name']}", f"{G.site['name']} | {G.site['tagline']}") [ G.site['tagline'] != "" ]

        self.config = {
            'site_title' : site_title,
            'site_keywords' : "contact us, email, " + G.site["keywords"],
        }

    def doHome(self):
        from datetime import date
        today = date.today().strftime("%A, %b. %d, %Y")
          # there datetime.datetime, datetime.date, datetime.time, datetime.timedelta, tzinfo;
          # datetime may be a combination of date/time;
          # date is just date;

        self.doConfig()

        self.html = render_template(
            "homeHtml.jinja",
            today = today,
        )

