.. python3-cookbook documentation master file, created by
   sphinx-quickstart on Tue Aug 19 03:21:45 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _topics-index:

================================================
boris-spider 1.0 documentation
================================================

.. toctree::
  :caption: 简介
  :hidden:

  docs/使用说明/index
  docs/框架剖析/index
  docs/学习交流/index


|image0|

**boris-spide**\ r是一款使用Python语言编写的爬虫框架，于多年的爬虫业务中不断磨合而诞生，相比于scrapy，该框架更易上手，且又满足复杂的需求，支持分布式及批次采集。

官方文档：https://spider-doc.readthedocs.io

特性
----

1. 自动下载与重试异常请求，返回的response支持\ **xpath**\ 、\ **css**\ 、\ **re**\ 等解析方式。自动处理中文乱码；
2. 支持 **单进程爬虫**\ ，
   **分布式爬虫**\ ，\ **批次爬虫**\ 。批次爬虫封装了周期性采集数据的逻辑，批次开始时自动下发任务，抓取数据，统计任务处理速度，预估批次是否会超时，\ **超时报警**\ 等；
3. 可\ **随时终止**\ 、启动爬虫，\ **任务不丢失不漏采**\ ；
4. **支持注册多模板**\ ，即可将多个网站的解析模板注册到同一个爬虫内，由该爬虫统一管理;
5. 内置\ **DebugSpider**\ 与\ **DebugBatchSpider**\ 调试爬虫，调试代码更方便，且不会将调试过程中的数据入库，造成数据污染;
6. 支持以\ **模板的方式创建**\ 爬虫项目、解析模板、数据item;
7. **数据自动入库**\ ，不需要编写Pipeline;


环境要求：
----------

-  Python 3.6.0+
-  Works on Linux, Windows, macOS

安装
----

From PyPi:

::

   pip3 install boris-spider

From Git:

::

   pip3 install git+https://github.com/Boris-code/boris-spider.git

快速上手
--------

创建爬虫

::

   spider create -p first_spider

创建后的爬虫代码如下：

::

   import spider


   class FirstSpider(spider.SingleSpider):
       def start_requests(self, *args, **kws):
           yield spider.Request("https://www.baidu.com")

       def parser(self, request, response):
           # print(response.text)
           print(response.xpath('//input[@type="submit"]/@value').extract_first())


   if __name__ == "__main__":
       FirstSpider().start()


直接运行，打印如下：

::

   Thread-2|2020-05-19 18:23:41,128|request.py|get_response|line:283|DEBUG|
                   -------------- FirstSpider.parser request for ----------------
                   url  = https://www.baidu.com
                   method = GET
                   body = {'timeout': 22, 'stream': True, 'verify': False, 'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'}}

   百度一下
   Thread-2|2020-05-19 18:23:41,727|parser_control.py|run|line:415|INFO| parser 等待任务 ...
   FirstSpider|2020-05-19 18:23:44,735|single_spider.py|run|line:83|DEBUG| 无任务，爬虫结束



.. |image0| image:: https://img.shields.io/badge/python-3.6-brightgreen