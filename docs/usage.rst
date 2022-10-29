=====
Usage
=====

To use sharedprocesspool in a project::

    from sharedprocesspool.workpool import Workpool
    def mul_2(x):
        return x * 2
    with Workpool(num_workers = 5, max_items = 100) as pool:
        for item in range(0, 10000):
            pool.submit(mul_2, item)
        for result in pool.results():
            print(result)

