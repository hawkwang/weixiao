import java.io.IOException;
import java.lang.management.ManagementFactory;

import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooDefs.Ids;
import org.apache.zookeeper.ZooKeeper;


public class ClusterClient implements Watcher, Runnable {
	
	private static String membershipRoot = "/Members";
	ZooKeeper zk;
	
	public ClusterClient(String hostPort, Long pid) {
		String processId = pid.toString();
		try {
			zk = new ZooKeeper(hostPort, 2000, this);
		} catch (IOException e) {
			e.printStackTrace();
		}
		if (zk != null) {
			try {
				zk.create(membershipRoot + '/' + processId, processId.getBytes(), 
						Ids.OPEN_ACL_UNSAFE, CreateMode.EPHEMERAL);
			} catch (KeeperException | InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
	public synchronized void close() {
		try {
			zk.close();
		}
		catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	@Override
	public void process(WatchedEvent event) {
		System.out.printf("\nEvent Received: %s", event.toString());
	}
	
	public void run() {
		try {
			synchronized (this) {
	              while (true) {
	            	  wait();
	              }
			}
	      } catch (InterruptedException e) {
	    	  e.printStackTrace();
	    	  Thread.currentThread().interrupt();
	      } finally {
	    	  this.close();
	      }
	  }

	public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Usage: ClusterClient <Host:Port>");
            System.exit(0);
        }
        String hostPort = args[0];
        //Get the process id
        String name = ManagementFactory.getRuntimeMXBean().getName();
        System.out.println("process : " + name);
        int index = name.indexOf('@');
        Long processId = Long.parseLong(name.substring(0, index));
        new ClusterClient(hostPort, processId).run();
	}
}
