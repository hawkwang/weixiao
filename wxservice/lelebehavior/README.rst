lelebehavior: save user access behavior
==========================

lelebehavior is providing web services through RESTful API:

.. code-block:: shell

   curl -u hawkwang:1111111 -i -H "Content-Type: application/json" -X POST -d '{"uid":-1,"gid":-1,"t":"1401895865","IP":"127.0.0.1","bcode":0,"tcode":0, "tid":-1 }' http://localhost:5002/behavior/api/v1.0/behaviors


Behavior Code (bcode)
-----------

.. code-block:: shell
0 - 访问
1 - 注册
2 - 登录
3 - 退出
4 - 赞
5 - 分享
6 - 创建
7 - 
 - 
 - 
 - 
 - 

Target Code (tcode)
-----------

.. code-block:: shell
0 - lele主页
1 - 乐群
1 - 乐乐
2 - 乐友
 - 

Prepare with PostgreSQL
^^^^^^^

1. ``sudo su postgres`` with complex password
2. ``createuser -d -P lelebehavior``
3. ``createdb lelebehavior -O lelebehavior``

Usage with virtualenv
^^^^^

1. ``cd leleminer``
2. ``virtualenv env``
3. Activate the virtual environment
   ``source env/bin/activate``
4. Install the required libraries
   4.1 ``pip install -r requirements.txt``
5. Launch leleminer web service
   ``python lelebehavior.py``

