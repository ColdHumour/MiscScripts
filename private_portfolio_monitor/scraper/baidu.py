# -*- coding: utf-8 -*-

"""
baidu.py

market data scraper from baidu
"""

import urllib
from bs4 import BeautifulSoup

BASEURL_INTRADAY = "http://gupiao.baidu.com/api/stocks/stocktimeline?from=pc&os_ver=1&cuid=xxx&vv=100&format=json&stock_code=sh000300"