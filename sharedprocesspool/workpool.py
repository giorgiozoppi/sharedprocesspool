"""
This module implements a simple workpool without just using multiprocessing and without using shared memory.
It tries just to limit the amount of data processed in order to avoid a broken pipe.
Python multiprocessing Queue are implemented by Unix Pipes.
"""
import multiprocessing
import time
import logging
_LOGGER = logging.getLogger("Workpool")
_LOGGER.setLevel(logging.INFO)

class PoisonPill:
    """PoisonPill is a termination token for the pool
    """    
    pass

def _worker_id() -> None:
    """This function is associated to the termination token"""
    return None

class _WorkItem:
    args = None
    target = None
    poison = False
    def __init__(self, target, poison, /, *args):
        self.args = args
        self.poison = poison
        self.target = target
        

class Workpool:
    def __init__(self, num_workers: int = 1, max_items = 100):
        self.manager: multiprocessing.Manager = multiprocessing.Manager()
        self.i_queue: multiprocessing.Queue = self.manager.Queue()
        self.o_queue: multiprocessing.Queue = self.manager.Queue()
        self.process_manager = None
        self.workers = num_workers
        self.max_items = max_items
        self.processes = []
        self.start_time = float(0)
        self.end_time = float(0)
        self.started = False
        self.shallClose = False
        self.semaphore = multiprocessing.Semaphore(self.max_items)

    def __enter__(self):
        self.start_time = time.perf_counter()
        self.process_manager = multiprocessing.Process(target=self._start_processes)
        self.process_manager.start()
        self.shallClose = True
        _LOGGER.info("Workpool started at %f", self.start_time)
        self.started = True
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            return False # uncomment to pass exception through
        else:
            _LOGGER.info("Workpool executed batch in %f seconds, average per worker %f", self.completion_time(), self.completion_time()/ self.workers)

    def submit(self, target, /, *args)-> None:
        # pickle add value to the inargs.
        self.i_queue.put(_WorkItem(target, None,*args))
        
        if not self.started:
            self.start_time = time.perf_counter()
            self.process_manager = multiprocessing.Process(target=self._start_processes)
            self.process_manager.start()
            _LOGGER.info("Workpool started at %f", self.start_time)
            self.started = True
        # semaphore to limit the data on the pipes and avoid broken pipes.
        self.semaphore.acquire() 
        
    def close(self):
        for _ in range(self.workers * 2):
            self.i_queue.put(_WorkItem(_worker_id, PoisonPill()))
        for p in self.processes:
            p.join()

        self.process_manager.join()       

    def completion_time(self):
        return self.end_time - self.start_time

    def _start_processes(self):
        _LOGGER.info("Start %d processes in the workpool", self.workers)
        current_args = []
        current_args.append(self.i_queue)
        current_args.append(self.o_queue)

        for _ in range(self.workers):
            p = multiprocessing.Process(
                target=self._worker_wrapper())
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

    def results(self):
        if self.shallClose:
            self.close() 
            self.shallClose = False  
        processor_finished = 0
        while True:
            new_result = self.o_queue.get()
            if isinstance(new_result, PoisonPill):
                processor_finished += 1
                if processor_finished == self.workers:
                    self.started = False
                    self.end_time = time.perf_counter()
                    break
            else:
                yield new_result







