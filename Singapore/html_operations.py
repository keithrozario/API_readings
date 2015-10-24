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
        cols = tr.findAll('th')
        for index, column in enumerate(cols):
                cols[index] = strip_html(str(column)).replace("MASA/TIME","")
        return cols

def strip_html(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data() #strip all HTML from the data


def get_html(url,current_url_date):    

    
    current_url_being_read = url + "year/" + str(current_url_date.year) + "/month/" + str(current_url_date.month) + "/day/" + str(current_url_date.day)
    print '@@@@@' + str(current_url_date) + '@@@@@'
    print current_url_being_read

    #attempt to open the webpage of the current URL
    try:
        webpage_html = urllib2.urlopen(current_url_being_read, timeout=30)
    except URLError, e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
        return None
    except :
        print 'Unknown Error Occured'
        return None

    return webpage_html
