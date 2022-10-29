/**
Copyright (c) 2022 Giorgio Zoppi <giorgio.zoppi@gmail.com>

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
**/
#ifndef SHARED_QUEUE_H
#define SHARED_QUEUE_H
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <stdbool.h>
#include <linux/limits.h>
#include <unistd.h>
#include <sys/types.h>
#include <errno.h>
#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif

const uint64_t BIG_POOL_SIZE = 1024*1024*1024 * 8;
static const char *queue_default_name = "/process_pool_shm";
typedef struct queue_pool {
    void *pool;
    char shm_path[256];
    uint64_t size;
    int fd;
} queue_pool_t;
typedef struct queue_node {
    void* base_addr;
    uint64_t item_size;
    void* next_addr;
} queue_node_t;

extern queue_pool_t* allocate_queue_pool(uint64_t size);
extern void destroy_queue_pool(queue_pool_t* pool);
#ifdef __cplusplus
}
#endif
#endif