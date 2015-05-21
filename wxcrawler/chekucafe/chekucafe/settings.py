# -*- coding: utf-8 -*-

# Scrapy settings for chekucafe project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'chekucafe'

SPIDER_MODULES = ['chekucafe.spiders']
NEWSPIDER_MODULE = 'chekucafe.spiders'

LOG_LEVEL = 'INFO'
RETRY_ENABLED = False

ITEM_PIPELINES = {
#    'chekucafe.pipelines.ChekucafePipeline': 200,
    'chekucafe.pipelines.DuplicatesPipeline': 300,
    'chekucafe.pipelines.LivingSocialPipeline': 800,
}

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'lelespider',
            'password': '1111111',
            'database': 'lelespider'}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'chekucafe (+http://www.yourdomain.com)'
