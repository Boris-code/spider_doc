分布式爬虫-Spider
=================

该爬虫支持分布式，使用方式与\ ``SingleSpider``\ 类似，常用于抓取大规模数据的生产环境。

阅读建议：根据文档的每一步，动手实操

因爬虫与\ ``SingleSpider``\ 使用方式类似，更高级的使用方法参考\ ``SingleSpider``

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

2. 快速生成分布式爬虫
---------------------

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


1. 修改基类， 使其继承\ **spider.Spider**\ ：

   ::

       class TestParsers(spider.Spider):

2. 修改配置文件setting.py, 设置数据库连接地址.
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

3. 改造main.py, 改成如下：

   ::

       from parsers import *


       if __name__ == "__main__":
           spider = test_parsers.TestParsers(table_folder="test:test1")
           spider.start()

4. 运行main.py 即可

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



**总结：**

数据入库， 只需要根据表生成item， 然后给item赋值， 之后直接 yield item
即可

示例代码：https://github.com/Boris-code/boris-spider-demo/tree/master/spider\_demo

4.Spider类参数详解
------------------

::

    def __init__(
            self,
            table_folder=None,
            min_task_count=1,
            check_task_interval=5,
            parser_count=None,
            begin_callback=None,
            end_callback=None,
            delete_tabs=(),
            process_num=None,
            auto_stop_when_spider_done=None,
            auto_start_requests=None,
            send_run_time=False,
            batch_interval=0,
            *parser_args,
            **parser_kwargs
        ):
        """
        @summary: 爬虫
        ---------
        @param table_folder: 爬虫request及item存放redis中的文件夹
        @param min_task_count: redis 中最少任务数, 少于这个数量会从mysql的任务表取任务。默认1秒
        @param check_task_interval: 检查是否还有任务的时间间隔；默认5秒
        @param parser_count: 线程数，默认为配置文件中的线程数
        @param begin_callback: 爬虫开始回调函数
        @param end_callback: 爬虫结束回调函数
        @param delete_tabs: 爬虫启动时删除的表，元组类型。 支持正则
        @param process_num: 进程数
        @param auto_stop_when_spider_done: 爬虫抓取完毕后是否自动结束或等待任务，默认自动结束
        @param auto_start_requests: 爬虫是否自动添加任务
        @param send_run_time: 发送运行时间
        @param batch_interval: 抓取时间间隔 默认为0 天为单位 多次启动时，只有当前时间与第一次抓取结束的时间间隔大于指定的时间间隔时，爬虫才启动

        @param *parser_args: 传给parser下start_requests的参数, tuple()
        @param **parser_kwargs: 传给parser下start_requests的参数, dict()
        ---------
        @result:
        """

.. |-w274| image:: http://markdown-media.oss-cn-beijing.aliyuncs.com/2020/07/13/15939415095166.jpg?x-oss-process=style/markdown-media
.. |-w1343| image:: http://markdown-media.oss-cn-beijing.aliyuncs.com/2020/07/13/15945669163896.jpg?x-oss-process=style/markdown-media
