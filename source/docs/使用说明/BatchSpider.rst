批次爬虫-BatchSpider
====================

批次爬取是基于分布式爬虫改进的，使其更好的支持周期性采集。本框架会记录每个批次的抓取状态，以及监控预警

准备条件
--------

批次爬虫为保证每个批次都全量抓取指定的数据，任务队列采用任务表的方式记录，比如下图，我们将要抓取的地址存入任务表

.. figure:: http://markdown-media.oss-cn-beijing.aliyuncs.com/2020/12/30/16093098203519.jpg?x-oss-process=style/markdown-media
   :alt:

任务表的字段包括爬虫请求的必要参数，如url、或某些id等，以保证我们可以用这些参数拼出请求。本示例为\ ``url``

另外还需要包含一个字段，表示本条任务的处理状态，本示例为 ``state``\ ，
state字段为整形，值有4种（-1 抓取失败，0等待抓取，1抓取成功，2抓取中）

1. 创建项目
-----------

::

    > spider create -s test-spider

    test-spider 项目生成成功

生成的项目结构如下： |-w274|

解释说明

1. main.py：代码启动入口
2. setting.py：项目配置文件
3. parsers/：编写爬虫的位置
4. items/：数据item文件存放的位置

2. 快速生成批次爬虫
-------------------

1. 进入parsers目录：\ ``cd test-spider/parsers``
2. 创建爬虫：\ ``spider create -p test_parsers``

创建爬虫后，默认生成的代码模板如下：

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


1. 修改基类， 使其继承\ **spider.BatchSpider**\ ：

   ::

       class TestParsers(spider.BatchSpider):

2. 修改start\_requests函数，接收传递的task

   ::

       def start_requests(self, task):
           # task 为在任务表中取出的每一条任务
           id, url = task # id， url为所取的字段，main函数中指定的
           yield spider.Request(url, task_id=id)

3. 修改配置文件setting.py, 设置数据库连接地址.
   redis数据库用来做任务队列，mysql数据库用来存储抓取到的数据，二者均均要配置

   ::

       # MYSQL
       MYSQL_IP = ""
       MYSQL_PORT = 3306
       MYSQL_DB = ""
       MYSQL_USER_NAME = ""
       MYSQL_USER_PASS = ""

       # REDIS
       # IP:PORT 多个逗号分隔
       REDISDB_IP_PORTS = "localhost:6379"
       REDISDB_USER_PASS = ""
       # 默认 0 到 15 共16个数据库
       REDISDB_DB = 0

4. 改造main.py, 改成如下：

   ::

       from parsers import *
       from spider import ArgumentParser

       def crawl_test(args):
           spider = test_parsers.TestParsers(
               task_table="batch_spider_task",  # mysql中的任务表
               batch_record_table="batch_spider_batch_record",  # mysql中的批次记录表
               batch_name="批次爬虫测试(周全)",  # 批次名字
               batch_interval=7,  # 批次时间 天为单位 若为小时 可写 1 / 24
               task_keys=["id", "url"],  # 需要获取任务表里的字段名，可添加多个
               table_folder="test:batch_spider",  # redis中存放request等信息的根key
               task_state="state",  # mysql中任务状态字段
           )

           if args == 1:
               spider.start_monitor_task()  # 监控批次与任务下发

           if args == 2:
               spider.start()  # 采集


       if __name__ == "__main__":
           parser = ArgumentParser(description="批次爬虫示例")
           parser.add_argument(
               "--crawl_test", type=int, nargs=1, help="批次爬虫测试(1|2）", function=crawl_test
           )

       parser.start()

5. 运行

   ::

       # 监控批次与任务下发
       python main.py --crawl_test 1
       # 采集
       python main.py --crawl_test 1

3. 数据入库
-----------

数据入库支持两种方式

1. 自己编写入库sql，调用操作数据库的第三方包，如pymsql，将数据入库。\ **不推荐**\ ，原因如下：

   1. pymysql不支持并发操作，及多线程
   2. 数据建议批量入库，自己组装数据，分批入库比较麻烦
   3. 拼接sql比较麻烦

2. 使用框架的item模块。\ **推荐**

3.1 item 模块快速入门
~~~~~~~~~~~~~~~~~~~~~

首先先介绍下item的含义。item
及为抓取的结构化数据，一个item类对应一张表，每个item对象对应表里的一条数据

1. 首先我们先创建一张表，如： |-w1343|
2. 生成item：

   返回项目，cd到items目录下，执行 ``spider create -i spider_test``
   (spider\_test 为第一步创建的表名)，打印如下：

   ::

       MainThread|2020-07-13 13:04:43,655|mysqldb.py|__init__|line:90|DEBUG| 连接到mysql数据库 localhost : spider-demo

       spider_test_item.py 生成成功

观察当前目录，已生成item文件，内容如下：

::

        from spider import Item


        class SpiderTestItem(Item):
            def __init__(self, *args, **kwargs):
                # self.id = None  # type : int(10) unsigned | allow_null : NO | key : PRI | default_value : None | extra : auto_increment | column_comment :
                self.title = None  # type : varchar(255) | allow_null : YES | key :  | default_value : None | extra : | column_comment :

1. 使用item将数据入库:

修改 parsers/test\_parsers.py， 内容如下：

::

        def parser(self, request, response):
            title = response.xpath('//title/text()').extract_first() # 取标题
            item = spider_test_item.SpiderTestItem() # 声明一个item
            item.title = title # 给item属性赋值
            yield item # 返回item， item会自动批量入库


数据入库， 只需要根据表生成item， 然后给item赋值， 之后直接 yield item
即可

3.2 更新任务状态
~~~~~~~~~~~~~~~~

当一条任务做完后，我们要更新其状态，写法如下

::

    def parser(self, request, response):
        yield self.update_task_batch(request.task_id, 1) # 更新任务状态为1


4. 示例代码：
-------------

https://github.com/Boris-code/boris-spider-demo/tree/master/batch\_spider\_demo

.. |-w274| image:: http://markdown-media.oss-cn-beijing.aliyuncs.com/2020/07/13/15939415095166.jpg?x-oss-process=style/markdown-media
.. |-w1343| image:: http://markdown-media.oss-cn-beijing.aliyuncs.com/2020/07/13/15945669163896.jpg?x-oss-process=style/markdown-media
