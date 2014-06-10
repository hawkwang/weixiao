lelebehavior: save user access behavior
==========================

lelebehavior is providing web services through RESTful API:

.. code-block:: shell

   curl -u hawkwang:1111111 -i -H "Content-Type: application/json" -X POST -d '{"uid":-1,"gid":-1,"t":"1401895865","IP":"127.0.0.1","bcode":0,"tcode":0, "tid":-1 }' http://localhost:5002/behavior/api/v1.0/behaviors

   curl -u hawkwang:1111111 -i -H "Content-Type: application/json" -X POST -d '{"uid":-1,"gid":-1,"t":"1401895865","IP":"127.0.0.1", "bcode":0,"tcode":0, "tid":-1}' http://localhost:5002/behavior/api/v1.0/statistics

the statistics API is used to get the specified statistic report with json format, for example,
for "赞", we can get result as {"s":1,"t":200}, 
which "s" means that the specifies user himself or herself like count for the target, 
while "t" means that the total like count for the target (乐趣，乐友，乐乐, etc.)

Behavior Code (bcode)
-----------

.. code-block:: shell

0 - 访问

1 - 注册

2 - 登录

3 - 退出

4 - 赞

5 - 取消赞

6 - 分享

7 - 创建

8 - 评论

9 - 访问信息源

10 - 关注（收藏）

11 - 取消关注

12 - 搜索 （包括点击 1.群乐等按钮；2.更多？；3.刷新？   ？表示是否应该统计呢？）

13 - 

-

-

-



Target Code (tcode)
-----------

.. code-block:: shell

0 - lele主页

1 - 乐群

2 - 乐乐

3 - 乐友

4 - 

Prepare with PostgreSQL
^^^^^^^

1. ``sudo su postgres`` with complex password
2. ``createuser -d -P lelebehavior``
3. ``createdb lelebehavior -O lelebehavior``

Usage with virtualenv
^^^^^

1. ``cd lelebehavior``
2. ``virtualenv env``
3. Activate the virtual environment
   ``source env/bin/activate``
4. Install the required libraries
   4.1 ``pip install -r requirements.txt``
5. Launch lelebehavior web service
   ``python lelebehavior.py``

