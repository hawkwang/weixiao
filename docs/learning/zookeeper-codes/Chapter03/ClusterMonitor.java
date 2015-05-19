import java.io.IOException;
import java.util.List;

import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooDefs.Ids;
import org.apache.zookeeper.ZooKeeper;


public class ClusterMonitor implements Runnable {
	
	private static String membershipRoot = "/Members";
	private final Watcher connectionWatcher;
	private final Watcher childrenWatcher;
	
	private ZooKeeper zk;
	boolean alive=true;
	
	public ClusterMonitor(String HostPort) 
			throws IOException, InterruptedException, KeeperException {
		
		connectionWatcher = new Watcher() {
		    @Override
		    public void process(WatchedEvent event) {
		    	if(event.getType() == Watcher.Event.EventType.None &&
		    			event.getState() == Watcher.Event.KeeperState.SyncConnected) {
		    		System.out.printf("\nEvent Received: %s", event.toString());
		    	}   
		    }
		};
    
	    childrenWatcher = new Watcher() {
	    	@Override
	    	public void process(WatchedEvent event) {
	    		System.out.printf("\nEvent Received: %s", event.toString());
	    		if (event.getType() == Event.EventType.NodeChildrenChanged) {
		    		try {
		    			//Get current list of child znode, reset the watch
		    			List<String> children = zk.getChildren(
		    					membershipRoot, this);
		    			wall("!!! Cluster Membership Change !!!");
		    			wall("Members: " + children);
		    		} catch (KeeperException e) {
		    			throw new RuntimeException(e);
		    		} catch (InterruptedException e) {
		    			Thread.currentThread().interrupt();
		    			alive = false;
		    			throw new RuntimeException(e);
		    		}
	    		}
	    	}
	    };

	    zk = new ZooKeeper(HostPort, 2000, connectionWatcher);

	    // Ensure the parent znode exists
	    if(zk.exists(membershipRoot, false) == null) {
	    	zk.create(membershipRoot, "ClusterMonitorRoot".getBytes(), 
	    			Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
	    }

	    // Set a watch on the parent znode
	    List<String> children = zk.getChildren(membershipRoot, childrenWatcher);
	    System.err.println("Members: " + children);
	}

	public synchronized void close() {
		try {
			zk.close();
		}
		catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	public void wall (String message) {
		System.out.printf("\nMESSAGE: %s", message);
	}
	
	public void run() {
		try {
			synchronized (this) {
	              while (alive) {
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

	public static void main(String[] args) 
			throws IOException, InterruptedException, KeeperException {
        if (args.length != 1) {
            System.err.println("Usage: ClusterMonitor <Host:Port>");
            System.exit(0);
        }
        String hostPort = args[0];
        new ClusterMonitor(hostPort).run();
	}
}
