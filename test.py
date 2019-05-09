# -*- coding: utf-8 -*-
# Created by CaoDa on 2019/5/8
import random
import time

from tornado.ioloop import IOLoop

from ip2region_util import IP2RegionUtil

io_loop = IOLoop.instance()
util = IP2RegionUtil()
r = lambda: random.randint(0, 255)
ips = ['{}.{}.{}.{}'.format(r(), r(), r(), r()) for x in range(100000)]
t1 = time.time()
for ip in ips:
    util.search(ip)
print(time.time() - t1)
io_loop.start()
