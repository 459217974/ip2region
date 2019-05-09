查询IP地区工具
===
&nbsp;&nbsp;&nbsp;&nbsp;
根据IP查询IP地区的工具。使用了**Cython**优化了性能。结合**Tornado**可以实现自动更新 IP 数据库。
感谢 [ip2region](https://github.com/lionsoul2014/ip2region) 项目提供的支持。

&nbsp;&nbsp;&nbsp;&nbsp;
由于做项目需要这个工具，也是临时学的**Cython**，所以欢迎大佬能提出改进意见，继续优化性能。

&nbsp;&nbsp;&nbsp;&nbsp;
有**Bug**欢迎提 [ISSUE](https://github.com/459217974/ip2region/issues/new) ，当然如果能直接提 PullRequest 就更好了。

## 使用

* 安装依赖

    ```bash
    pip install -r requirements.txt    
    ``` 
* 编译 **Cython** 拓展

    ```bash
    python setup.py build_ext --inplace
    ```
    
    **Cython**环境的安装请参照[官网](http://docs.cython.org/en/latest/src/quickstart/install.html)
    
* 测试

    - 简单使用（直接使用自带数据库文件，无自动更新功能，不依赖**Tornado**）
    
        ```python
        from ip2region_util import IP2RegionUtil
  
        util = IP2RegionUtil()
        print(util.search('8.8.8.8'))
        ```
        输出：
        ```python
        {'city_id': 166, 'region': '美国|0|0|0|Level3'}
        ```
     - 基于**Tornado**实现自动更新数据库文件
    
        ```python
        from ip2region_util import IP2RegionUtil
        from tornado.ioloop import IOLoop
 
        util = IP2RegionUtil()
        io_loop = IOLoop.instance()
        print(util.search('8.8.8.8'))
        io_loop.start()
        ```
        
 ## 性能
 
 &nbsp;&nbsp;&nbsp;&nbsp;
 为了尽量提高性能，本项目在原 [ip2region](https://github.com/lionsoul2014/ip2region) 项目的基础上仅仅保留了内存搜索方法。实际测试比原方法提升一倍以上性能。
 
 我测试的参考数据：10W/s
