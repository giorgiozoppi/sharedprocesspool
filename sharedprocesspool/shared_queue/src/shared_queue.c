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
#include "shared_queue.h"

queue_pool_t *allocate_queue_pool(uint64_t size) {
  queue_pool_t *data = (queue_pool_t *)calloc(1, sizeof(queue_pool_t));
  int flags = O_RDWR | O_CREAT;
  int fd = shm_open(queue_default_name, flags, S_IRUSR | S_IWUSR);
  if (fd < 0) {
    fprintf(stderr, "Failed to created the queue pool: cannot allocate %lu size\n", size);
    exit(EXIT_FAILURE);
  }
  if (ftruncate(fd, size) < 0) {
    fprintf(stderr, "Failed to created the queue pool: cannot truncate file %s\n", strerror(errno));
    exit(EXIT_FAILURE);
  }
  /* Map shared memory object */

  data->pool = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
  strncpy(data->shm_path, queue_default_name, sizeof(data->shm_path));
  data->shm_path[sizeof(data->shm_path) - 1 ] = 0;

  if (data->pool == MAP_FAILED) {
    fprintf(stderr, "Failed to created the queue pool, failed to mmap\n");
  }
  data->size = size;
  data->fd = fd;
}
void destroy_queue_pool(queue_pool_t *pool) {
  if (shm_unlink(pool->shm_path) < 0) {
    fprintf(stderr, "Failed to destroy pool");
    free(pool);
    exit(EXIT_FAILURE);
  }
  pool = NULL;
}
