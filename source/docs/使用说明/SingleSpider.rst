单机爬虫-SingleSpider
=====================

该爬虫上手比较简单，支持多线程，但不支持分布式。如果待抓取的目标数据量不多，可选用此爬虫。

.. _1-创建爬虫:

1. 创建爬虫
-----------

打开命令行工具，输入 ``spider create -p TestSpider``\ ，
TestSpider为爬虫名，可随意指定，支持下划线和驼峰两种命名规范。
示例如下：

::

   > spider create -p TestSpider

   TestSpider 生成成功

观察当前目录，我们会发现，已经生成了个\ **test_spider.py**,
文件内容如下：

::

   import spider


   class TestSpider(spider.SingleSpider):
       def start_requests(self, *args, **kws):
           yield spider.Request("https://www.baidu.com")

       def parser(self, request, response):
           # print(response.text)
           print(response.xpath('//input[@type="submit"]/@value').extract_first())


   if __name__ == "__main__":
       TestSpider().start()

可直接运行

.. _2-代码讲解:

2. 代码讲解
-----------

默认生成的代码继承了spider.SingleSpider，包含 ``start_requests`` 及
``parser`` 两个函数，含义如下：

1. spider.SingleSpider：单机爬虫
2. start_requests：初始任务下发入口
3. spider.Request：与著名的requests库类似，表示一个请求，支持requests所有参数，同时也可携带些自定义的参数，之后详细说明
4. parser：数据解析函数
5. response：请求响应的返回体，支持xpath、re、css等解析方式

.. _3-使用进阶:

3. 使用进阶
-----------

.. _31-指定解析函数:

3.1 指定解析函数
~~~~~~~~~~~~~~~~

默认的解析函数为parser，不过往往我们会有多个解析函数，来应对不同的响应，这时就需要指定请求对应的解析函数是哪个，使用方法如下：

1. 生产任务时使用\ ``callback``\ 参数指定解析函数，如

   ::

       yield spider.Request("https://www.baidu.com", callback=self.parser_baidu)

2. 定义解析函数，如：

   ::

       def parser_baidu(self, request, response):
            pass

.. _32-携带参数:

3.2 携带参数
~~~~~~~~~~~~

开发过程中，我们往往需要携带一些中间过程的参数，比如我们在解析函数\ ``parser1``\ 中抽取到了数据A，需要携带到\ ``parser2``\ 中，如何做呢？
示例如下：

::

   def parser1(self, request, response):
       yield spider.Request("https://www.baidu.com", A='123', callback=self.parser2)


   def parser2(self, request, response):
       A = request.A
       print(A)

即在Request中作为一个参数携带，获取时直接request.xxx即可。支持携带任意类型的参数。

.. _33-下载中间件:

3.3 下载中间件
~~~~~~~~~~~~~~

用于在下载前动态的修改请求，如追加cookie，请求头等。使用示例如下：

::

   def download_midware(self, request):
       request.headers = {
           "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36"
       }
       return request

这样，每个Request在下载response之前，都会经过此中间件，动态的添加了请求头。

有时，我们需要多个下载中间件，来对不同类型的请求添加不同的参数，我们可以使用\ ``download_midware``\ 参数\ **指定中间件**\ ，示例如下：

::

   def start_requests(self, *args, **kws):
       yield spider.Request("https://www.baidu.com", download_midware=self.download_midware1)

   def download_midware1(self, request):
       request.headers = {
           "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36"
       }
       return request

.. _34-使用多线程:

3.4 使用多线程
~~~~~~~~~~~~~~

默认是单线程，若想开启多线程，可传递参数\ ``parser_count``\ ，值为线程数，示例如下：

::

   if __name__ == "__main__":
       TestSpider2(parser_count=10).start() // 开起了10线程