import hashlib
import os

import fallocate
import pytest

from sharedprocesspool.workpool import Workpool

_TMP_FILE = "/tmp/test.payload"
_TMP_CHUNK_SIZE = 1024 * 1024 * 50
_TMP_SIZE = 1024 * 1024 * 700
_TEST_WORKERS = 5
_TEST_BATCH_SIZE = 100


def checksum(data):
    outdata = []
    result = hashlib.sha256(data).hexdigest()
    outdata.append(result)
    return outdata


def _read_chunks():
    with open(_TMP_FILE, "w+b") as f:
        fallocate.fallocate(f, 0, _TMP_SIZE)

    with open(_TMP_FILE, "r+b") as infile:
        while True:
            chunk = infile.read(_TMP_CHUNK_SIZE)
            if not chunk:
                break
            yield chunk
    os.remove(_TMP_FILE)


@pytest.fixture
def setup_teardown_workpool():
    pool = Workpool(num_workers=5)
    yield pool
    pool = None


def test_workpool_should_be_able_to_handle_chunks(setup_teardown_workpool):
    pool = setup_teardown_workpool
    for chunk in _read_chunks():
        params = tuple([chunk])
        pool.submit(checksum, *params)
    pool.close()
    counter = 0
    for result in pool.results():
        print(result)
        counter = counter +1
        assert result[
            0] == "8565a714dca840f8652c5bae9249ab05f5fb5a4f9f13fbe23304b10f68252da2"
    assert counter == (_TMP_SIZE / _TMP_CHUNK_SIZE)

def test_workpool_context_manager():
    with Workpool(_TEST_WORKERS, _TEST_BATCH_SIZE) as pool:
        for chunk in _read_chunks():
            params = tuple([chunk])
            pool.submit(checksum, *params)
        
        for result in pool.results():
            assert result[
                0] == "8565a714dca840f8652c5bae9249ab05f5fb5a4f9f13fbe23304b10f68252da2"
            