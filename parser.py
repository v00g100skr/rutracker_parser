from dateutil import parser
import requests
import feedparser
import sqlite3
import logging
import os
import asyncio


BOT_TOKEN = os.environ.get('BOT_TOKEN') or 'bot_token'
CHANNEL_ID = os.environ.get('CHANNEL_ID') or 'chanelid'
FEED_URLS = os.environ.get('FEED_URLS') or []

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


async def main():
    for feed_url in FEED_URLS.split(','):
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
                message = '<b>%s</b>\n\n%s\n\n%s' % (entry.title, entry.tags[0].label, entry.links[0].href)
                send_message(message)
                data =[(entry.title, parsed_date)]
                cursor.executemany("INSERT INTO entities VALUES (?,?)", data)
                conn.commit()
        logger.info('END %s' % (feed_url))
        await asyncio.sleep(1200)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    asyncio.ensure_future(main())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.close()
