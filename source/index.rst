.. python3-cookbook documentation master file, created by
   sphinx-quickstart on Tue Aug 19 03:21:45 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _topics-index:

================================================
boris-spider documentation
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

1. 支持周期性采集
~~~~~~~~~~~~~~~~~

周期性抓取是爬虫中常见的需求，如每日抓取一次商品的销量等，我们把每个周期称为一个批次。

这类爬虫，普遍做法是设置个定时任务，每天启动一次。但你有没有想过，若由于某种原因，定时任务启动程序时没启动起来怎么办？比如服务器资源不够了，启动起来直接被kill了。

另外如何保证每条数据在每个批次内都得以更新呢？

本框架支持批次采集，引入了批次表的概念，详细记录了每一批次的抓取状态

.. figure:: http://markdown-media.oss-cn-beijing.aliyuncs.com/2020/12/20/16084680404224.jpg?x-oss-process=style/markdown-media
   :alt: -w899

2. 支持分布式
~~~~~~~~~~~~~

面对海量的数据，分布式采集必不可少的，本框架原生支持分布式，且可随时重启爬虫，任务不丢失

3. 完善的报警机制
~~~~~~~~~~~~~~~~~

为了保证数据的全量性、准确性、时效性，本框架内置报警机制，有了这些报警，我们可以实时掌握爬虫状态

.. figure:: http://markdown-media.oss-cn-beijing.aliyuncs.com/2020/12/20/16084718683378.jpg?x-oss-process=style/markdown-media
   :alt: -w657


.. figure:: http://markdown-media.oss-cn-beijing.aliyuncs.com/2020/12/20/16084718974597.jpg?x-oss-process=style/markdown-media
   :alt: -w501


.. figure:: http://markdown-media.oss-cn-beijing.aliyuncs.com/2020/12/29/16092335882158.jpg?x-oss-process=style/markdown-media
   :alt: -w416



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