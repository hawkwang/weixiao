import signal
from kazoo.client import KazooClient
from kazoo.recipe.watchers import ChildrenWatch

zoo_path = '/MyPath'

zk = KazooClient(hosts='localhost:2181')
zk.start()
zk.ensure_path(zoo_path)

@zk.ChildrenWatch(zoo_path)
def child_watch_func(children):
    print "List of Children %s" % children

while True:
    signal.pause()
