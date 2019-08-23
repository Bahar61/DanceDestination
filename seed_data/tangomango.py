"""Tango Mango Website Scrape"""

from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.tangomango.org/index.php?show=San_Francisco,\
                       CA+Alameda,CA+San_Mateo,CA+Santa_Clara,CA+Marin,CA+Contra_Costa,\
                       CA+Sacramento,CA+Santa_Cruz,CA+Monterey,CA+Sonoma,CA+Mendocino,\
                       CA+Stanislaus,CA').text

soup = BeautifulSoup(source, 'html5lib')

# print(soup.prettify())


location = soup.findAll("td", {"onclick"="location='/mycal.php'" "onmouseout"="outtab()" "onmouseover"="overtab('mycal')"}) 

print(location)