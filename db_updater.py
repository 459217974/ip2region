# -*- coding: utf-8 -*-
# Created by CaoDa on 2019/5/7
import hashlib
import json
import os
from typing import Callable, Awaitable

from tornado.ioloop import IOLoop

from tornado.httpclient import AsyncHTTPClient


class DBUpdater(object):

    def __init__(self):
        self.http_client = AsyncHTTPClient()
        self.check_url = 'https://api.github.com/repos/lionsoul2014/ip2region/contents/data'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
        }
        self.checking = False
        if os.path.exists('ip2region.db'):
            with open('ip2region.db', 'rb') as f:
                db_file = f.read()
            self.db_file_sha = self.__get_github_file_sha(db_file)

    @classmethod
    def __get_github_file_sha(cls, file: bytes):
        return hashlib.sha1(
            b'blob ' + str(len(file)).encode() + b'\0' + file
        ).hexdigest()

    async def __co_download_db(self, url, sha):
        res = await self.http_client.fetch(url, method='GET', headers=self.headers)
        if res.code != 200:
            raise IOError('download db file failed!')
        if self.__get_github_file_sha(res.body) != sha:
            raise IOError('download db file failed!')
        with open('ip2region.db', 'wb') as f:
            f.write(res.body)

    @classmethod
    def __get_db_file_info(cls, file_infos):
        for file_info in file_infos:
            if file_info.get('name', '') == 'ip2region.db':
                return file_info

    async def __co_check_and_update(self, db_changed_callback: Callable):
        IOLoop.current().call_later(5, self.__co_check_and_update, db_changed_callback)
        if self.checking:
            return
        self.checking = True
        try:
            res = await self.http_client.fetch(
                self.check_url, method='GET', headers=self.headers
            )
            if res.code != 200:
                raise IOError('call github api failed')
            file_infos = json.loads(res.body)
            db_file_info = self.__get_db_file_info(file_infos)
            if self.db_file_sha != db_file_info['sha']:
                await self.__co_download_db(db_file_info['download_url'], db_file_info['sha'])
                self.db_file_sha = db_file_info['sha']
                ret = db_changed_callback()
                if isinstance(ret, Awaitable):
                    await ret
        finally:
            self.checking = False

    def start(self, db_changed_callback: Callable):
        IOLoop.current().add_callback(self.__co_check_and_update, db_changed_callback)
