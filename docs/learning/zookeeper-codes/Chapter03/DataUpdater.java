import java.io.IOException;
import java.util.UUID;

import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;

public class DataUpdater implements Watcher {
	
	private static String hostPort = "localhost:2181";
	private static String zooDataPath = "/MyConfig";
	
	ZooKeeper zk;

	public DataUpdater() throws IOException {
		try {
			zk = new ZooKeeper(hostPort, 2000, this);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void run() throws InterruptedException, KeeperException {
		while (true) {
			String uuid = UUID.randomUUID().toString();
			byte zoo_data[] = uuid.getBytes();
			zk.setData(zooDataPath, zoo_data, -1);
			try {
			    Thread.sleep(5000); // Sleep for 5 secs
			} catch(InterruptedException e) {
			    Thread.currentThread().interrupt();
			}
		}
	}

	public static void main(String[] args) 
			throws IOException, InterruptedException, KeeperException {
		DataUpdater dataUpdater = new DataUpdater();
		dataUpdater.run();
	}

	@Override
	public void process(WatchedEvent event) {
		System.out.printf("\nEvent Received: %s", event.toString());
	}
}