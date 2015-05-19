public void simpleCuratorFrameworkClient() 
                                throws Exception
{
    CuratorFramework client = 
                CuratorFrameworkFactory.newClient(
                            server.getConnectString(), 
                            new RetryOneTime(1));
    client.start();
    
    try
    {
        String path = client.create().withMode(
                       CreateMode.PERSISTENT).forPath(
                       "/test_znode", "".getBytes());
    }
    finally
    {
        client.close();
    }
}
