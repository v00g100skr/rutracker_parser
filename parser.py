from dateutil import parser
import requests
import feedparser
import sqlite3
import logging
import yaml

try:
    with open("local.yml", 'r') as stream:
        config = yaml.safe_load(stream)
except:
    with open("config.yml", 'r') as stream:
        config = yaml.safe_load(stream)

BOT_TOKEN = config['BOT_TOKEN']
CHANNEL_ID = config['CHANNEL_ID']
FEED_URLS = config['FEED_URLS']

conn = sqlite3.connect("parser.db")
cursor = conn.cursor()

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('parser.log')
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)


def send_message(message):
    requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text={message}&parse_mode=html&disable_web_page_preview=True')


def main():
    for feed_url in FEED_URLS:
        logger.info('RUN %s' % (feed_url))
        rss_feed = feedparser.parse(feed_url)

        for entry in rss_feed.entries:

            parsed_date = parser.parse(entry.updated)
            sql = "SELECT * FROM entities WHERE title=?"
            cursor.execute(sql, [(entry.title)])
            result = cursor.fetchone()
            logger.debug(entry.title)

            if not result:
                logger.info(entry.title)
                message = '<b>%s</b>\n\n%s\n\n%s' % (entry.tags[0].label, entry.title, entry.links[0].href)
                send_message(message)
                data =[(entry.title, parsed_date)]
                cursor.executemany("INSERT INTO entities VALUES (?,?)", data)
                conn.commit()
        logger.info('END %s' % (feed_url))

if __name__ == "__main__":
    main()
