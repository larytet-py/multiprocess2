# -*- coding: UTF-8 -*-

"""Main
Implements a simple multiprocessing demo
See  https://bugs.python.org/issue40860

Try 

    docker build --tag multiprocess . && docker run -e LOGLEVEL=INFO multiprocess
"""

import logging
import os
import math
import time
import random
import threading
import multiprocessing
import psutil

def waste_time(deadline):
    '''
    Waste some time idling
    '''
    time.sleep(200*deadline)


job_counter = 0
spawn_job_mutex = threading.Lock()
def spawn_job(deadline):
    '''
    Creat a new Process, call join(), process errors
    '''    
    global job_counter
    time_start = time.time()
    # https://bugs.python.org/issue40860
    with spawn_job_mutex:
        job = multiprocessing.Process(target=waste_time, args=(deadline, ))
        job.start()
    job.join(deadline)
    elapsed = time.time()-time_start
    if elapsed < deadline and job.is_alive():
        logger.error(f"#{job_counter}: job.join() returned while process {job.pid} is still alive elapsed={elapsed} deadline={deadline}")
    job.terminate()
    try:
        job.close()
    except Exception as e:
        logger.debug(f"job.close() failed {e}")
    # A not atomic counter, I do not care about precision
    job_counter += 1        

def spawn_thread(deadline):
    '''
    Spawn a thread wich in turn creates a process
    '''
    thread = threading.Thread(target=spawn_job, args=(deadline, ))
    thread.start()
    return thread

def spawn_threads(deadline, amount):
    threads = []
    for _ in range(amount):
        thread = spawn_thread(deadline)
        threads.append(thread)
    return threads

def join_random_thread(threads, deadline):
    '''
    Pick a random thread, call join()
    '''
    # By choosing random sampling I can trigger the exception faster (20s?)
    sample = random.sample(range(0, len(threads)), 1)[0]
    # Picking the oldest is a slower way to get the exception (1-2 minutes?) 
    #sample = 0
    thread = threads[sample]
    thread.join()
    return thread

def run_it_all():
    '''
    1. Start a bunch of processes, 
    2. call join() for one of them,
    3. start a new process
    4. Goto step 2
    '''
    start = time.time()
    process = psutil.Process(os.getpid())
    deadline=0.2
    cores = multiprocessing.cpu_count()
    threads = spawn_threads(deadline=deadline, amount=2*cores)
    while True:
        thread = join_random_thread(threads, deadline)
        threads.remove(thread)

        thread = spawn_thread(deadline=deadline)
        threads.append(thread)
        if time.time() - start > 5.0:
            logger.info(process.memory_info().rss)
            start = time.time()
    
if __name__ == '__main__':
    logger_format = '%(name)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s'
    logging.basicConfig(format=logger_format)
    logger = logging.getLogger('multiprocess')
    loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
    logger.setLevel(loglevel)
    logger.debug("Starting debug log")

    run_it_all()


