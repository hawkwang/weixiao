wxanalyzer: Easy URL and web page content analyzer
==========================


The core API call is the function ``flag, msg, event = getEvent(url)``:

.. code-block:: python

   import wxanalyzer

   f, m, e = wxanalyzer.getEvent(url)

Package & Usage
-----------

Since *wxanalyzer* will be used in all the weixiao projects, so we just illustrate 
how to package and used in virtualenv.


Package
^^^^^

1. Prepare the requirements.txt and other stuff
2. Use ``python setup.py sdist`` to package module as follows:

dist

└── wxanalyzer-0.1.0.tar.gz


Usage with virtualenv
^^^^^

1. ``mkdir xyz; cd xyz``
2. ``virtualenv env``
3. Activate the virtual environment
   ``source env/bin/activate``
4. Install the required libraries
   ``pip install -r requirements.txt``
5. Install the wxanalyzer package
   ``pip install --no-index /wxanalyzer/dist/wxanalyzer-0.1.0.tar.gz``
6. Great, we can use the API call, see previous section.

Usage with Chinese
^^^^^

See: http://blog.csdn.net/gufengshanyin/article/details/21533409



一、版本信息

1.      Tomcat版本：apache-tomcat-6.0.39，

下载地址：http://tomcat.apache.org/download-60.cgi，下载32-bitWindows zip或64-bitWindows zip（根据自己电脑配置而定）

2.      Solr版本：solr-4.7.0，

下载地址：http://mirror.bit.edu.cn/apache/lucene/solr/4.7.0/，下载solr-4.7.0.zip，顺便把solr-4.7.0-src.tgz也一起下了吧（这是源码，以后在eclipse中配置solr需用到）

3.      IK Analyzer版本：IKAnalyzer 2012FF_hf1，

下载地址：https://code.google.com/p/ik-analyzer/downloads/list，下载IKAnalyzer 2012FF_hf1.zip

二、配置步骤

1.      解压IK Analyzer 2012FF_hf1.zip，将解压后文件夹中的IKAnalyzer2012FF_u1.jar拷贝到solr服务的solr\WEB-INF\lib下面（如：C:\Users\zheng\Downloads\apache-tomcat-6.0.39\solr\WEB-INF\lib），把IKAnalyzer.cfg.xml和stopword.dic拷贝到solr服务的solr\WEB-INF\lib\class下面（若lib文件夹下没有class文件夹，可自己新建）

2.      修改scheme.xml（注意是路径C:\Users\zheng\Downloads\solr-4.7.0\example\solr\collection1\conf目录下面的scheme.xml文件），在<types></types>配置项间加一段如下配置：

 <fieldType name="text_ik" class="solr.TextField">   

     <analyzer class="org.wltea.analyzer.lucene.IKAnalyzer"/>   

 </fieldType>

在<fields></fields>配置项间加一段如下配置：

<field name="text"      type="text_ik"   indexed="true"  stored="true"  multiValued="true" />

说明：这里的text是field，而text_ik是fieldType

三、测试配置是否成功

保存以上修改后，重启tomcat，在浏览器中输入网址：http://localhost:8983/solr/#/collection1/analysis

如配置正确则出现如下界面：


在Field Value(Index)下面的文本框中输入中文：

我在配置IK Analyzer中文分词，结果配置成功。

然后在Analyse Fieldname / FieldType:右边的下拉框中选择“text”。点击“AnalyseValues”则会显示分词的结果：


四、为字段text_general添加IK Analyzer中文分词效果

       修改…tomcat\webapps\solr_home\colletion1\conf目录下的schema.xml文件，找到name=”text_general”的<fieldType>字段类型，修改如下：


说明：

1. 不能将positionIncrementGap="100"放入到<fieldType>字段类型中去，因为IKAnalyzer不支持positionIncrementGap的属性注入；若添加则启动tomcat时会出现org.apache.solr.common.SolrException: Plugin Initializing failurefor [schema.xml] fieldType错误提示

2. <analyzer></analyzer>包含的内容是solr自带的分词库，如果不想使用solr自带的分词库，直接在上图中去掉<analyzer></analyzer>包含的内容即可。

3. 为字段text_general添加了IK Analyzer中文分词效果后，其实，在本文上面第二点的2中就没必要进行添加操作了。
