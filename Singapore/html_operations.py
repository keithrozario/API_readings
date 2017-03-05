from urllib.error import URLError
from urllib.request import urlopen
from urllib.error import HTTPError
from html.parser import HTMLParser
import urllib


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
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

    if int(current_url_date[8:10])>9: #double digits
        current_url_being_day = current_url_date[8:10]
    else:
        current_url_being_day = current_url_date[9:10]

    if int(current_url_date[5:7])>9: #double digits
        current_url_being_month = current_url_date[5:7]
    else:
        current_url_being_month = current_url_date[6:7]

    current_url_year = current_url_date[0:4]


    current_url_being_read = url + "year/" + current_url_year + "/month/" + current_url_being_month  + "/day/" + current_url_being_day
    
    print ('@@@@@' + str(current_url_date) + '@@@@@')
    print (current_url_being_read)



    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    test_headers = {'User-Agent': user_agent}

    req = urllib.request.Request(current_url_being_read, data=None, headers=test_headers)

    #attempt to open the webpage of the current URL
    try:
        webpage_html = urlopen(req)
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read())
        return None

    return webpage_html
