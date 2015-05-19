#include <time.h>
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

int main(int argc, char *argv[])
{
	char zdata_buf[128];
	struct tm *local;
	time_t t;

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

    sleep(3); /* Sleep for a few second for connection to complete */

	if (is_connected) 
	{
		if (ZNONODE == zoo_exists(zh, zoo_path, 0, NULL))
		{
			fprintf(stderr, "%s doesn't exist! \
                    Please start zdata_watcher.\n", zoo_path);
			exit(EXIT_FAILURE);
		}

		while(1) 
		{
			t = time(NULL);
			local = localtime(&t);
			memset(zdata_buf,'\0',strlen(zdata_buf));
			strcpy(zdata_buf,asctime(local));
			
			if (ZOK != zoo_set(zh, zoo_path, zdata_buf, strlen(zdata_buf), -1))
			{
				fprintf(stderr, "Error in write at %s!\n", zoo_path);
			}
		
			sleep(5);
		}
	}
	
    return 0;
}
