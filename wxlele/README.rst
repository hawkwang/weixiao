wxlele: Best event sharing and searching engine
==========================

.. code-block:: python

   移植注意:
   给如下目录写权限
   lele/public/img/captcha
   lele/public/img/photo/tmp
   lele/public/img/photo/tmp/thumbnails
   lele/public/img/photo/uploaded-files
   lele/public/img/data/tmp
   lele/public/img/data/tmp/thumbnails
   lele/public/img/data/uploaded-files
   lele/public/img/event-photo/tmp
   lele/public/img/event-photo/tmp/thumbnails
   lele/public/img/event-photo/uploaded-files

.. code-block:: python

   launch apache service
   ------------------------------------------------
   1. 查看apache服务
      ps ax | grep httpd | grep -v grep
   2. 启动
      /usr/local/zend/apache2/bin/httpd -f /usr/local/zend/apache2/conf/httpd.conf -k start
   
   launch mysql service
   ------------------------------------------------
   由于装了两套mysql，重启机器后需要按照如下步骤去关掉zend的mysql再打开系统自带的
   1. 查看mysql服务
      ps aux|grep mysql
   2. 关闭所有的mysql服务
      sudo kill ***
   3. 启动指定的mysql服务
      sudo /usr/local/mysql/support-files/mysql.server restart
      
   launch postgresql service
   ------------------------------------------------
   根据各个应用创建自己的数据库
   
   launch WeixiaoCrawler
   ------------------------------------------------
   cd Dropbox/weixiao/platform/crawler
   ./runme
   
   launch WeixiaoTask
   ------------------------------------------------
   参见相关安装运行。
   
   launch WeixiaoSim
   ------------------------------------------------
   cd /Users/hawkwang/Documents/weixiao/wxopentask/WeixiaoSim/weixiao
   python main.py http://wxlele.local/api/
   
   launch WeixiaoService/leleminer
   ------------------------------------------------
   cd /Users/hawkwang/Documents/weixiao/wxservice/leleminer
   python leleminer.py
   
   launch WeixiaoService/lelebehavior
   ------------------------------------------------
   cd /Users/hawkwang/Documents/weixiao/wxservice/lelebehavior
   python lelebehavior.py
   
   launch WexiaoSearchEngine
   ------------------------------------------------
   cd /home/hawkwang/Documents/solr-4.6.1/lele
   java -jar start.jar
   http://localhost:8983/solr/#/events/query
   
   launch WeixiaoLele
   ------------------------------------------------

How to add new source with crawler (FIXME)
^^^^^
.. code-block:: python

   1 - create group
   
   2 - get group id with mysql
   
   3 - create crawler emits event item with source of the group id
   
   4 - run WeixiaoSim to put newly identified event to lele repository
   


Todo list
^^^^^
.. code-block:: python

   DONE - promote module - used to support 赞 and hook the activity log to database
   
   WIP - wxbehavior subsystem (service) - used to log any needed behavior from user, and generate analysis report and output by json 

   TBD - update search engine related code to reflect popularity (access, like, share, save and etc.)
   
   TBD - design weixiao popularity models for group, lele and user
   
   TBD - create nonceutil, see https://github.com/timostamm/NonceUtil-PHP and http://tyleregeto.com/article/a-guide-to-nonce
   
   
   
