# Scrapy settings for douban project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'douban (+http://www.yourdomain.com)'

#REDIRECT_ENABLED = False
#RETRY_ENABLED = False
LOG_LEVEL = 'INFO'
#CONCURRENT_REQUESTS = 100
#AJAXCRAWL_ENABLED = True

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


