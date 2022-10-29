=================
SharedProcessPool
=================


.. image:: https://img.shields.io/pypi/v/sharedprocesspool.svg
        :target: https://pypi.python.org/pypi/sharedprocesspool

.. image:: https://img.shields.io/travis/giorgiozoppi/sharedprocesspool.svg
        :target: https://travis-ci.com/giorgiozoppi/sharedprocesspool

.. image:: https://readthedocs.org/projects/sharedprocesspool/badge/?version=latest
        :target: https://sharedprocesspool.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/giorgiozoppi/sharedprocesspool/shield.svg
     :target: https://pyup.io/repos/github/giorgiozoppi/sharedprocesspool/
     :alt: Updates



SharedProcessPool is package that implements embarassing parallel using shared memory this will avoid pickling from input and output data. We provide two
modules:
 - workpool. A pure python process pool that works in batches, tested for realibility and scalability using pickling
 - sharedprocesspool. An efficient process pool that avoid pickling mapping input data and output in a shared memory scoreboard.


* Free software: MIT license
* Documentation: https://sharedprocesspool.readthedocs.io.

### Usage
```python
import hashlib
from sharedprocesspool import Workpool
def read_chunks() -> bytearray:
    ........
def checksum(data):
     return hashlib.sha256(data).hexdigest()
            
with Workpool(num_workers=1) as pool:
        for chunk in _read_chunks():
            params = tuple([chunk])
            pool.submit(checksum, *params)
        for result in pool.results():
            print(result)
```

Features
--------

* TODO

