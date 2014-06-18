wxlele: Best event sharing and searching engine
==========================

移植注意

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
   
   launch mysql service
   ------------------------------------------------
   由于装了两套mysql，重启机器后需要按照如下步骤去关掉zend的mysql再打开系统自带的
   ps aux|grep mysql
   sudo kill ***
   sudo /usr/local/mysql/support-files/mysql.server restart
   
   launch WeixiaoCrawler
   ------------------------------------------------
   
   launch WeixiaoTask
   ------------------------------------------------
   
   launch WeixiaoSim
   ------------------------------------------------
   
   launch WeixiaoService/leleminer
   ------------------------------------------------
   
   launch WeixiaoService/lelebehavior
   ------------------------------------------------
   
   
   launch WexiaoSearchEngine
   ------------------------------------------------
   cd /home/hawkwang/Documents/solr-4.6.1/lele
   java -jar start.jar
   http://localhost:8983/solr/#/events/query
   
   launch WeixiaoLele
   ------------------------------------------------


Todo list
^^^^^
.. code-block:: python

   DONE - promote module - used to support 赞 and hook the activity log to database
   
   WIP - wxbehavior subsystem (service) - used to log any needed behavior from user, and generate analysis report and output by json 

   TBD - update search engine related code to reflect popularity (access, like, share, save and etc.)
   
   TBD - design weixiao popularity models for group, lele and user
   
   TBD - create nonceutil, see https://github.com/timostamm/NonceUtil-PHP and http://tyleregeto.com/article/a-guide-to-nonce
   
   
   
