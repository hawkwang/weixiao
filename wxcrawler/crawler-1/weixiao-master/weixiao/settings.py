# Scrapy settings for comesg project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'weixiao'

SPIDER_MODULES = ['weixiao.spiders']
NEWSPIDER_MODULE = 'weixiao.spiders'

ITEM_PIPELINES = {
    'weixiao.pipelines.DuplicatesPipeline': 300,
    'weixiao.pipelines.LivingSocialPipeline': 800,
}

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'lelespider',
            'password': '1111111',
            'database': 'lelespider'}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'comesg (+http://www.yourdomain.com)'
