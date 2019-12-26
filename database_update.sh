touch /tmp/runed
source /home/vagrant/src/dance-destination/env/bin/activate
cd /home/vagrant/src/dance-destination
rm seed_data/19hz_scrape.csv
python3 seed_data/19hz.py
python3 -c 'from seed import update_events_database; update_events_database()'


