# -*- coding: utf-8 -*-
"""
Created on 2021-05-13 20:57:49
---------
@summary:
---------
@author: george
"""

import feapder


class Account(feapder.AirSpider):
    def start_requests(self):
        yield feapder.Request("https://www.baidu.com")

    def parse(self, request, response):
        print(response)


if __name__ == "__main__":
    Account().start()