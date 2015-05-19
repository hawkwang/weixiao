public void testCuratorClient() throws Exception
{
    CuratorZookeeperClient client = 
                        new CuratorZookeeperClient(
                                server.getConnectString(), 
                                10000, 10000, null, 
                                new RetryOneTime(1));
    client.start();
    try 
    {
        client.blockUntilConnectedOrTimedOut();
        String path = 
                    client.getZooKeeper().create(
                                "/test_znode", 
                                "".getBytes(), 
                                ZooDefs.Ids.OPEN_ACL_UNSAFE, 
                                CreateMode.PERSISTENT);
    }
    finally
    {
        client.close();
    }
}
