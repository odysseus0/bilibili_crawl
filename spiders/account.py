# -*- coding: utf-8 -*-
"""
Created on 2021-05-13 20:57:49
---------
@summary:
---------
@author: george
"""

import feapder
from items.account_item import AccountItem
from items.account_following_item import AccountFollowingItem
from myproxy import proxies


class Account(feapder.Spider):
    __SEED_MID__ = 20165629  # 共青团中央
    __MAX_DEPTH__ = 3

    def info_request(self, mid):
        """
        Construct account info request
        """
        return feapder.Request(f"https://api.bilibili.com/x/space/acc/info?mid={mid}")

    def following_request(self, mid, pn=1, depth=1):
        """
        Construct account following relation request
        """
        return feapder.Request(f"https://api.bilibili.com/x/relation/followings?vmid={mid}&ps=50&pn={pn}",
                               callback=self.following_parse, mid=mid, depth=depth, pn=pn)

    def start_requests(self):
        yield self.info_request(self.__SEED_MID__)
        yield self.following_request(self.__SEED_MID__)

    def following_parse(self, request, response):
        """
        Parser for response from following request.
        """
        mid = request.mid
        pn = request.pn
        depth = request.depth

        # If the account somehow does not allow us to check its followings
        if response.json['code'] != 0:
            return
        data = response.json['data']
        total = int(data['total'])

        # Save this page of following to database
        yield AccountFollowingItem(mid=mid, pn=pn, **data)
        # If there are more following pages, request them as well
        if pn < 5 and 50 * pn < total:
            yield self.following_request(mid, pn + 1, depth)

        # Scrap the info of all the official accounts the current account follows
        # Deduplication will be taken care of by the framework
        following_mids = [acc['mid'] for acc in data['list'] if acc['official_verify']['type'] == 1]
        for acc in data['list']:
            yield AccountItem(**acc)
        # for following_mid in following_mids:
        #     yield self.info_request(following_mid)

        if depth + 1 <= self.__MAX_DEPTH__:
            for following_mid in following_mids:
                yield self.following_request(following_mid, depth=depth + 1)

    def parse(self, request, response):
        """
        Parser for response from account info request.
        """
        if response.json['code'] != 0:
            return

        yield AccountItem(**response.json['data'])

    def validate(self, request, response):
        # ask the cralwer to retry failed request
        if response.status_code != 200:
            raise Exception("response code not 200")

    def download_midware(self, request):
        request.proxies = proxies
        return request


if __name__ == "__main__":
    Account(redis_key="account").start()
