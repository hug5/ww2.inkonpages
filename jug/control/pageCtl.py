from jug.lib.logger import logger
from flask import render_template
from jug.lib.fLib import F
from jug.control.headerCtl import HeaderCtl
from jug.control.footerCtl import FooterCtl
from jug.lib.gLib import G

class PageCtl():

    def __init__(self):

        self.article = ''
        self.header = ''
        self.footer = ''
        self.ascii_art = ''
        self.html = ''
        self.site_title = ''
        self.site_keywords = ''

    def getHtml(self):
        return self.html

    def doHeader(self):
        Header = HeaderCtl()
        Header.doHeader()
        self.header = Header.getHtml()

    def doFooter(self):
        Footer = FooterCtl()
        Footer.doFooter()
        self.footer = Footer.getHtml()

    def doAscii_art(self):
        # Wrap with  () to do multiple lines
        self.ascii_art = ("<!-- \n" +
        "// [==]  👹 " + G.site["name"] + "  <o=o> //-->")

    def doHome(self):
        from jug.control.homeCtl import HomeCtl
        # F.uwsgi_log("doHome")
        logger.info('DoHome')

        Home = HomeCtl()
        Home.doHome()
        # Don't check for error; just proceed; catch it later;
        # if not G.sys.get("error"):
        self.article = Home.getHtml()
        self.site_title = Home.getConfig().get("site_title")
        self.site_keywords = Home.getConfig().get("site_keywords")
        # logger.info(f'---type info: {type(html)}')

    def doContact(self):
        from jug.control.contactCtl import ContactCtl
        logger.info('DoContact')

        Contact = ContactCtl()
        Contact.doContact()
        self.article = Contact.getHtml()
        self.site_title = Contact.getConfig().get("site_title")
        self.site_keywords = Contact.getConfig().get("site_keywords")


    def doPage(self, page):
        self.doHeader()
        self.doFooter()
        self.doAscii_art()

        if page == "home":
            self.doHome()
        elif page == "contact":
            self.doContact()
        else:
            G.sys["error"] = "redirect"
            G.sys["redirect"] = "/"

        if G.sys.get("error"): return

        html = render_template(
            "pageHtml.jinja",
            title = self.site_title,
            site_keywords = self.site_keywords,
            header = self.header,
            article = self.article,
            footer = self.footer,
        )

        logger.info(f'---type info: {type(html)}')
        self.html = F.stripJinja(html) + self.ascii_art
