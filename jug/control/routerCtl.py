from jug.lib.logger import logger
  # need to import the logger variable;

from flask import Flask, \
                  render_template, \
                  redirect, \
                  request

import tomli
# from jug.dbo import dbc
# from jug.lib.f import F
from jug.lib.g import G
from pathlib import Path
# import re


# import json
# from json import dumps
# from werkzeug.routing import Request
# from werkzeug.wrappers import Request, Response
# from werkzeug.test import create_environ


class RouterCtl():

    def __init__(self):

        dir_html = "../html"

        self.jug = Flask(
            __name__,
            template_folder=dir_html,
        )

        # self.jug.debug = True

        self.article = ''
        self.header = ''
        self.footer = ''

        self.doConfig_toml()

    def doConfig_toml(self):
        try:

            config_toml_path = Path("jug/conf/config.toml")
            if not Path(config_toml_path).is_file():
                raise FileNotFoundError(f"File Not Found: {config_toml_path}.")

            with config_toml_path.open(mode='rb') as file_toml:
                config_toml = tomli.load(file_toml)
                # If bad, should give FileNotFoundError

            G.site["name"] = config_toml["site"]["name"]
            G.site["tagline"] = config_toml["site"]["tagline"]

            G.site["logo_title"] = config_toml["site"]["logo_title"]
            G.site["description"] = config_toml["site"]["description"]
            G.site["keywords"] = config_toml["site"]["keywords"]
            G.site["time_zone"] = config_toml["site"]["time_zone"]
            G.site["time_zone_name"] = config_toml["site"]["time_zone_name"]
            G.site["time_zone_mail"] = config_toml["site"]["time_zone_mail"]
            G.site["time_zone_mail_name"] = config_toml["site"]["time_zone_mail_name"]
            G.site["amazon_tag"] = config_toml["site"]["amazon_tag"]

            G.contact["email"] = config_toml["contact"]["email"]
            G.contact["email_name"] = config_toml["contact"]["email_name"]
            G.contact["bounce_email"] = config_toml["contact"]["bounce_email"]

            G.db["un"] = config_toml["db"]["un"]
            G.db["pw"] = config_toml["db"]["pw"]
            G.db["host"] = config_toml["db"]["host"]
            G.db["port"] = config_toml["db"]["port"]
            G.db["database"] = config_toml["db"]["database"]


        except FileNotFoundError as e:
            logger.exception(f"config.toml Load Error: {e}")
        except Exception as e:
            logger.exception(f"doConfig_toml Error: {e}")
        finally:
            # logger.info(f'weatherAPI_key: {G["weatherAPI_key"]}')
            # logger.info(f'weatherAPI_key: {G.api["weatherAPI_key"]}')
            pass


    def doCommon(self):
        from jug.control.headerCtl import HeaderCtl
        from jug.control.footerCtl import FooterCtl

        logger.info('doCommon')

        cfDict = {
            "base_url" : request.url_root,
            "bestseller_url" : "/rank/bestseller/fiction/",
            "contact_url" : "/contact/",
            "link" : "https://hmso.inkonpages.com/book/theswines/"
        }

        # do Header
        headerOb = HeaderCtl()
        headerOb.start(cfDict)
        self.header = headerOb.getHtml()

        # do Footer
        footerOb = FooterCtl()
        footerOb.start(cfDict)
        self.footer = footerOb.getHtml()


        # pass


    def doHome(self):
        from jug.control.homeCtl import HomeCtl
        logger.info('DoHome')

        self.doCommon()

        homeOb = HomeCtl()
        homeOb.start()
        self.article = homeOb.getHtml()

        site_title = homeOb.getConfig()["site_title"]

        base_url = request.url_root

        pageHtml = render_template(
            "pageHtml.jinja",
            title = site_title,
            header = self.header,
            article = self.article,
            footer = self.footer,
            base_url = base_url
        )

        # return F.stripJinjaWhiteSpace(pageHtml)
        return pageHtml




    ##
        # def doSomePathUrl(self, url):
        #     from jug.control import pathCtl

        #     logger.info('DoSomePathUrl')

        #     self.doCommon()

        #     pathO = pathCtl.PathCtl(url)
        #     self.article = pathO.doStart()
        #     site_title = pathO.getConfig()["site_title"]


        #     pageHtml = render_template(
        #         "pageHtml.jinja",
        #         title = site_title,
        #         header = self.header,
        #         article = self.article,
        #         footer = self.footer,
        #     )

        #     return F.stripJinjaWhiteSpace(pageHtml) + self.logo

        # def doCheckBadPath(self, url):

        #     # Doing this for aesthetic; don't want a path that is /home, /paperdrift or /station paperdrift
        #     # Also check that all paths end with trailing slash;

        #     # checkPath = ''
        #       # Dilemma: don't want to make this variable global;
        #       # But also want to be able to use within local functions below;
        #       # So declare here; and assign as nonlocal within local functions?

        #     def check_path_url():
        #         # Check for certain paths we ant to avoid; assign to home if so;

        #         # nonlocal url  # avoid unbound variable error;

        #         # If url path is any of these, then go home;
        #         home_list = ["home", "paperdrift", "station paperdrift"]
        #         url2 = url.lower()

        #         # check for home or paperdrift in url; if so, go to root url;
        #         url3 = url2.rstrip('/')
        #         # if url3 in home_list: return "/"
        #         if url3 in home_list:
        #             return "/"
        #         else:
        #             return False
        #         # Should also return false implicitly


        #     def check_trailing_slash():
        #         # Check there is trailing slash in paths;
        #         # nonlocal checkPath
        #         # nonlocal url

        #         # check that url ends in /
        #         checkPath = F.checkPathSlash(url)
        #         # if checkPath != True: return checkPath
        #         # if not checkPath:
        #         if checkPath:
        #             return checkPath
        #         else:
        #             return False
        #         # Should also return false implicitly

        #     def cleanUrl():
        #         # nonlocal url
        #         url2 = url.rstrip('/')

        #         # remove non-alphanumeric characters, but allow for space
        #         # all bad characters will be replaced with space;
        #         # then later we'll remove redundant spaces;
        #         new_url = re.sub(r'[^a-zA-Z0-9\- ]', ' ', url2)
        #         # new_url2 = new_url.replace("  ", " ")
        #         # new_url = new_url.replace("%20%%20", "x")
        #         # new_url = new_url.replace("%20", "x")
        #         # new_url = new_url.replace("20%", "x")
        #         # new_url = new_url.replace("%", "x")
        #           # This doesn't seem to work right... always some edge problem;
        #           # When you ahve a weird url like this:
        #           # https://station.paperdrift.com/busan%20%20%20%%20%20korea/
        #           # I think the server crashes before it even gets here;
        #           # Weird... not the %20 isn't showing up!

        #         # remove redundant spaces
        #         new_url2 = ' '.join(new_url.split())

        #         # Don't need to escape since we removed all bad characters;
        #         # escaped_url = F.hesc(new_url)

        #         if new_url2 != url2:
        #             logger.info(f'Cleaned url: {new_url2} : {url2}')
        #             return "/" + new_url2 + "/"
        #         else:
        #             # logger.info(f'good url: {escaped_url}')
        #             logger.info(f'Good url: {new_url2}')
        #             return False


        #         # clean_text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
        #         # print(clean_text)


        #     # if check_trailing_slash():
        #     checkPath = check_trailing_slash()
        #     if checkPath: return checkPath

        #     # Check if url is clean
        #     result = cleanUrl()
        #     if result: return result

        #     # Check that the city name is not home, paperdrift, station paperdrift
        #     # if check_path_url(): return "/"
        #     path = check_path_url()
        #     if path: return path



        #     # If all good, return False; nothing to do;
        #     return False




    def doRequestUrl(self):
        # Assume this url:
        # https://station.paperdrift.com/something/?a=b

        rpath = request.url_root
        logger.info("---URL url_root: " + rpath)
          # https://station.paperdrift.com/

        rpath = request.base_url
        logger.info("---URL base_url: " + rpath)
            # https://station.paperdrift.com/something/

        rpath = request.url
        logger.info("---URL url: " + rpath)
          # https://station.paperdrift.com/something/?a=b

        rpath = request.full_path
        logger.info("---URL full_path: " + rpath)
          # /something/?a=b
          # /?   # will always have a ? on the index or other page ERRONESOUSLY;

        rpath = request.environ['PATH_INFO']
        logger.info("---URL PATH_INFO: " + rpath)
            # /something/

        rpath = request.environ['QUERY_STRING']
        logger.info("---URL QUERY_STRING: " + rpath)
          # a=b

        # These below give me the same IP address
        # rpath = request.remote_addr
        # logger.info("---Remote Address: " + rpath)
          # 84.239.5.141
        rpath = request.environ['REMOTE_ADDR']
        logger.info("---Remote Address2: " + rpath)
          # 84.239.5.141


        # This gives us the TRUE RAW uri; ? and // are always shown
        rpath = request.environ["REQUEST_URI"]
        logger.info("---uri: " + rpath)
          # /something/?a=b

        # print everything; check uwsgi_log
        # print(request.environ)

        # Also:
        # logger.debug, logger.info, logger.warning, logger.error, logger.critical


    def checkTrailingQuestion(self):

        # check for /?/ and /??+ path (2 or more question marks);
        ch_qmark = request.full_path
        if ch_qmark == "/?/" or ch_qmark.find("/??") >= 0 :
            return False # Not okay; redirect

        return True # okay


    def doRoute(self):

        @self.jug.before_request
        def before_request_route():

            logger.info("---before_request_route")

            self.doRequestUrl()

            if not self.checkTrailingQuestion():
                rpath = request.base_url
                return redirect(rpath, code=301)


        @self.jug.route('/')
        def home():
            logger.info("---home()")
            # return "hello"
            return self.doHome()



        @self.jug.route('/contact/')
        @self.jug.route('/contact/<path:url>')
        def contact(url=""):
            if url:
                return redirect("/contact/", code=301)

            return "contact"


        @self.jug.route('/rank/')
        @self.jug.route('/rank/bestseller/')
        def rank_bad():
            return "rank bad"

        @self.jug.route('/rank/bestseller/fiction/')
        @self.jug.route('/rank/alltime/')
        def rank_good():
            return "rank good"


        @self.jug.route('/<path:url>')
        def bad_url(url):
            return redirect("/", code=301)



      # https://inkonpages.com/rank/bestseller/fiction/


        # @self.jug.route('/<path:url>')
        # def contact(url):

        #     # If return some value, then go to that given url
        #     # If return False, then the url is fine;
        #     result = self.doCheckBadPath(url)
        #     # So a good path will return False; anything else is bad path;
        #     # And we should redirect to the return value;
        #     if result: return redirect(result, code=301)

        #     # If path is good, then proceed normally;
        #     return self.doSomePathUrl(url)


      # https://inkonpages.com/rank/bestseller/fiction/
      # https://inkonpages.com/rank/bestseller/nonfiction/
      # https://inkonpages.com/rank/alltime/
      # https://inkonpages.com/contact/

      # @self.jug.route('/<path:url>')

      # path             /foo/page.html
      # full_path        /foo/page.html?x=y
      # script_root      /myapplication

      # url_root         http://www.example.com/myapplication/
      # base_url         http://www.example.com/myapplication/foo/page.html
      # url              http://www.example.com/myapplication/foo/page.html?x=y


    def start(self):
        self.doRoute()
        return self.jug



## These below don't work even when it appears to!
# method 1
# obj = Router()
# jug = obj.start()

# method 2
# jug = Router().start()
  # Can just shorten to 1 line like this;

# These 2 may be equivalent and allows for debug mode
# $ flask --app hello run --debug
# app.run(debug=True)

# But how to do this on a running remote server running uwsgi?

