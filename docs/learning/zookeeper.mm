<map version="0.9.0">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node CREATED="1431563822998" ID="ID_1825471418" MODIFIED="1431563841607" TEXT="zookeeper">
<node CREATED="1431564199298" ID="ID_1656371843" MODIFIED="1431564211102" POSITION="right" TEXT="what is it?">
<node CREATED="1431564214745" ID="ID_140202377" MODIFIED="1431564232485" TEXT="centralized coordination service"/>
<node CREATED="1431564239275" ID="ID_720709713" MODIFIED="1431564250281" TEXT="zookeeper ensemble">
<node CREATED="1431572101448" ID="ID_1885958200" MODIFIED="1431572107600" TEXT="quorum">
<node CREATED="1431572076559" ID="ID_317506402" MODIFIED="1431572128151" TEXT="zookeeper instances are working in a leader / follower format"/>
<node CREATED="1431564711188" ID="ID_1524835182" MODIFIED="1431564738666" TEXT="minimum recommended size - 3 on seperate machines"/>
<node CREATED="1431572065962" ID="ID_919985996" MODIFIED="1431572075656" TEXT="better to have 5"/>
</node>
<node CREATED="1431572897276" ID="ID_248158298" MODIFIED="1431572926602" TEXT="multiple node modes - operations">
<node CREATED="1431572941831" ID="ID_1331613526" MODIFIED="1431572947745" TEXT="single machine version">
<node CREATED="1431572950790" ID="ID_315083402" MODIFIED="1431573495862" TEXT="1) create three different configuration files under conf folder of ${ZK_HOME} - &#xa;zoo1.cfg, zoo2.cfg and zoo3.cfg">
<node CREATED="1431573086615" ID="ID_447601910" MODIFIED="1431573160718" TEXT="tickTime=2000 &#xa;initLimit=5 &#xa;syncLimit=2 &#xa;dataDir=/home/hawk/Documents/tmp/zookeeper/zoo1 &#xa;clientPort=2181 &#xa;server.1=localhost:2666:3666 &#xa;server.2=localhost:2667:3667 &#xa;server.3=localhost:2668:3668"/>
<node CREATED="1431573086615" ID="ID_532944272" MODIFIED="1431573193332" TEXT="tickTime=2000 &#xa;initLimit=5 &#xa;syncLimit=2 &#xa;dataDir=/home/hawk/Documents/tmp/zookeeper/zoo2 &#xa;clientPort=2182 &#xa;server.1=localhost:2666:3666 &#xa;server.2=localhost:2667:3667 &#xa;server.3=localhost:2668:3668"/>
<node CREATED="1431573086615" ID="ID_629637335" MODIFIED="1431573201798" TEXT="tickTime=2000 &#xa;initLimit=5 &#xa;syncLimit=2 &#xa;dataDir=/home/hawk/Documents/tmp/zookeeper/zoo3 &#xa;clientPort=2183 &#xa;server.1=localhost:2666:3666 &#xa;server.2=localhost:2667:3667 &#xa;server.3=localhost:2668:3668"/>
</node>
<node CREATED="1431573245224" ID="ID_454034606" MODIFIED="1431573480928" TEXT="2) fix the server ID parameter correctly in the myid file for each instance">
<node CREATED="1431573263502" ID="ID_722843563" MODIFIED="1431573315855">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      echo 1 &gt; /home/hawk/Documents/tmp/zookeeper/zoo1/myid
    </p>
    <p>
      echo 2 &gt; /home/hawk/Documents/tmp/zookeeper/zoo2/myid
    </p>
    <p>
      echo 3 &gt; /home/hawk/Documents/tmp/zookeeper/zoo3/myid
    </p>
  </body>
</html>
</richcontent>
</node>
</node>
<node CREATED="1431573438021" ID="ID_783373308" MODIFIED="1431573485843" TEXT="3) start the ZooKeeper instances">
<node CREATED="1431573713039" ID="ID_1757473843" MODIFIED="1431573716643" TEXT="${ZK_HOME}/bin/zkServer.sh start ${ZK_HOME}/conf/zoo1.cfg"/>
<node CREATED="1431573718075" ID="ID_1750960411" MODIFIED="1431573729497" TEXT="${ZK_HOME}/bin/zkServer.sh start ${ZK_HOME}/conf/zoo2.cfg"/>
<node CREATED="1431573719833" ID="ID_113452857" MODIFIED="1431573731959" TEXT="${ZK_HOME}/bin/zkServer.sh start ${ZK_HOME}/conf/zoo3.cfg"/>
</node>
<node CREATED="1431573461461" ID="ID_178669946" MODIFIED="1431573490205" TEXT="4) connect to the multinode ZooKeeper cluster">
<node CREATED="1431577716522" ID="ID_733977114" MODIFIED="1431577863281" TEXT="zkCli.sh -server localhost:2181,localhost:2182,localhost:2183"/>
</node>
</node>
</node>
</node>
</node>
<node CREATED="1431564253999" ID="ID_1098404943" MODIFIED="1431564274654" POSITION="right" TEXT="common distributed coordination tasks">
<node CREATED="1431564278271" ID="ID_423362975" MODIFIED="1431564286411" TEXT="configuration management"/>
<node CREATED="1431564286913" ID="ID_945558149" MODIFIED="1431564293109" TEXT="naming service">
<node CREATED="1431564349078" ID="ID_1016961318" MODIFIED="1431564357859" TEXT="service discovery"/>
</node>
<node CREATED="1431564293747" ID="ID_1864667491" MODIFIED="1431564311325" TEXT="distributed sysnchronization, such as locks and barries"/>
<node CREATED="1431564311556" ID="ID_328307147" MODIFIED="1431564340339" TEXT="cluster membership operations,such as detection of node join or leave"/>
<node CREATED="1431564384772" ID="ID_1340077734" MODIFIED="1431564404207" TEXT="ensure high availability">
<node CREATED="1431564410928" ID="ID_709469639" MODIFIED="1431564420262" TEXT="fault tolerance"/>
</node>
</node>
<node CREATED="1431564500578" ID="ID_1874733229" MODIFIED="1431564502852" POSITION="right" TEXT="client">
<node CREATED="1431564438290" ID="ID_1371654271" MODIFIED="1431571336094" TEXT="client bindings">
<node CREATED="1431564447078" ID="ID_1895666119" MODIFIED="1431564449466" TEXT="C"/>
<node CREATED="1431564449913" ID="ID_5094464" MODIFIED="1431564451515" TEXT="Java">
<node CREATED="1431571340752" ID="ID_1318963325" MODIFIED="1431571342586" TEXT="zkCli.sh -server localhost:2181"/>
</node>
<node CREATED="1431564452017" ID="ID_1582914009" MODIFIED="1431564455100" TEXT="Perl"/>
<node CREATED="1431564455510" ID="ID_1843531936" MODIFIED="1431564475672" TEXT="Python"/>
</node>
<node CREATED="1431564479536" FOLDED="true" ID="ID_747801673" MODIFIED="1431564533593" TEXT="Communicty contributed client libraries">
<node CREATED="1431564509934" ID="ID_693382430" MODIFIED="1431564518302" TEXT="Go"/>
<node CREATED="1431564519033" ID="ID_1102224370" MODIFIED="1431564521884" TEXT="Scala"/>
<node CREATED="1431564522153" ID="ID_573222638" MODIFIED="1431564526560" TEXT="Erlang"/>
<node CREATED="1431564526954" ID="ID_1192169222" MODIFIED="1431564530771" TEXT="etc."/>
</node>
</node>
<node CREATED="1431568461610" ID="ID_1621867539" MODIFIED="1431573139001" POSITION="right" TEXT="installation">
<node CREATED="1431568469089" ID="ID_1527369460" MODIFIED="1431572888458" TEXT="-------------- zookeeper 3.4.6 ------------------------- &#xa;wget http://www.gtlib.gatech.edu/pub/apache/zookeeper/stable/zookeeper-3.4.6.tar.gz &#xa;ls -alh zookeeper-3.4.6.tar.gz  &#xa;sudo tar -C /usr/share -zxf zookeeper-3.4.6.tar.gz &#xa;cd /usr/share/zookeeper-3.4.6/ &#xa;ls  &#xa;&#xa;&#x66f4;&#x65b0;&#x73af;&#x5883;&#x53d8;&#x91cf;&#xa;vi ~/.bashrc&#xa;export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64&#xa;export CLASSPATH=.:$JAVA_HOME/jre/lib/dt.jar:$JAVA_HOME/jre/lib/tools.jar:$JAVA_HOME/jre/lib/rt.jar:$JAVA_HOME/jre/lib&#xa;export PATH=$PATH:$JAVA_HOME/bin&#xa;export ZK_HOME=/usr/share/zookeeper-3.4.6&#xa;export PATH=$PATH:$ZK_HOME/bin&#xa;&#xa;source ~/.bashrc&#xa;&#xa;&#x66f4;&#x6539;singlenode mode&#x4e0b;&#x7684;&#x914d;&#x7f6e;&#x6587;&#x4ef6;&#xff0c;&#x5176;&#x4e2d;dataDir&#x9700;&#x8981;&#x5f53;&#x524d;&#x7528;&#x6237;&#x53ef;&#x8bbf;&#x95ee;&#x6743;&#x9650;&#xa;$ sudo vi conf/zoo.cfg&#xa;tickTime=2000&#xa;dataDir=/home/hawk/Documents/tmp/zookeeper&#xa;clientPort=2181&#xa;&#xa;&#x8fd0;&#x884c;&#xa;zkServer.sh start&#xa;&#xa;&#x68c0;&#x67e5;&#x662f;&#x5426;&#x8fd0;&#x884c;&#x6b63;&#x5e38;&#xa;ps -ef | grep zookeeper | grep -v grep | awk &apos;{print $2}&apos;&#xa;&#x6216;&#x8005;&#xa;jps&#xa;&#x5f97;&#x5230; QuorumPeerMain&#xa;&#x6216;&#x8005;&#xa;zkServer.sh status&#xa;&#xa;&#xa;"/>
</node>
</node>
</map>
