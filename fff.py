import scrapy
import npyscreen
from lxml import html
import urllib.request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
import logging
from cfonts import say


# logging.getLogger('scrapy').propagate = False


class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.TransparentThemeLightText)

        self.addForm("MAIN", MainForm, name="str(ass)")


class MainForm(npyscreen.NPSApp):
    def main(self):
        result = ''
        url = 'https://habr.com/ru/all/'
        request_html = urllib.request.urlopen(url)
        mybytes = request_html.read()
        req = mybytes.decode("utf8")
        request_html.close()

        tree = html.fromstring(req)
        link = tree.xpath('//*[@id]/article/h2/a/@href')
        text = tree.xpath('//*[@id]/article/h2/a/text()')
        articles = dict(zip(text, link))
        Options = npyscreen.OptionList()
        options = Options.options
        for





if __name__ == '__main__':
    TA = MainForm()
    TA.run()
