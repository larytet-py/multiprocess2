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
    timeout = deadline + 0.100
    time_start = time.time()
    job = multiprocessing.Process(target=load_cpu, args=(deadline, ))
    job.start()
    job.join(timeout)
    elapsed = time.time()-time_start
    if elapsed < timeout and job.is_alive():
        print("job.join() returned too early")


def spawn_jobs(amount):
    jobs = []
    for _ in range(amount):
        job = threading.Thread(target=spawn_job, args=(0.200, ))
        job.start()
        jobs.append(job)
    return jobs

def join_jobs(jobs):
    for job in jobs:
        job.join()

def run_it_all():
    while True:
        jobs = spawn_jobs(8)
        join_jobs(jobs)
    
if __name__ == '__main__':
    logger = logging.getLogger('multiprocess')
    loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
    if loglevel == "": loglevel = os.environ.get("LOG_LEVEL", "INFO").upper()
    run_it_all()