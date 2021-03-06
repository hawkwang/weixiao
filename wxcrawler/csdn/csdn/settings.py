#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Scrapy settings for csdn project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'csdn'

SPIDER_MODULES = ['csdn.spiders']
NEWSPIDER_MODULE = 'csdn.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'douban (+http://www.yourdomain.com)'

#REDIRECT_ENABLED = False
#RETRY_ENABLED = False
LOG_ENABLED = True 
LOG_LEVEL = 'INFO'
#CONCURRENT_REQUESTS = 100
#AJAXCRAWL_ENABLED = True

ITEM_PIPELINES = {
    'csdn.pipelines.DuplicatesPipeline': 300,
    'csdn.pipelines.LivingSocialPipeline': 800,
}

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',
            'port': '5432',
            'username': 'lelespider',
            'password': '1111111',
            'database': 'lelespider'}


