"""
This module implements a simple workpool without just using multiprocessing and without using shared memory.
It tries just to limit the amount of data processed in order to avoid a broken pipe.
Python multiprocessing Queue are implemented by Unix Pipes.
"""
import logging
import multiprocessing
import time
from multiprocessing import synchronize
from typing import Any, Callable, Generator, List

from typing_extensions import TypeAlias

_LOGGER = logging.getLogger("Workpool")
_LOGGER.setLevel(logging.INFO)
_SemaphoreType: TypeAlias = synchronize.Semaphore


class _PoisonPill:
    """PoisonPill is a termination token for the pool
    """
    pass


def _worker_id() -> None:
    """This function is associated to the termination token"""
    return None


class _WorkItem:
    """Item to be passed to the processes
    """
    args: Any = None
    target: Callable
    poison: _PoisonPill

    def __init__(self, target, poison, /, *args):
        self.args = args
        self.poison = poison
        self.target = target


class Workpool:
    """Class that implements a process workpool
        trying to provide the user the max dimension of the batch.
        When that size is reached we'll wait until the user
        has consumed all the data.
        This makes sense in order to process huge amount of data.
    """

    def __init__(self, num_workers: int = 1, max_items=100):
        """_summary_

        Args:
            num_workers (int, optional): _description_. Defaults to 1.
            max_items (int, optional): _description_. Defaults to 100.
        """
        self.manager: Any = multiprocessing.Manager()
        self.i_queue: multiprocessing.Queue = self.manager.Queue()
        self.o_queue: multiprocessing.Queue = self.manager.Queue()
        self.process_manager: multiprocessing.Process = multiprocessing.Process(
            target=self._start_processes)
        self.workers: int = num_workers
        self.max_items: int = max_items
        self.processes: List[multiprocessing.Process] = []
        self.start_time: float = float(0)
        self.end_time: float = float(0)
        self.started: bool = False
        self.shallClose: bool = False
        self.semaphore: _SemaphoreType = multiprocessing.Semaphore(
            self.max_items)

    def __enter__(self):

        self.start_time: float = time.perf_counter()
        self.process_manager.start()
        self.shallClose: bool = True
        _LOGGER.info("Workpool started at %f", self.start_time)
        self.started: bool = True
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            return False  # uncomment to pass exception through
        else:
            _LOGGER.info(
                "Workpool executed batch in %f seconds, average per worker %f",
                self.completion_time(),
                self.completion_time() / self.workers)

    def submit(self, target: Callable, /, *args) -> None:
        """_summary_

        Args:
            target (Callable): _description_
        """
        # pickle add value to the inargs.
        self.i_queue.put(_WorkItem(target, None, *args))

        if not self.started:
            self.start_time = time.perf_counter()
            self.process_manager = multiprocessing.Process(
                target=self._start_processes)
            self.process_manager.start()
            _LOGGER.info("Workpool started at %f", self.start_time)
            self.started = True
        # semaphore to limit the data on the pipes and avoid broken pipes.
        self.semaphore.acquire()

    def results(self) -> Generator[Any, None, None]:
        """Method that returns a generator for the results

        Yields:
            Any: result of the processing.
        """
        if self.shallClose:
            self.close()
            self.shallClose = False
        processor_finished: int = 0
        while True:
            new_result = self.o_queue.get()
            if isinstance(new_result, _PoisonPill):
                processor_finished += 1
                if processor_finished == self.workers:
                    self.started = False
                    self.end_time = time.perf_counter()
                    break
            else:
                yield new_result

    def close(self):
        """Method that closes the workpool and free the resources
           This method shall always called for making the workpool
           happy except when it is used as context manager.
        """
        for _ in range(self.workers):
            self.i_queue.put(_WorkItem(_worker_id, _PoisonPill()))
        for p in self.processes:
            p.join()

        self.process_manager.join()

    def completion_time(self):
        """Method that estimate the completion time.
            It is recommended that this method will be called
            after fetching the results

        Returns:
            float: completion time of the batch in seconds
        """
        return self.end_time - self.start_time

    def _start_processes(self):
        _LOGGER.info("Start %d processes in the workpool", self.workers)
        current_args = []
        current_args.append(self.i_queue)
        current_args.append(self.o_queue)

        for _ in range(self.workers):
            p = multiprocessing.Process(target=self._worker_wrapper())
            self.processes.append(p)
            p.start()

    def _worker_wrapper(self) -> None:
        in_queue = self.i_queue
        out_queue = self.o_queue
        stop_flag = False
        while not stop_flag:
            new_item = in_queue.get()
            if new_item.poison is None:
                result = new_item.target(*new_item.args)
            else:
                # we've finished.
                result = new_item.poison
                stop_flag = True

            out_queue.put(result)
            self.semaphore.release()
