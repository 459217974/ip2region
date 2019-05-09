# -*- coding: utf-8 -*-
# Created by CaoDa on 2019/5/9
from singleton_meta import SingletonMeta
from db_updater import DBUpdater
from searcher import IP2Region


class IP2RegionUtil(object, metaclass=SingletonMeta):

    def __init__(self):
        self.db_updater = DBUpdater()
        self.searcher = IP2Region()
        self.db_updater.start(self.__on_db_changed)

    def search(self, ip):
        return self.searcher.search(ip)

    def __on_db_changed(self):
        self.searcher = IP2Region()
