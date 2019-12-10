"""19HZ Website Scrape"""

from bs4 import BeautifulSoup
import requests
import csv
import html5lib


source = requests.get('https://19hz.info/eventlisting_BayArea.php').text

# with open('eventlisting_BayArea.php') as f:
#     source = f.read()

soup = BeautifulSoup(source, 'html5lib')

csv_file = open('19hz_scrape.csv', 'w')

csv_writer = csv.writer(csv_file, delimiter='\t')

def get_td_from_tr(tr):
    """ Find all td html tags."""
    return tr.find_all('td')


def process_tr(tr):
    """ Getting info in the row."""

    data = tr.find_all('td')

    try:
        name_location = (data[1].text).split('@ ')
        name = ''.join(name_location[:1])
        location = ''.join(name_location[1:2])
        date = data[0].text
        genre = data[2].text
        price_age = data[3].text
        organizer = data[4].text
        link = tr.find('a')['href']

        
    except:
        print(get_td_from_tr(tr))
        return

    csv_writer.writerow([name,location,date,genre,price_age,organizer,link])

for tr in (soup.find('table').find_all('tr')[1:]):
    """Calls the fun process_tr on the table that contains data we need."""
    process_tr(tr)

    

csv_file.close()
