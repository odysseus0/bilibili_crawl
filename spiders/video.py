# -*- coding: utf-8 -*-
"""
Created on 2021-05-13 21:05:24
---------
@summary:
---------
@author: george
"""

import feapder
from items.video_item import VideoItem


class Video(feapder.Spider):
    # specify the maximum number of depth when running BFS on content recommendation
    __MAX_DEPTH__ = 2
    __SEED_BVID__ = "BV1oJ411M7RS"

    def view_request(self, bvid):
        return feapder.Request(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}")

    def related_request(self, bvid, depth=1):
        return feapder.Request(f"https://api.bilibili.com/x/web-interface/archive/related?bvid={bvid}",
                               callback=self.parse_related, depth=depth)

    def start_requests(self):
        # this is the ID of the seed video
        # request to retrieve the info about the seed video itself
        yield self.view_request(self.__SEED_BVID__)
        # request to retrieve related videos of the video
        yield self.related_request(self.__SEED_BVID__)

    def parse(self, request, response):
        data = response.json['data']
        yield VideoItem(**data)

    def parse_related(self, request, response):
        # get the current depth
        depth = request.depth
        # stop searching if gone beyond the max depth
        if depth >= self.__MAX_DEPTH__:
            return

        data = response.json['data']
        for view in data:
            yield VideoItem(**view)
            yield self.related_request(view['bvid'], depth + 1)

    def validate(self, request, response):
        # ask the cralwer to retry failed request
        if response.status_code != 200:
            raise Exception("response code not 200")


if __name__ == "__main__":
    # specify the redis key used for this crawling task and the number of threads
    Video(redis_key="test", thread_count=4).start()
