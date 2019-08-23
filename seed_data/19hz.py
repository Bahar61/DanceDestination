"""19HZ Website Scrape"""

from bs4 import BeautifulSoup
import requests

source = requests.get('https://19hz.info/eventlisting_BayArea.php').text

soup = BeautifulSoup(source, 'html5lib')

# print(soup.prettify())


# event_link = soup.find('a')['href']

# print(event_link)

# for link in soup.find_all('a'):



row = soup.table.tbody.tr
link = soup.table.tbody.tr.a['href']



# print(row)
# print(link)

# for child in row.children:
print(list(row.children)[0].text)
    # print(child.text)
    