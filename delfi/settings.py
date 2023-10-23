# All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

SPIDER_MODULES = ['delfi.zirneklis']
USER_AGENT = 'Friendly scraper'
DOWNLOAD_DELAY = 1
ITEM_PIPELINES = {'delfi.pipelines.RakstuApstrade': 300}
DOWNLOADER_CLIENT_TLS_METHOD = 'TLSv1.2'
FEED_EXPORT_ENCODING = 'utf-8'
CONCURRENT_REQUESTS=25
