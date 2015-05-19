#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#include <zookeeper.h>

/* ZooKeeper Znode Data Length (1MB, the max supported) */
#define ZDATALEN    1024 * 1024

static char *host_port;
static char *zoo_path = "/MyData";

static zhandle_t *zh;
static int is_connected;
static char *watcher_ctx = "ZooKeeper Data Watcher";

/**
 * Watcher function for connection state change events 
 */
void connection_watcher(zhandle_t *zzh, int type, int state, const char *path,
             void* context)
{
    if (type == ZOO_SESSION_EVENT) 
	{
        if (state == ZOO_CONNECTED_STATE) 
		{
            is_connected = 1;
        } 
		else
		{
			is_connected = 0;
		}
    }
}

/**
 * Watcher function for data change event generated in the /MyData node
 */
static void
data_watcher(zhandle_t *wzh, int type, int state, const char *zpath,
    void *watcher_ctx)
{
    char *zoo_data = malloc(ZDATALEN * sizeof(char));
    int zoo_data_len = ZDATALEN;

    if (state == ZOO_CONNECTED_STATE)
    {
		if (type == ZOO_CHANGED_EVENT)
		{
            /* Get the updated data and reset the watch */
            zoo_wget(wzh, zoo_path, data_watcher, (void *)watcher_ctx,
                zoo_data, &zoo_data_len, NULL);
			fprintf(stderr, "!!! Data Change Detected !!!\n");
            fprintf(stderr, "%s\n", zoo_data);
        }
    }
}

int main(int argc, char *argv[])
{
    int zdata_len;
	char *zdata_buf = NULL;

    if (argc != 2) 
	{
        fprintf(stderr, "USAGE: %s host:port\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    host_port = argv[1];

    zh = zookeeper_init(host_port, connection_watcher, 2000, 0, 0, 0);
    
	if (zh == NULL) 
    {
        fprintf(stderr, "Error connecting to ZooKeeper server[%d]!\n", errno);
        exit(EXIT_FAILURE);
    }

    while (1)
    {
        if (is_connected) 
        {
            zdata_buf = (char *) malloc (ZDATALEN * sizeof(char));
            
            if (ZNONODE == zoo_exists(zh, zoo_path, 0, NULL))
            {
                if (ZOK == zoo_create( zh, zoo_path, NULL, -1, 
                            &ZOO_OPEN_ACL_UNSAFE, 0, NULL, 0))
                {
                    fprintf(stderr, "%s created!\n", zoo_path);
                }
                else
                {
                    fprintf(stderr, " Error Creating %s!\n", zoo_path);
                    exit(EXIT_FAILURE);
                }
            }
        
            if (ZOK != zoo_wget(zh, zoo_path, data_watcher, watcher_ctx, 
                        zdata_buf, &zdata_len, NULL))
            {
                fprintf(stderr, "Error setting watch at %s!\n", zoo_path);
            }
            
            pause();
        }
    }
	
    free(zdata_buf);
    return 0;
}
