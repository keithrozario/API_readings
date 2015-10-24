import urllib2
from urllib2 import urlopen, URLError
from urllib2 import HTTPError
from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

#Get value of each column
#added custom code to strip "MASA/TIME" from header value to just give out the time
def getHeaders(tr):
        cols = tr.findAll('td')
        for index, column in enumerate(cols):
                cols[index] = strip_html(str(column)).replace("MASA/TIME","")
        return cols

def strip_html(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data() #strip all HTML from the data

def create_url_list():
    met_dept_api_url_list = []
    met_dept_api_url_list.append("http://apims.doe.gov.my/v2/hour1_")
    met_dept_api_url_list.append("http://apims.doe.gov.my/v2/hour2_")
    met_dept_api_url_list.append("http://apims.doe.gov.my/v2/hour3_")
    met_dept_api_url_list.append("http://apims.doe.gov.my/v2/hour4_")
    return met_dept_api_url_list

def get_html(url_list,current_url_date):    

    webpage_htmls = []
    for url in url_list:
                    
        current_url_being_read = url + str(current_url_date) + ".html"
        print '@@@@@' + str(current_url_date) + '@@@@@'
        print current_url_being_read

        #attempt to open the webpage of the current URL
        try:
            API_HTML = urllib2.urlopen(current_url_being_read, timeout=30)
            webpage_htmls.append(API_HTML)
        except URLError, e:
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
            return None
        except :
            print 'Unknown Error Occured'
            return None

    return webpage_htmls
