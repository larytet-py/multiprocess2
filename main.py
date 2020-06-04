# -*- coding: UTF-8 -*-

"""Main
Implements a simple multiprocessing demo

https://bugs.python.org/issue40860?@ok_message=msg%20370695%20created%0Aissue%2040860%20created&@template=item
Try 

    docker build --tag multiprocess .
    docker run -e LOGLEVEL=DEBUG multiprocess
"""

import logging
import os
import math
import time
import random
import threading
import multiprocessing

def load_cpu(deadline):
    start = time.time()

    while time.time() - start < deadline:
        math.pow(random.randint(0, 1), random.randint(0, 1))

def spawn_job(deadline):
    timeout = deadline + 0.02*deadline
    time_start = time.time()
    job = multiprocessing.Process(target=load_cpu, args=(deadline, ))
    job.start()
    job.join(timeout)
    elapsed = time.time()-time_start
    if elapsed < timeout and job.is_alive():
        logger.error("job.join() returned too early")

def spawn_thread(deadline):
    thread = threading.Thread(target=spawn_job, args=(deadline, ))
    thread.start()
    return thread

def spawn_threads(deadline, amount):
    threads = []
    for _ in range(amount):
        thread = spawn_thread(deadline)
        threads.append(thread)
    return threads

def join_random_thread(threads):
    thread = random.sample(range(0, len(threads)), 1)
    thread.join()
    return thread

def run_it_all():
    threads = spawn_threads(deadline=0.020, amount=8)
    while True:
        thread = join_random_thread(threads)
        threads.remove(thread)

        thread = spawn_thread(deadline=0.020)
        threads.append(thread)
    
if __name__ == '__main__':
    logger = logging.getLogger('multiprocess')
    loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
    if loglevel == "": loglevel = os.environ.get("LOG_LEVEL", "INFO").upper()
    run_it_all()